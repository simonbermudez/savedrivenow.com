from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.conf import settings
from django.db import transaction
from django.forms import inlineformset_factory
from .models import Lead, Vehicle, LeadsSubscriber
from .forms import LeadForm, VehicleForm


class LeadListView(ListView):
    model = Lead
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 10

    def get_queryset(self):
        return Lead.objects.prefetch_related('vehicles').all().order_by('-created_at')


def lead_create_view(request):
    """Create a new lead with optional vehicle information"""
    # Create a formset for vehicles
    VehicleFormSet = inlineformset_factory(
        Lead, Vehicle, 
        form=VehicleForm, 
        extra=1, 
        can_delete=False,
        max_num=5  # Maximum 5 vehicles
    )
    
    if request.method == 'POST':
        print("POST request received")
        print("POST data:", request.POST)
        lead_form = LeadForm(request.POST)
        
        # Initialize formset without instance for creation
        vehicle_formset = VehicleFormSet(request.POST, prefix='vehicles')
        
        print("Lead form is valid:", lead_form.is_valid())
        print("Vehicle formset is valid:", vehicle_formset.is_valid())
        
        if not lead_form.is_valid():
            print("Lead form errors:", lead_form.errors)
        if not vehicle_formset.is_valid():
            print("Vehicle formset errors:", vehicle_formset.errors)
            print("Vehicle formset non form errors:", vehicle_formset.non_form_errors())
        
        # Lead form must be valid, vehicle formset validation is more flexible
        if lead_form.is_valid():
            try:
                with transaction.atomic():
                    # Save the lead first
                    lead = lead_form.save()
                    print(f"Lead saved: {lead}")
                    
                    # Process vehicle formset manually
                    saved_vehicles = 0
                    for i, form in enumerate(vehicle_formset.forms):
                        if form.is_valid() and not form.cleaned_data.get('DELETE', False):
                            # Check if any vehicle data is provided
                            year = form.cleaned_data.get('year')
                            make = form.cleaned_data.get('make')
                            model = form.cleaned_data.get('model')
                            
                            if year or make or model:
                                vehicle = form.save(commit=False)
                                vehicle.lead = lead
                                vehicle.save()
                                saved_vehicles += 1
                                print(f"Vehicle saved: {vehicle}")
                        elif not form.is_valid() and form.errors:
                            print(f"Vehicle form {i} errors:", form.errors)
                    
                    message = f'Lead "{lead.full_name}" has been created successfully!'
                    if saved_vehicles > 0:
                        message += f' {saved_vehicles} vehicle(s) added.'
                    
                    # Send notifications AFTER vehicles are saved
                    LeadsSubscriber.email_leads_to_active_subscribers(lead)
                    
                    # Optionally send welcome email to the lead (uncomment if desired)
                    # try:
                    #     from .tasks import send_welcome_email_async
                    #     send_welcome_email_async.delay(lead.id)
                    # except ImportError:
                    #     pass  # Skip welcome email if Celery not available
                    
                    messages.success(request, message)
                    return redirect('lead_list')
            except Exception as e:
                print("Error saving lead:", str(e))
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error creating lead: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        lead_form = LeadForm()
        vehicle_formset = VehicleFormSet(prefix='vehicles')
    
    context = {
        'lead_form': lead_form,
        'vehicle_formset': vehicle_formset,
        'google_places_api_key': settings.GOOGLE_PLACES_API_KEY,
        'turnstile_site_key': settings.TURNSTILE_SITE_KEY
    }
    return render(request, 'leads/landing.html', context)


def lead_detail_view(request, pk):
    """View details of a specific lead"""
    lead = get_object_or_404(Lead.objects.prefetch_related('vehicles'), pk=pk)
    return render(request, 'leads/lead_detail.html', {'lead': lead})


def lead_update_view(request, pk):
    """Update an existing lead"""
    lead = get_object_or_404(Lead.objects.prefetch_related('vehicles'), pk=pk)
    
    if request.method == 'POST':
        lead_form = LeadForm(request.POST, instance=lead)
        if lead_form.is_valid():
            try:
                lead = lead_form.save()
                messages.success(request, f'Lead "{lead.full_name}" has been updated successfully!')
                return redirect('lead_detail', pk=lead.pk)
            except Exception as e:
                messages.error(request, f'Error updating lead: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        lead_form = LeadForm(instance=lead)
    
    context = {
        'lead_form': lead_form,
        'lead': lead,
        'vehicles': lead.vehicles.all()
    }
    return render(request, 'leads/lead_update.html', context)


def lead_delete_view(request, pk):
    """Delete a lead"""
    lead = get_object_or_404(Lead, pk=pk)
    
    if request.method == 'POST':
        lead_name = lead.full_name
        lead.delete()
        messages.success(request, f'Lead "{lead_name}" has been deleted successfully!')
        return redirect('lead_list')
    
    return render(request, 'leads/lead_delete.html', {'lead': lead})


def vehicle_create_view(request, lead_pk):
    """Add a new vehicle to an existing lead"""
    lead = get_object_or_404(Lead, pk=lead_pk)
    
    if request.method == 'POST':
        vehicle_form = VehicleForm(request.POST)
        if vehicle_form.is_valid():
            try:
                vehicle = vehicle_form.save(commit=False)
                vehicle.lead = lead
                vehicle.save()
                messages.success(request, f'Vehicle "{vehicle}" has been added successfully!')
                return redirect('lead_detail', pk=lead.pk)
            except Exception as e:
                messages.error(request, f'Error adding vehicle: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        vehicle_form = VehicleForm()
    
    context = {
        'vehicle_form': vehicle_form,
        'lead': lead
    }
    return render(request, 'leads/vehicle_create.html', context)


def vehicle_update_view(request, pk):
    """Update an existing vehicle"""
    vehicle = get_object_or_404(Vehicle.objects.select_related('lead'), pk=pk)
    
    if request.method == 'POST':
        vehicle_form = VehicleForm(request.POST, instance=vehicle)
        if vehicle_form.is_valid():
            try:
                vehicle = vehicle_form.save()
                messages.success(request, f'Vehicle "{vehicle}" has been updated successfully!')
                return redirect('lead_detail', pk=vehicle.lead.pk)
            except Exception as e:
                messages.error(request, f'Error updating vehicle: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        vehicle_form = VehicleForm(instance=vehicle)
    
    context = {
        'vehicle_form': vehicle_form,
        'vehicle': vehicle,
        'lead': vehicle.lead
    }
    return render(request, 'leads/vehicle_update.html', context)


def vehicle_delete_view(request, pk):
    """Delete a vehicle"""
    vehicle = get_object_or_404(Vehicle.objects.select_related('lead'), pk=pk)
    lead = vehicle.lead
    
    if request.method == 'POST':
        vehicle_info = str(vehicle)
        vehicle.delete()
        messages.success(request, f'Vehicle "{vehicle_info}" has been deleted successfully!')
        return redirect('lead_detail', pk=lead.pk)
    
    context = {
        'vehicle': vehicle,
        'lead': lead
    }
    return render(request, 'leads/vehicle_delete.html', context)
