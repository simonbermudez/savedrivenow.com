import requests
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError


class TurnstileWidget(forms.Widget):
    """Widget for rendering Cloudflare Turnstile CAPTCHA"""
    
    def __init__(self, attrs=None):
        self.site_key = getattr(settings, 'TURNSTILE_SITE_KEY', '')
        super().__init__(attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        """Render the Turnstile widget"""
        if attrs is None:
            attrs = {}
        
        attrs.update({
            'class': 'cf-turnstile',
            'data-sitekey': self.site_key,
            'data-theme': 'light',
            'data-size': 'normal',
        })
        
        return f'<div class="cf-turnstile" data-sitekey="{self.site_key}" data-theme="light"></div>'


class TurnstileField(forms.CharField):
    """Form field for Cloudflare Turnstile CAPTCHA"""
    
    widget = TurnstileWidget
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', True)
        kwargs.setdefault('label', '')
        # Don't show this field in the form rendering since we handle it manually
        kwargs.setdefault('widget', TurnstileWidget())
        super().__init__(*args, **kwargs)
    
    def clean(self, value):
        """Clean and validate the Turnstile response"""
        # Get the cleaned value from parent
        value = super().clean(value)
        
        if not value:
            raise ValidationError('CAPTCHA verification is required.')
        
        # Verify the token with Cloudflare
        secret_key = getattr(settings, 'TURNSTILE_SECRET_KEY', '')
        
        data = {
            'secret': secret_key,
            'response': value,
        }
        
        try:
            response = requests.post(
                'https://challenges.cloudflare.com/turnstile/v0/siteverify',
                data=data,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if not result.get('success', False):
                error_codes = result.get('error-codes', [])
                if 'timeout-or-duplicate' in error_codes:
                    raise ValidationError('CAPTCHA has expired. Please try again.')
                elif 'invalid-input-response' in error_codes:
                    raise ValidationError('Invalid CAPTCHA response. Please try again.')
                else:
                    raise ValidationError('CAPTCHA verification failed. Please try again.')
                    
        except requests.RequestException:
            raise ValidationError('CAPTCHA verification failed. Please try again.')
        
        return value
    
    def widget_attrs(self, widget):
        """Add additional attributes to the widget"""
        attrs = super().widget_attrs(widget)
        attrs.update({
            'data-sitekey': getattr(settings, 'TURNSTILE_SITE_KEY', ''),
        })
        return attrs
