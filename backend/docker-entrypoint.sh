#!/bin/bash
set -e

# Ensure PORT has a default value if not set
export PORT=${PORT:-8000}
echo "Using PORT: $PORT"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
echo "Checking connection to PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT with user $POSTGRES_USER and database $POSTGRES_DB"

# Check if PostgreSQL variables are set
if [ -z "$POSTGRES_HOST" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_DB" ]; then
  echo "ERROR: PostgreSQL environment variables not properly set!"
  echo "POSTGRES_HOST=$POSTGRES_HOST"
  echo "POSTGRES_USER=$POSTGRES_USER"
  echo "POSTGRES_DB=$POSTGRES_DB"
  echo "POSTGRES_PORT=$POSTGRES_PORT"
  echo "Skipping PostgreSQL check and continuing..."
else
  # Try to connect to PostgreSQL with properly quoted parameters
  until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 5
  done
  echo "PostgreSQL is up - continuing"
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