from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'address', 'city', 'state', 'phone_number', 'email', 'birth_date', 'vehicle_year', 'vehicle_make', 'vehicle_model']
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
            'state': forms.Select(attrs={
                'class': 'form-control'
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
        required_fields = ['full_name', 'address', 'city', 'state', 'phone_number', 'email', 'birth_date']
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
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['email'].label = 'Email Address'
        self.fields['birth_date'].label = 'Date of Birth'
        self.fields['vehicle_year'].label = 'Vehicle Year'
        self.fields['vehicle_make'].label = 'Vehicle Make'
        self.fields['vehicle_model'].label = 'Vehicle Model'
