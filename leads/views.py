from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.conf import settings
from .models import Lead
from .forms import LeadForm


class LeadListView(ListView):
    model = Lead
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 10

    def get_queryset(self):
        return Lead.objects.all().order_by('-created_at')


def lead_create_view(request):
    """Create a new lead"""
    if request.method == 'POST':
        print("POST request received")
        print("POST data:", request.POST)
        form = LeadForm(request.POST)
        print("Form is valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)
        if form.is_valid():
            try:
                lead = form.save()
                messages.success(request, f'Lead "{lead.full_name}" has been created successfully!')
                return redirect('lead_list')
            except Exception as e:
                print("Error saving lead:", str(e))
                messages.error(request, f'Error creating lead: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LeadForm()
    
    context = {
        'form': form,
        'google_places_api_key': settings.GOOGLE_PLACES_API_KEY,
        'turnstile_site_key': settings.TURNSTILE_SITE_KEY
    }
    return render(request, 'leads/landing.html', context)


def lead_detail_view(request, pk):
    """View details of a specific lead"""
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'leads/lead_detail.html', {'lead': lead})


def lead_update_view(request, pk):
    """Update an existing lead"""
    lead = get_object_or_404(Lead, pk=pk)
    
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            try:
                lead = form.save()
                messages.success(request, f'Lead "{lead.full_name}" has been updated successfully!')
                return redirect('lead_detail', pk=lead.pk)
            except Exception as e:
                messages.error(request, f'Error updating lead: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LeadForm(instance=lead)
    
    return render(request, 'leads/lead_update.html', {'form': form, 'lead': lead})


def lead_delete_view(request, pk):
    """Delete a lead"""
    lead = get_object_or_404(Lead, pk=pk)
    
    if request.method == 'POST':
        lead_name = lead.full_name
        lead.delete()
        messages.success(request, f'Lead "{lead_name}" has been deleted successfully!')
        return redirect('lead_list')
    
    return render(request, 'leads/lead_delete.html', {'lead': lead})
