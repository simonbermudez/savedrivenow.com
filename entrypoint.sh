#!/bin/bash

# Exit on any error
set -e

echo "Starting SaveDriveNow application..."

# Wait for PostgreSQL to be ready (only if DB_HOST is set)
if [ "${DB_HOST:-}" ]; then
    echo "Waiting for PostgreSQL at $DB_HOST:${DB_PORT:-5432}..."
    until pg_isready -h "${DB_HOST}" -p "${DB_PORT:-5432}" -U "${DB_USER:-postgres}"; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    echo "PostgreSQL is up - continuing..."
fi

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run celery worker 
celery -A savedrivenow worker --loglevel=info --concurrency=4 --detach

# Start the application
echo "Starting Django application..."
exec "$@"
