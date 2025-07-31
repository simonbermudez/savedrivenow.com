# Email Setup with Zoho SMTP

This guide explains how to set up email functionality in the SaveDriveNow Django application using Zoho SMTP.

## Configuration

The application is configured to send emails using Zoho's SMTP servers with the following settings:

### SMTP Settings (in settings.py)
- **Email Backend**: `django.core.mail.backends.smtp.EmailBackend`
- **SMTP Host**: `smtp.zoho.com`
- **SMTP Port**: `587`
- **Use TLS**: `True`

### Environment Variables

The following environment variables need to be set:

- `EMAIL_HOST_USER`: The Zoho email address (leads@savedrivenow.com)
- `EMAIL_HOST_PASSWORD`: The password for the Zoho email account
- `DEFAULT_FROM_EMAIL`: The default sender email address (leads@savedrivenow.com)

### Configuration Files

1. **`.env` file**: Contains the actual credentials for local development
2. **`.envsample` file**: Template with placeholder values
3. **`docker-compose.yml`**: Development Docker configuration
4. **`docker-compose.prod.yml`**: Production Docker configuration

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `python-dotenv` which is needed to load environment variables from the `.env` file.

### 2. Environment Variables

The `.env` file has been created with the Zoho credentials:

```
EMAIL_HOST_USER=leads@savedrivenow.com
EMAIL_HOST_PASSWORD=password_here_zoho
DEFAULT_FROM_EMAIL=leads@savedrivenow.com
```

### 3. Zoho Account Configuration

Make sure the Zoho account is configured to allow SMTP access:

1. Log in to your Zoho Mail account
2. Go to Settings > Security
3. Enable "Allow less secure apps" or set up App-specific passwords
4. Verify that SMTP is enabled for the account

### 4. Testing Email Functionality

To test if emails are working, you can use Django's shell:

```python
python manage.py shell

from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email',
    'This is a test email from SaveDriveNow.',
    settings.DEFAULT_FROM_EMAIL,
    ['your-test-email@example.com'],
    fail_silently=False,
)
```

## How Email is Used in the Application

The application automatically sends email notifications when new leads are created:

1. When a new `Lead` is saved, the `save()` method calls `LeadsSubscriber.email_leads_to_active_subscribers()`
2. This method finds all active subscribers (`is_active=True`)
3. For each active subscriber, it sends an email with the lead details
4. The subscriber's `number_of_leads_sent` counter is incremented

### Email Template

The email sent to subscribers includes:
- Subject: "New Lead: [Full Name]"
- Body: Lead details, email, and phone number
- From: leads@savedrivenow.com

## Security Notes

- Never commit the actual `.env` file with real credentials to version control
- Use environment variables in production environments
- Consider using Django's email backends for development (console backend for testing)
- In production, ensure TLS is properly configured

## Troubleshooting

If emails are not being sent:

1. Check that the Zoho credentials are correct
2. Verify that the Zoho account allows SMTP access
3. Check Django logs for SMTP connection errors
4. Test with Django's console email backend for debugging:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

## Production Deployment

For production deployment:

1. Set environment variables on your server/hosting platform
2. Use the production docker-compose file which includes email environment variables
3. Ensure firewall allows outbound connections on port 587
4. Consider using more robust email services for high-volume applications
