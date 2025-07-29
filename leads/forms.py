from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'address', 'city', 'state', 'phone_number', 'email', 'birth_date']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            }),
            'state': forms.Select(attrs={
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required
        for field in self.fields.values():
            field.required = True
        
        # Add custom labels
        self.fields['full_name'].label = 'Full Name'
        self.fields['address'].label = 'Street Address'
        self.fields['city'].label = 'City'
        self.fields['state'].label = 'State'
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['email'].label = 'Email Address'
        self.fields['birth_date'].label = 'Date of Birth'
