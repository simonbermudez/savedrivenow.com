from django.urls import path
from . import views

urlpatterns = [
    path('', views.LeadListView.as_view(), name='lead_list'),
    path('create/', views.lead_create_view, name='lead_create'),
    path('<int:pk>/', views.lead_detail_view, name='lead_detail'),
    path('<int:pk>/update/', views.lead_update_view, name='lead_update'),
    path('<int:pk>/delete/', views.lead_delete_view, name='lead_delete'),
]
