# Email System Documentation

## Overview

SaveDriveNow now features a beautiful, professional email system that sends HTML emails when leads fill out the form. The system includes two types of emails:

1. **Lead Notification Emails** - Sent to subscribers when a new lead is created
2. **Welcome Emails** - Sent to leads to thank them for their submission (optional)

## Features

### Beautiful HTML Templates
- Professional gradient design matching the SaveDriveNow brand
- Responsive design that looks great on desktop and mobile
- Fallback plain text versions for compatibility
- Rich formatting with icons, cards, and structured layouts

### Lead Notification Email Features
- Complete lead information display
- Contact buttons (email and phone)
- Vehicle information (if provided)
- Professional styling with SaveDriveNow branding
- Organized information sections

### Welcome Email Features
- Thank you message for the lead
- Clear next steps explanation
- Information summary
- Professional appearance
- Call-to-action for additional quotes

## Configuration

### Email Settings
The email system uses the existing Django email configuration in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'leads@savedrivenow.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'leads@savedrivenow.com')
```

### Enable/Disable Welcome Emails
Welcome emails are currently disabled by default. To enable them, uncomment the lines in `leads/models.py`:

```python
# Optionally send welcome email to the lead
# Uncomment the lines below if you want to send welcome emails
# from .email_utils import send_welcome_email
# send_welcome_email(self)
```

## File Structure

```
leads/
├── templates/
│   └── emails/
│       ├── new_lead_notification.html  # HTML template for lead notifications
│       ├── new_lead_notification.txt   # Text template for lead notifications
│       ├── welcome_email.html          # HTML template for welcome emails
│       └── welcome_email.txt           # Text template for welcome emails
├── email_utils.py                      # Email utility functions
├── management/
│   └── commands/
│       └── test_email_templates.py     # Command to test email templates
└── models.py                           # Updated with new email logic
```

## Testing

### Test Email Templates
Use the management command to test email templates with sample data:

```bash
# Test both notification and welcome emails
python manage.py test_email_templates --test-email your-email@example.com

# Test only notification email
python manage.py test_email_templates --test-email your-email@example.com --send-notification

# Test only welcome email
python manage.py test_email_templates --test-email your-email@example.com --send-welcome
```

### Preview in Admin
1. Go to Django Admin → Leads
2. Click on any lead
3. Click the "📧 Preview Email" link to see how the email will look
4. Add `?type=welcome` to the URL to preview the welcome email

## How It Works

### Lead Notification Flow
1. User fills out the form on the website
2. New `Lead` object is saved to the database
3. `Lead.save()` method triggers `LeadsSubscriber.email_leads_to_active_subscribers()`
4. System finds all active subscribers (`is_active=True`)
5. Beautiful HTML email is sent to each subscriber
6. Subscriber's `number_of_leads_sent` counter is incremented

### Welcome Email Flow (Optional)
1. After the lead notification emails are sent
2. If enabled, `send_welcome_email()` is called
3. Welcome email is sent to the lead's email address
4. Lead receives a thank you email with next steps

## Email Templates

### Notification Email Sections
- Header with SaveDriveNow branding
- Lead's personal information
- Contact information with clickable email/phone links
- Address details
- Driving history
- Vehicle information (if provided)
- Action buttons for easy contact
- Professional footer

### Welcome Email Sections
- Thank you header
- Personal greeting
- Next steps explanation (3-step process)
- Information summary
- Call-to-action section
- Professional footer with contact info

## Customization

### Styling
All styles are contained within the HTML templates. You can modify:
- Colors in the CSS variables
- Layout and spacing
- Fonts and typography
- Button styles
- Brand colors

### Content
- Update template text directly in the HTML/text files
- Modify email subject lines in `email_utils.py`
- Add new template variables as needed

### Adding New Email Types
1. Create new HTML and text templates in `leads/templates/emails/`
2. Add new function in `email_utils.py`
3. Call the function from appropriate model methods or views

## Error Handling

The email system includes comprehensive error handling:
- Failed emails are logged with details
- Subscriber counters are only incremented on successful sends
- Graceful fallback to plain text if HTML fails
- Non-blocking operation (won't prevent lead creation if email fails)

## Production Considerations

1. **Email Delivery**: Ensure SMTP credentials are properly configured
2. **Rate Limiting**: Consider implementing email rate limiting for high-volume usage
3. **Monitoring**: Monitor email delivery success rates
4. **Spam Prevention**: Ensure proper SPF/DKIM records for your domain
5. **Unsubscribe**: Consider adding unsubscribe functionality for compliance

## Troubleshooting

### Common Issues
1. **Emails not sending**: Check SMTP configuration and credentials
2. **HTML not rendering**: Verify template paths and syntax
3. **Images not showing**: Use absolute URLs for any images
4. **Mobile formatting**: Test on various email clients

### Debug Mode
In development, you can use the console email backend for testing:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This will print emails to the console instead of sending them.
