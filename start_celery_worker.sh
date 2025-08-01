#!/bin/bash
# Script to start Celery worker for development

echo "Starting Celery worker for SaveDriveNow..."
echo "Make sure Redis is running first: redis-server"
echo ""

cd /home/siber/Dev/savedrivenow.com

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "Activated virtual environment"
fi

# Start Celery worker
celery -A savedrivenow worker --loglevel=info --concurrency=4

echo "Celery worker stopped"
