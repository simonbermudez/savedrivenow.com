from django.urls import path
from . import views

urlpatterns = [
    # path('', views.LeadListView.as_view(), name='lead_list'),
    path('create/', views.lead_create_view, name='lead_create'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
    # path('<int:pk>/', views.lead_detail_view, name='lead_detail'),
    # path('<int:pk>/update/', views.lead_update_view, name='lead_update'),
    # path('<int:pk>/delete/', views.lead_delete_view, name='lead_delete'),
    
    # # Vehicle URLs
    # path('<int:lead_pk>/vehicle/create/', views.vehicle_create_view, name='vehicle_create'),
    # path('vehicle/<int:pk>/update/', views.vehicle_update_view, name='vehicle_update'),
    # path('vehicle/<int:pk>/delete/', views.vehicle_delete_view, name='vehicle_delete'),
]
