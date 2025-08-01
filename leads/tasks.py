"""
Celery tasks for handling email operations asynchronously
"""
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def send_lead_notification_email_async(self, lead_id, recipient_email, subscriber_id=None):
    """
    Send a lead notification email asynchronously.
    
    Args:
        lead_id: The ID of the Lead instance
        recipient_email: Email address to send to
        subscriber_id: Optional ID of the LeadsSubscriber instance
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        from leads.models import Lead, LeadsSubscriber
        
        # Get the lead instance
        lead = Lead.objects.select_related().prefetch_related('vehicles').get(id=lead_id)
        
        # Get subscriber if provided
        subscriber = None
        if subscriber_id:
            subscriber = LeadsSubscriber.objects.get(id=subscriber_id)
        
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
        
        # Update subscriber count if this was sent to a subscriber
        if subscriber:
            subscriber.number_of_leads_sent += 1
            subscriber.save()
            
        return True
        
    except Exception as e:
        logger.error(f"Failed to send lead notification email to {recipient_email}: {str(e)}")
        # This will trigger a retry due to autoretry_for
        raise e


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def send_welcome_email_async(self, lead_id):
    """
    Send a welcome email to a lead asynchronously.
    
    Args:
        lead_id: The ID of the Lead instance
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        from leads.models import Lead
        
        # Get the lead instance
        lead = Lead.objects.get(id=lead_id)
        
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
        logger.error(f"Failed to send welcome email to lead {lead_id}: {str(e)}")
        # This will trigger a retry due to autoretry_for
        raise e


@shared_task
def send_emails_to_subscribers_async(lead_id):
    """
    Send lead notifications to all active subscribers asynchronously.
    
    Args:
        lead_id: The ID of the Lead instance
    """
    try:
        from leads.models import LeadsSubscriber
        
        # Get all active subscribers
        active_subscribers = LeadsSubscriber.objects.filter(is_active=True)
        
        # Queue individual email tasks for each subscriber
        for subscriber in active_subscribers:
            send_lead_notification_email_async.delay(
                lead_id=lead_id,
                recipient_email=subscriber.email,
                subscriber_id=subscriber.id
            )
        
        logger.info(f"Queued lead notification emails for {active_subscribers.count()} subscribers for lead {lead_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to queue lead notification emails for lead {lead_id}: {str(e)}")
        return False
