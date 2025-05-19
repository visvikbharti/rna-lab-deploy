#!/bin/bash
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn rna_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4 --timeout 120