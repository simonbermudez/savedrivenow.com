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
        super().save(*args, **kwargs)
