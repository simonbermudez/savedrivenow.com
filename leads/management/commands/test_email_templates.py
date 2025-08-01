"""
Management command to test email templates with sample data.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from leads.models import Lead, LeadsSubscriber
from leads.email_utils import send_lead_notification_email, send_welcome_email
import datetime


class Command(BaseCommand):
    help = 'Test email templates with sample lead data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-email',
            type=str,
            help='Email address to send test emails to',
            default='test@example.com'
        )
        parser.add_argument(
            '--send-notification',
            action='store_true',
            help='Send lead notification email'
        )
        parser.add_argument(
            '--send-welcome',
            action='store_true',
            help='Send welcome email'
        )

    def handle(self, *args, **options):
        # Create a sample lead for testing
        sample_lead = Lead(
            full_name="John Smith",
            address="123 Main Street",
            city="Springfield",
            state="IL",
            zip_code="62701",
            phone_number="+15551234567",
            email="john.smith@example.com",
            birth_date=datetime.date(1985, 5, 15),
            tickets_past_year=0,
            accidents_past_year=1,
            is_homeowner=True,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        
        # Set a fake primary key for template rendering
        sample_lead.pk = 1
        
        # We need to temporarily save the lead to create vehicles
        try:
            # Check if a test lead already exists
            existing_lead = Lead.objects.filter(email="john.smith@example.com").first()
            if existing_lead:
                sample_lead = existing_lead
                self.stdout.write("Using existing test lead")
            else:
                sample_lead.save()
                self.stdout.write("Created new test lead")
                
            # Add some test vehicles if they don't exist
            from leads.models import Vehicle
            if not sample_lead.vehicles.exists():
                Vehicle.objects.create(
                    lead=sample_lead,
                    year=2020,
                    make="Toyota",
                    model="Camry"
                )
                Vehicle.objects.create(
                    lead=sample_lead,
                    year=2018,
                    make="Honda",
                    model="Civic"
                )
                self.stdout.write("Added test vehicles")
                
        except Exception as e:
            self.stdout.write(f"Note: Could not save test lead to database: {e}")
            self.stdout.write("Proceeding with in-memory lead for email template testing")
        
        test_email = options['test_email']
        
        self.stdout.write(
            self.style.SUCCESS(f'Testing email templates with sample lead data...')
        )
        self.stdout.write(f'Test email will be sent to: {test_email}')
        
        if options['send_notification'] or (not options['send_notification'] and not options['send_welcome']):
            self.stdout.write('\nSending lead notification email...')
            success = send_lead_notification_email(
                lead=sample_lead,
                recipient_email=test_email
            )
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✓ Lead notification email sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('✗ Failed to send lead notification email')
                )
        
        if options['send_welcome'] or (not options['send_notification'] and not options['send_welcome']):
            self.stdout.write('\nSending welcome email...')
            
            # Temporarily change the lead's email to the test email
            original_email = sample_lead.email
            sample_lead.email = test_email
            
            success = send_welcome_email(lead=sample_lead)
            
            # Restore original email
            sample_lead.email = original_email
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✓ Welcome email sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('✗ Failed to send welcome email')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\nEmail template testing completed!')
        )
        self.stdout.write('Check your email inbox to see the beautiful templates.')
