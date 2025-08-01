#!/usr/bin/env python
"""
Test script to verify Celery and async email setup
"""
import os
import sys
import django

# Add the project to the Python path
sys.path.append('/home/siber/Dev/savedrivenow.com')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'savedrivenow.settings')
django.setup()

def test_celery_connection():
    """Test if Celery can connect to Redis"""
    try:
        from celery import current_app
        
        # Test broker connection
        conn = current_app.broker_connection()
        conn.ensure_connection(max_retries=3)
        print("✓ Celery broker connection successful!")
        return True
    except Exception as e:
        print(f"✗ Celery broker connection failed: {e}")
        print("Make sure Redis is running: redis-server")
        return False

def test_task_import():
    """Test if email tasks can be imported"""
    try:
        from leads.tasks import send_lead_notification_email_async, send_welcome_email_async
        print("✓ Email tasks imported successfully!")
        return True
    except Exception as e:
        print(f"✗ Failed to import email tasks: {e}")
        return False

def test_lead_with_vehicles():
    """Test creating a lead with vehicles and queueing email"""
    try:
        from leads.models import Lead, Vehicle, LeadsSubscriber
        from django.utils import timezone
        from datetime import date
        
        # Create a test subscriber if none exists
        subscriber, created = LeadsSubscriber.objects.get_or_create(
            email='test-subscriber@example.com',
            defaults={
                'number_of_leads_purchased': 10,
                'number_of_leads_sent': 0,
                'is_active': True
            }
        )
        if created:
            print("✓ Created test subscriber")
        else:
            print("✓ Using existing test subscriber")
        
        # Create a test lead
        lead = Lead.objects.create(
            full_name='Async Test User',
            address='123 Async St',
            city='Test City',
            state='CA',
            zip_code='90210',
            phone_number='+15551234567',
            email=f'async-test-{timezone.now().timestamp()}@example.com',
            birth_date=date(1990, 1, 1),
            tickets_past_year=0,
            accidents_past_year=0,
            is_homeowner=True
        )
        
        # Add vehicles
        Vehicle.objects.create(lead=lead, year=2020, make='Toyota', model='Camry')
        Vehicle.objects.create(lead=lead, year=2018, make='Honda', model='Civic')
        
        print(f"✓ Created test lead with {lead.vehicles.count()} vehicles")
        
        # Test async email queueing
        LeadsSubscriber.email_leads_to_active_subscribers(lead)
        print("✓ Queued async email tasks successfully!")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to test lead creation and email queueing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("Testing Async Email Setup")
    print("=" * 40)
    
    # Run tests
    celery_ok = test_celery_connection()
    tasks_ok = test_task_import()
    
    if celery_ok and tasks_ok:
        print("\n🎉 Basic setup looks good!")
        print("\nTesting lead creation and email queueing...")
        if test_lead_with_vehicles():
            print("\n🎉 All tests passed!")
            print("\nNext steps:")
            print("1. Start Redis: redis-server")
            print("2. Start Celery worker: ./start_celery_worker.sh")
            print("3. Create a lead through the web interface")
            print("4. Check worker logs to see email processing")
        else:
            print("\n❌ Lead/email test failed")
    else:
        print("\n❌ Setup issues detected. Please fix them before proceeding.")
        
    print("\n" + "=" * 40)
