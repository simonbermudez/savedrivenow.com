# Async Email Setup with Celery

This document explains how to set up and use asynchronous email sending for the SaveDriveNow application.

## Overview

The application now uses Celery with Redis as a message broker to send emails asynchronously. This provides several benefits:

- **Non-blocking**: Lead creation doesn't wait for emails to be sent
- **Reliability**: Failed emails are automatically retried
- **Scalability**: Multiple workers can process emails concurrently
- **Monitoring**: Email task status can be tracked and monitored

## Prerequisites

### Option 1: Local Redis Installation

Install Redis on your system:

```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS with Homebrew
brew install redis

# Start Redis server
redis-server
```

### Option 2: Docker Compose (Recommended)

Use the provided Docker Compose configuration:

```bash
# Start Redis and the full application
docker-compose -f docker-compose.dev.yml up

# Or just start Redis
docker-compose -f docker-compose.dev.yml up redis
```

## Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Set environment variables (optional, defaults provided):

```bash
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Running the System

### Development Setup

1. **Start Redis** (if not using Docker):
```bash
redis-server
```

2. **Start Django development server**:
```bash
python manage.py runserver
```

3. **Start Celery worker** (in a separate terminal):
```bash
# Using the provided script
./start_celery_worker.sh

# Or manually
celery -A savedrivenow worker --loglevel=info
```

### Production Setup

1. **Start Celery worker as a daemon**:
```bash
celery -A savedrivenow worker --loglevel=info --detach --pidfile=celery.pid
```

2. **Start Celery beat for periodic tasks** (if needed):
```bash
celery -A savedrivenow beat --loglevel=info --detach --pidfile=celerybeat.pid
```

## How It Works

### Email Flow

1. **Lead Creation**: When a new lead is created with vehicles, the process is:
   - Lead is saved to database
   - Vehicles are saved to database
   - Email tasks are queued asynchronously
   - User sees immediate success response

2. **Email Processing**: 
   - Celery workers pick up email tasks from the queue
   - Each subscriber gets an individual email task
   - Failed emails are automatically retried (up to 3 times)
   - Subscriber email counters are updated after successful sends

### Task Types

- `send_lead_notification_email_async`: Sends lead notification to a single recipient
- `send_welcome_email_async`: Sends welcome email to the lead
- `send_emails_to_subscribers_async`: Queues notifications for all active subscribers

## Monitoring

### View Task Status

```bash
# Monitor Celery worker
celery -A savedrivenow inspect active

# View task history
celery -A savedrivenow events
```

### Logs

- **Worker logs**: Show task processing and errors
- **Django logs**: Show email queuing and application events
- **Redis logs**: Show message broker activity

## Configuration

### Celery Settings (in `settings.py`)

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes
```

### Email Rate Limiting

The system is configured to send a maximum of 50 emails per minute to prevent overwhelming the SMTP server.

## Fallback Behavior

If Celery is not available or Redis is down, the system will automatically fall back to synchronous email sending to ensure lead notifications are still sent.

## Troubleshooting

### Common Issues

1. **"Connection refused" error**:
   - Ensure Redis is running
   - Check CELERY_BROKER_URL setting

2. **Tasks not processing**:
   - Ensure Celery worker is running
   - Check worker logs for errors

3. **Emails not sending**:
   - Check SMTP configuration
   - Verify EMAIL_HOST_PASSWORD is set
   - Check Django email logs

### Debug Commands

```bash
# Test Redis connection
redis-cli ping

# Test Celery connection
python manage.py shell -c "from celery import current_app; print(current_app.broker_connection().ensure_connection())"

# Test email task manually
python manage.py shell -c "from leads.tasks import send_lead_notification_email_async; send_lead_notification_email_async.delay(1, 'test@example.com')"
```

## Production Considerations

1. **Use a process manager** like systemd or supervisor for Celery workers
2. **Monitor queue size** and add more workers if needed
3. **Set up proper logging** and error alerting
4. **Consider using a dedicated Redis instance** for production
5. **Implement email bounce handling** for better deliverability
