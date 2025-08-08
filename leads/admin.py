from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Lead, Vehicle, LeadsSubscriber, State

# Register your models here.

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'city', 'state', 'created_at', 'email_preview_link')
    list_filter = ('state', 'is_homeowner', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'city')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def email_preview_link(self, obj):
        """Add a link to preview the email template for this lead"""
        return format_html(
            '<a href="/admin/leads/lead/{}/email-preview/" target="_blank">📧 Preview Email</a>',
            obj.pk
        )
    email_preview_link.short_description = 'Email Preview'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:lead_id>/email-preview/', self.admin_site.admin_view(self.email_preview_view), name='lead_email_preview'),
        ]
        return custom_urls + urls
    
    def email_preview_view(self, request, lead_id):
        """View to preview the email template"""
        try:
            lead = Lead.objects.get(pk=lead_id)
            
            # Get the email type from query parameters
            email_type = request.GET.get('type', 'notification')
            
            if email_type == 'welcome':
                html_content = render_to_string('emails/welcome_email.html', {'lead': lead})
            else:
                html_content = render_to_string('emails/new_lead_notification.html', {'lead': lead})
            
            return HttpResponse(html_content)
        except Lead.DoesNotExist:
            return HttpResponse("Lead not found", status=404)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'lead', 'created_at')
    list_filter = ('make', 'year', 'created_at')
    search_fields = ('make', 'model', 'lead__full_name', 'lead__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(LeadsSubscriber)
class LeadsSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'get_states', 'number_of_leads_purchased', 'number_of_leads_sent', 'remaining_leads', 'is_active', 'created_at')
    list_filter = ('is_active', 'states', 'created_at', 'updated_at')
    search_fields = ('email',)
    readonly_fields = ('created_at', 'updated_at', 'remaining_leads', 'number_of_leads_sent', 'is_active')
    filter_horizontal = ('states',)  # This creates a nice multi-select widget
    ordering = ('-created_at',)
    
    def remaining_leads(self, obj):
        return obj.remaining_leads
    remaining_leads.short_description = 'Remaining Leads'
    
    def get_states(self, obj):
        """Display selected states in the list view"""
        states = obj.states.all()
        if states.exists():
            return ", ".join([f"{state.code}" for state in states])
        return "All States"
    get_states.short_description = 'States'


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('name',)
