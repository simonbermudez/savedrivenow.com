from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re


class Lead(models.Model):
    # Choices for states
    STATE_CHOICES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
    ]

    # Phone number validator
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
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
        choices=STATE_CHOICES,
        help_text="Select a state"
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
