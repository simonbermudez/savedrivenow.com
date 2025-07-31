from django.contrib import admin
from .models import Lead, Vehicle, LeadsSubscriber

# Register your models here.

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'city', 'state', 'created_at')
    list_filter = ('state', 'is_homeowner', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'city')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'lead', 'created_at')
    list_filter = ('make', 'year', 'created_at')
    search_fields = ('make', 'model', 'lead__full_name', 'lead__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(LeadsSubscriber)
class LeadsSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'number_of_leads_purchased', 'number_of_leads_sent', 'remaining_leads', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('email',)
    readonly_fields = ('created_at', 'updated_at', 'remaining_leads')
    ordering = ('-created_at',)
    
    def remaining_leads(self, obj):
        return obj.remaining_leads
    remaining_leads.short_description = 'Remaining Leads'
