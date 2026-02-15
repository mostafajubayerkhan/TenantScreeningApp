from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('preview-buttons/', views.button_preview, name='button_preview'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rent-estimator/', views.rent_estimator, name='rent_estimator'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Tools
    path('rent-estimator/', views.rent_estimator, name='rent_estimator'),
    path('lease-generator/', views.lease_generate, name='lease_generate'),
    
    # Properties
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/create/', views.property_create, name='property_create'),
    
    # Applications
    path('applications/<int:property_pk>/apply/', views.application_create, name='application_create'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/review/', views.application_review, name='application_review'),
    path('application/<int:pk>/screening/', views.run_screening, name='run_screening'),
    path('screening/<int:pk>/', views.view_screening_report, name='view_screening_report'),
]
