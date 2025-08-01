"""
Email utilities for the SaveDriveNow application.
Handles sending beautiful HTML emails for lead notifications.
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_lead_notification_email(lead, recipient_email, subscriber=None):
    """
    Send a beautiful HTML email notification for a new lead.
    
    Args:
        lead: The Lead instance
        recipient_email: Email address to send to
        subscriber: Optional LeadsSubscriber instance for additional context
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Prepare email context
        context = {
            'lead': lead,
            'subscriber': subscriber,
        }
        
        # Render HTML template
        html_content = render_to_string('emails/new_lead_notification.html', context)
        
        # Render text template for fallback
        text_content = render_to_string('emails/new_lead_notification.txt', context)
        
        # Create email with both HTML and text versions
        subject = f"🚗 New Lead Alert: {lead.full_name} - SaveDriveNow"
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )
        
        # Attach HTML version
        email.attach_alternative(html_content, "text/html")
        
        # Send the email
        email.send()
        
        logger.info(f"Lead notification email sent successfully to {recipient_email} for lead {lead.full_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send lead notification email to {recipient_email}: {str(e)}")
        return False


def send_welcome_email(lead):
    """
    Send a beautiful welcome email to the lead who just submitted their information.
    
    Args:
        lead: The Lead instance
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Prepare email context
        context = {
            'lead': lead,
        }
        
        # Render HTML template
        html_content = render_to_string('emails/welcome_email.html', context)
        
        # Render text template for fallback
        text_content = render_to_string('emails/welcome_email.txt', context)
        
        # Create email with both HTML and text versions
        subject = f"Thank you for your interest in auto insurance, {lead.full_name}!"
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[lead.email],
        )
        
        # Attach HTML version
        email.attach_alternative(html_content, "text/html")
        
        # Send the email
        email.send()
        
        logger.info(f"Welcome email sent successfully to {lead.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {lead.email}: {str(e)}")
        return False
