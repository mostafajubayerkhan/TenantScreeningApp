from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import User, Property, RentalApplication, ScreeningReport, LeaseDocument, Message
from .forms import UserRegistrationForm, PropertyForm, RentalApplicationForm


def home(request):
    """Landing page"""
    properties = Property.objects.filter(status='available')[:6]
    context = {
        'properties': properties,
    }
    return render(request, 'home.html', context)


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to TenantScreening.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """Dashboard - different views for Landlord vs Tenant"""
    user = request.user
    
    if user.role == 'landlord':
        # Landlord Dashboard
        properties = Property.objects.filter(landlord=user)
        applications = RentalApplication.objects.filter(property__landlord=user).select_related('property', 'tenant')
        recent_messages = Message.objects.filter(recipient=user)[:5]
        
        context = {
            'properties': properties,
            'applications': applications,
            'recent_messages': recent_messages,
            'total_properties': properties.count(),
            'pending_applications': applications.filter(status='pending').count(),
        }
        return render(request, 'dashboard/landlord_dashboard.html', context)
    else:
        # Tenant Dashboard
        applications = RentalApplication.objects.filter(tenant=user).select_related('property')
        leases = LeaseDocument.objects.filter(tenant=user).select_related('property')
        recent_messages = Message.objects.filter(recipient=user)[:5]
        
        context = {
            'applications': applications,
            'leases': leases,
            'recent_messages': recent_messages,
        }
        return render(request, 'dashboard/tenant_dashboard.html', context)


@login_required
def property_list(request):
    """List all available properties"""
    properties = Property.objects.filter(status='available').select_related('landlord')
    
    # Search and filter
    search_query = request.GET.get('search', '')
    city = request.GET.get('city', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    bedrooms = request.GET.get('bedrooms', '')
    
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    if city:
        properties = properties.filter(city__icontains=city)
    
    if min_price:
        properties = properties.filter(monthly_rent__gte=min_price)
    
    if max_price:
        properties = properties.filter(monthly_rent__lte=max_price)
    
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)
    
    context = {
        'properties': properties,
        'search_query': search_query,
    }
    return render(request, 'properties/property_list.html', context)


@login_required
def property_detail(request, pk):
    """Property detail page"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    # Check if user already applied
    has_applied = False
    if request.user.role == 'tenant':
        has_applied = RentalApplication.objects.filter(
            property=property_obj,
            tenant=request.user
        ).exists()
    
    context = {
        'property': property_obj,
        'has_applied': has_applied,
    }
    return render(request, 'properties/property_detail.html', context)


@login_required
def property_create(request):
    """Create new property (Landlord only)"""
    if request.user.role != 'landlord':
        messages.error(request, 'Only landlords can create property listings.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.landlord = request.user
            property_obj.save()
            messages.success(request, 'Property listed successfully!')
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm()
    
    return render(request, 'properties/property_form.html', {'form': form})


@login_required
def application_create(request, property_pk):
    """Create rental application (Tenant only)"""
    if request.user.role != 'tenant':
        messages.error(request, 'Only tenants can submit applications.')
        return redirect('dashboard')
    
    property_obj = get_object_or_404(Property, pk=property_pk)
    
    # Check if already applied
    if RentalApplication.objects.filter(property=property_obj, tenant=request.user).exists():
        messages.warning(request, 'You have already applied for this property.')
        return redirect('property_detail', pk=property_pk)
    
    if request.method == 'POST':
        form = RentalApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.property = property_obj
            application.tenant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('dashboard')
    else:
        form = RentalApplicationForm()
    
    context = {
        'form': form,
        'property': property_obj,
    }
    return render(request, 'applications/application_form.html', context)


@login_required
def application_detail(request, pk):
    """View application details"""
    application = get_object_or_404(RentalApplication, pk=pk)
    
    # Check permissions
    if request.user != application.tenant and request.user != application.property.landlord:
        messages.error(request, 'You do not have permission to view this application.')
        return redirect('dashboard')
    
    # Get screening report if exists
    screening = None
    try:
        screening = application.screening
    except ScreeningReport.DoesNotExist:
        pass
    
    context = {
        'application': application,
        'screening': screening,
    }
    return render(request, 'applications/application_detail.html', context)


@login_required
def application_review(request, pk):
    """Review and update application status (Landlord only)"""
    application = get_object_or_404(RentalApplication, pk=pk)
    
    if request.user != application.property.landlord:
        messages.error(request, 'You do not have permission to review this application.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['approved', 'rejected', 'under_review']:
            application.status = status
            application.reviewed_at = timezone.now()
            application.save()
            
            messages.success(request, f'Application {status} successfully.')
            return redirect('application_detail', pk=pk)
    
    return redirect('application_detail', pk=pk)
