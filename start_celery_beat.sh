#!/bin/bash
# Script to start Celery beat scheduler for periodic tasks (if needed later)

echo "Starting Celery beat scheduler for SaveDriveNow..."
echo "Make sure Redis is running first: redis-server"
echo ""

cd /home/siber/Dev/savedrivenow.com

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "Activated virtual environment"
fi

# Start Celery beat
celery -A savedrivenow beat --loglevel=info

echo "Celery beat stopped"
