#!/usr/bin/env python
"""
Simple script to test email template rendering
"""
import os
import sys
import django
from datetime import date
from django.utils import timezone

# Add the project to the Python path
sys.path.append('/home/siber/Dev/savedrivenow.com')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'savedrivenow.settings')
django.setup()

from django.template.loader import render_to_string
from leads.models import Lead, Vehicle

# Create a sample lead for testing
sample_lead = Lead(
    pk=1,
    full_name="John Smith",
    address="123 Main Street",
    city="Springfield",
    state="IL",
    zip_code="62701",
    phone_number="+15551234567",
    email="john.smith@example.com",
    birth_date=date(1985, 5, 15),
    tickets_past_year=0,
    accidents_past_year=1,
    is_homeowner=True,
    created_at=timezone.now(),
    updated_at=timezone.now(),
)

# Test by actually saving to database temporarily
try:
    # Check if test lead exists
    existing_lead = Lead.objects.filter(email="test-john.smith@example.com").first()
    if existing_lead:
        sample_lead = existing_lead
        print("Using existing test lead")
    else:
        # Use a different email to avoid conflicts
        sample_lead.email = "test-john.smith@example.com"
        sample_lead.save()
        print("Created new test lead")
        
        # Create actual vehicle objects
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
        print("Created test vehicles")
        
except Exception as e:
    print(f"Could not create test data in database: {e}")
    # Fallback: modify the template context to include mock data
    sample_lead.pk = 1
    
    # For template testing, we'll create a simple namespace object
    class MockLead:
        def __init__(self, lead_data):
            for key, value in lead_data.__dict__.items():
                setattr(self, key, value)
            
        class MockVehiclesManager:
            def __init__(self):
                self._vehicles = [
                    type('Vehicle', (), {'year': 2020, 'make': 'Toyota', 'model': 'Camry'}),
                    type('Vehicle', (), {'year': 2018, 'make': 'Honda', 'model': 'Civic'})
                ]
            
            def all(self):
                return self._vehicles
            
            def count(self):
                return len(self._vehicles)
        
        vehicles = MockVehiclesManager()
    
    sample_lead = MockLead(sample_lead)

# Test template rendering
context = {
    'lead': sample_lead,
}

print("Testing email template rendering...")
print("=" * 50)

try:
    html_content = render_to_string('emails/new_lead_notification.html', context)
    print("✓ HTML template rendered successfully!")
    print(f"Template length: {len(html_content)} characters")
    
    # Check if vehicles appear in the rendered HTML
    if "Toyota" in html_content and "Camry" in html_content:
        print("✓ Vehicle information found in rendered HTML!")
    else:
        print("✗ Vehicle information NOT found in rendered HTML")
        
    # Search for specific vehicle-related content
    vehicle_keywords = ["Vehicle", "🚗", "Toyota", "Camry", "Honda", "Civic"]
    found_keywords = []
    for keyword in vehicle_keywords:
        if keyword in html_content:
            found_keywords.append(keyword)
    
    print(f"Found vehicle keywords: {found_keywords}")
    
    # Save the rendered HTML to a file for inspection
    with open('/home/siber/Dev/savedrivenow.com/test_email_output.html', 'w') as f:
        f.write(html_content)
    print("✓ Rendered HTML saved to test_email_output.html")
    
except Exception as e:
    print(f"✗ Error rendering template: {e}")
    import traceback
    traceback.print_exc()
