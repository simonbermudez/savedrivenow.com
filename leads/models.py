from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re


class Vehicle(models.Model):
    """Model to store vehicle information for leads"""
    lead = models.ForeignKey(
        'Lead',
        on_delete=models.CASCADE,
        related_name='vehicles',
        help_text="The lead who owns this vehicle"
    )
    
    year = models.IntegerField(
        help_text="Year of the vehicle (e.g., 2020)"
    )
    
    make = models.CharField(
        max_length=50,
        help_text="Vehicle manufacturer (e.g., Toyota, Ford, Honda)"
    )
    
    model = models.CharField(
        max_length=50,
        help_text="Vehicle model (e.g., Camry, F-150, Civic)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class Lead(models.Model):
    # Phone number validator
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # ZIP code validator
    zip_regex = RegexValidator(
        regex=r'^\d{5}(-\d{4})?$',
        message="ZIP code must be in format: 12345 or 12345-6789"
    )

    # Full Name
    full_name = models.CharField(
        max_length=100,
        help_text="Full name of the lead"
    )

    # Address fields
    address = models.CharField(
        max_length=255,
        help_text="Street address"
    )
    
    city = models.CharField(
        max_length=100,
        help_text="City name"
    )
    
    state = models.CharField(
        max_length=2,
        help_text="Select a state"
    )
    
    zip_code = models.CharField(
        max_length=10,
        validators=[zip_regex],
        help_text="ZIP code (e.g., 12345 or 12345-6789)"
    )

    # Phone Number with validation
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        help_text="Phone number in format: +1234567890"
    )

    # Email with built-in validation
    email = models.EmailField(
        unique=True,
        help_text="Valid email address"
    )

    # Birth Date
    birth_date = models.DateField(
        help_text="Date of birth (YYYY-MM-DD)"
    )

    # Driving history
    tickets_past_year = models.IntegerField(
        default=0,
        help_text="Number of traffic tickets received in the past year"
    )

    accidents_past_year = models.IntegerField(
        default=0,
        help_text="Number of accidents in the past year"
    )

    # Property ownership
    is_homeowner = models.BooleanField(
        default=False,
        help_text="Is the lead a homeowner?"
    )

    # Metadata fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    def clean(self):
        """Custom validation method"""
        super().clean()
        
        # Validate email format (additional validation)
        if self.email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email):
                raise ValidationError({'email': 'Enter a valid email address.'})
        
        # Validate birth date (ensure it's not in the future)
        from django.utils import timezone
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError({'birth_date': 'Birth date cannot be in the future.'})

    def save(self, *args, **kwargs):
        """Override save method to run full_clean"""
        self.full_clean()
        LeadsSubscriber.email_leads_to_active_subscribers(self)
        super().save(*args, **kwargs)


class LeadsSubscriber(models.Model):
    """Model to track subscribers who receive leads via email"""
    
    email = models.EmailField(
        unique=True,
        help_text="Email address of the subscriber who receives leads"
    )
    
    number_of_leads_purchased = models.PositiveIntegerField(
        default=0,
        help_text="Total number of leads purchased by this subscriber"
    )
    
    number_of_leads_sent = models.PositiveIntegerField(
        default=0,
        help_text="Total number of leads sent to this subscriber"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Is the subscriber currently active?"
    )
    
    # Metadata fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Leads Subscriber"
        verbose_name_plural = "Leads Subscribers"
    
    def __str__(self):
        return f"{self.email} - Purchased: {self.number_of_leads_purchased}, Sent: {self.number_of_leads_sent}"
    
    def clean(self):
        """Custom validation method"""
        super().clean()
        
        # Validate email format (additional validation)
        if self.email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email):
                raise ValidationError({'email': 'Enter a valid email address.'})
        
        # Validate that number_of_leads_sent doesn't exceed number_of_leads_purchased
        if self.number_of_leads_sent > self.number_of_leads_purchased:
            raise ValidationError({
                'number_of_leads_sent': 'Number of leads sent cannot exceed number of leads purchased.'
            })
    
    def save(self, *args, **kwargs):
        """Override save method to run full_clean"""
        self.full_clean()
        self.is_active = self.can_receive_lead()
        super().save(*args, **kwargs)
    
    @property
    def remaining_leads(self):
        """Calculate the number of remaining leads"""
        return self.number_of_leads_purchased - self.number_of_leads_sent
    
    def can_receive_lead(self):
        """Check if subscriber can receive another lead"""
        return self.remaining_leads > 0

    @classmethod
    def email_leads_to_active_subscribers(cls, lead):
        """Send lead information to all active subscribers"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        active_subscribers = cls.objects.filter(is_active=True)
        
        for subscriber in active_subscribers:
            send_mail(
                subject=f"New Lead: {lead.full_name}",
                message=f"New lead details:\n\n{lead}\n\nContact them at {lead.email} or {lead.phone_number}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
            )
            subscriber.number_of_leads_sent += 1
            subscriber.save()
