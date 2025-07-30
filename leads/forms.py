from django import forms
from django.core.validators import RegexValidator
from .models import Lead
from .turnstile import TurnstileField


class LeadForm(forms.ModelForm):
    # Add CAPTCHA field
    captcha = TurnstileField()
    
    class Meta:
        model = Lead
        fields = ['full_name', 'address', 'city', 'state', 'zip_code', 'phone_number', 'email', 'birth_date', 'vehicle_year', 'vehicle_make', 'vehicle_model']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ZIP code'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(555) 123-4567'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'mm/dd/yyyy'
            }),
            'vehicle_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2020',
                'min': '1900',
                'max': '2025'
            }),
            'vehicle_make': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Toyota, Ford, Honda'
            }),
            'vehicle_model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Camry, F-150, Civic'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make most fields required, but vehicle fields optional
        required_fields = ['full_name', 'address', 'city', 'state', 'zip_code', 'phone_number', 'email', 'birth_date']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
        
        # Vehicle fields are optional
        optional_fields = ['vehicle_year', 'vehicle_make', 'vehicle_model']
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False
        
        # Add custom labels
        self.fields['full_name'].label = 'Full Name'
        self.fields['address'].label = 'Street Address'
        self.fields['city'].label = 'City'
        self.fields['state'].label = 'State'
        self.fields['zip_code'].label = 'ZIP Code'
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['email'].label = 'Email Address'
        self.fields['birth_date'].label = 'Date of Birth'
        self.fields['vehicle_year'].label = 'Vehicle Year'
        self.fields['vehicle_make'].label = 'Vehicle Make'
        self.fields['vehicle_model'].label = 'Vehicle Model'

    def clean_zip_code(self):
        """Validate ZIP code format"""
        zip_code = self.cleaned_data.get('zip_code')
        if zip_code:
            # Remove any spaces and validate format
            zip_code = zip_code.replace(' ', '')
            zip_validator = RegexValidator(
                regex=r'^\d{5}(-\d{4})?$',
                message="Enter a valid ZIP code (e.g., 12345 or 12345-6789)"
            )
            zip_validator(zip_code)
        return zip_code

    def clean_address(self):
        """Validate street address"""
        address = self.cleaned_data.get('address')
        if address:
            address = address.strip()
            if len(address) < 5:
                raise forms.ValidationError("Please enter a complete street address.")
        return address

    def clean_city(self):
        """Validate city name"""
        city = self.cleaned_data.get('city')
        if city:
            city = city.strip().title()
            if len(city) < 2:
                raise forms.ValidationError("Please enter a valid city name.")
        return city
