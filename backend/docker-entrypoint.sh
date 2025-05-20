#!/bin/bash
set -e

# Ensure PORT has a default value if not set
export PORT=${PORT:-8000}
export HEALTH_PORT=8001
echo "Using PORT: $PORT for Gunicorn and HEALTH_PORT: $HEALTH_PORT for health checks"

# Print all environment variables for debugging (except sensitive ones)
echo "Environment variables available:"
env | grep -v -E 'PASSWORD|SECRET|KEY' | sort

# Skip health check servers since we're disabling health checks
echo "Health checks disabled in Railway configuration"

# Check and map Railway env vars to our expected env vars
if [ -n "$DATABASE_URL" ]; then
  echo "Found DATABASE_URL, extracting connection details"
  # Extract connection details from DATABASE_URL
  # Expected format: postgres://username:password@hostname:port/database
  export POSTGRES_USER=$(echo $DATABASE_URL | awk -F[:/@] '{print $4}')
  export POSTGRES_PASSWORD=$(echo $DATABASE_URL | awk -F[:/@] '{print $5}')
  export POSTGRES_HOST=$(echo $DATABASE_URL | awk -F[:/@] '{print $6}')
  export POSTGRES_PORT=$(echo $DATABASE_URL | awk -F[:/@] '{print $7}')
  export POSTGRES_DB=$(echo $DATABASE_URL | awk -F[:/@] '{print $8}')
  
  echo "Extracted PostgreSQL details from DATABASE_URL:"
  echo "POSTGRES_HOST=$POSTGRES_HOST"
  echo "POSTGRES_PORT=$POSTGRES_PORT"
  echo "POSTGRES_USER=$POSTGRES_USER"
  echo "POSTGRES_DB=$POSTGRES_DB"
  echo "(POSTGRES_PASSWORD hidden for security)"
fi

# If we have PGHOST, PGUSER, etc., map them to our variables
if [ -n "$PGHOST" ] && [ -z "$POSTGRES_HOST" ]; then
  echo "Found PGHOST, using Railway PostgreSQL Plugin variables"
  export POSTGRES_HOST=$PGHOST
  export POSTGRES_PORT=$PGPORT
  export POSTGRES_USER=$PGUSER
  export POSTGRES_PASSWORD=$PGPASSWORD
  export POSTGRES_DB=$PGDATABASE
  
  echo "Mapped Railway PostgreSQL Plugin variables:"
  echo "POSTGRES_HOST=$POSTGRES_HOST"
  echo "POSTGRES_PORT=$POSTGRES_PORT"
  echo "POSTGRES_USER=$POSTGRES_USER"
  echo "POSTGRES_DB=$POSTGRES_DB"
  echo "(POSTGRES_PASSWORD hidden for security)"
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
echo "Will try to connect to PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT with user $POSTGRES_USER and database $POSTGRES_DB"

# Check if PostgreSQL variables are set
if [ -z "$POSTGRES_HOST" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_DB" ]; then
  echo "WARNING: PostgreSQL environment variables not properly set!"
  echo "POSTGRES_HOST=$POSTGRES_HOST"
  echo "POSTGRES_USER=$POSTGRES_USER"
  echo "POSTGRES_DB=$POSTGRES_DB"
  echo "POSTGRES_PORT=$POSTGRES_PORT"
  echo "Skipping PostgreSQL check and continuing with SQLite..."
  
  # Set up SQLite as fallback
  export USE_SQLITE=True
else
  # Try to connect to PostgreSQL with properly quoted parameters
  export PGPASSWORD="$POSTGRES_PASSWORD"
  echo "Attempting to connect to PostgreSQL..."
  if psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; then
    echo "PostgreSQL is up and accessible - continuing"
    export USE_SQLITE=False
  else
    echo "WARNING: Could not connect to PostgreSQL. Will continue with SQLite as fallback."
    export USE_SQLITE=True
  fi
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput || {
  echo "Warning: Database migrations failed but continuing anyway."
  echo "The application may not function properly until database is available."
}

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn rna_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120