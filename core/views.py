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


def button_preview(request):
    """Preview page for button styles"""
    return render(request, 'button_preview.html')


def rent_estimator(request):
    """Market Rent Estimator View"""
    result = None
    if request.method == "POST":
        # Get data
        zip_code = request.POST.get('zip_code')
        beds = int(request.POST.get('bedrooms', 1))
        baths = float(request.POST.get('bathrooms', 1))
        has_parking = request.POST.get('has_parking') == 'true'
        has_pool = request.POST.get('has_pool') == 'true'
        has_gym = request.POST.get('has_gym') == 'true'

        # MVP Algorithm
        base_rent = 1000  # Base for studio
        
        # Adjust for Beds/Baths
        base_rent += (beds * 400)
        base_rent += (baths * 200)

        # Adjust for Amenities
        if has_parking: base_rent += 150
        if has_pool: base_rent += 100
        if has_gym: base_rent += 100

        # Location Multiplier (Simulated)
        if zip_code and zip_code.startswith('9'): # West Coast Premium
            base_rent *= 1.2
        elif zip_code and zip_code.startswith('1'): # East Coast Premium
            base_rent *= 1.15

        optimal = int(base_rent)
        result = {
            'optimal_price': f"{optimal:,}",
            'low_range': f"{int(optimal * 0.9):,}",
            'high_range': f"{int(optimal * 1.1):,}",
        }

    return render(request, 'rent_estimator.html', {'result': result})


@login_required
def lease_generate(request):
    """Generate Lease Agreement View"""
    if request.user.role != 'landlord':
        messages.error(request, "Only Landlords can generate leases.")
        return redirect('dashboard')

    if request.method == 'POST':
        # Collect data from form
        data = {
            'address': request.POST.get('address'),
            'city_state_zip': request.POST.get('city_state_zip'),
            'landlord_name': request.POST.get('landlord_name'),
            'tenant_name': request.POST.get('tenant_name'),
            'start_date': request.POST.get('start_date'),
            'end_date': request.POST.get('end_date'),
            'rent_amount': request.POST.get('rent_amount'),
            'deposit_amount': request.POST.get('deposit_amount'),
            'late_fee': request.POST.get('late_fee'),
            'pets_allowed': request.POST.get('pets_allowed'),
            'utilities': request.POST.getlist('utilities'),
            'special_conditions': request.POST.get('special_conditions'),
        }
        return render(request, 'leases/lease_preview.html', {'data': data})

    return render(request, 'leases/lease_form.html')


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
        
        # Analytics
        total_views = sum(p.views for p in properties)
        
        # Trust Score Distribution
        apps = applications.select_related('tenant')
        gold = sum(1 for a in apps if a.tenant.trust_badge == 'gold')
        silver = sum(1 for a in apps if a.tenant.trust_badge == 'silver')
        bronze = sum(1 for a in apps if a.tenant.trust_badge == 'bronze')
        unranked = sum(1 for a in apps if a.tenant.trust_badge == 'unranked')

        context = {
            'properties': properties,
            'applications': applications,
            'recent_messages': recent_messages,
            'total_properties': properties.count(),
            'pending_applications': applications.filter(status='pending').count(),
            'total_views': total_views,
            'applications_gold': gold,
            'applications_silver': silver,
            'applications_bronze': bronze,
            'applications_unranked': unranked,
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
            'trust_score': user.calculate_trust_score(),
            'trust_badge': user.trust_badge,
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
    
    # Increment views
    property_obj.views += 1
    property_obj.save()
    
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


@login_required
def run_screening(request, pk):
    """Mock Screening Process (Payment + API Call)"""
    application = get_object_or_404(RentalApplication, pk=pk)
    
    if request.user != application.property.landlord:
        messages.error(request, 'Unauthorized.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        # 1. Simulate Payment ($30)
        # In real app: stripe.Charge.create(...)
        pass 

        # 2. Simulate API Call (TransUnion/Checkr)
        import random
        # Deterministic mock 
        score_val = random.randint(700, 820)
        if score_val >= 750: score_range = 'excellent'
        elif score_val >= 700: score_range = 'good'
        elif score_val >= 650: score_range = 'fair'
        else: score_range = 'poor'

        # Create Report
        ScreeningReport.objects.create(
            application=application,
            credit_score_range=score_range,
            criminal_record_clear=True, 
            eviction_history_clear=True,
            employment_verified=True,
            income_verified=True,
            recommendation="Accept" if score_val > 650 else "Conditional",
            risk_level='low' if score_val > 700 else 'medium'
        )
        
        messages.success(request, 'Screening Report Generated Successfully! ($30 charged)')
        return redirect('application_detail', pk=pk)
    
    return redirect('dashboard')


@login_required
def view_screening_report(request, pk):
    """View detailed screening report"""
    screening = get_object_or_404(ScreeningReport, pk=pk)
    
    # Permissions
    if request.user != screening.application.property.landlord:
        messages.error(request, 'Unauthorized.')
        return redirect('dashboard')
        
    return render(request, 'applications/screening_report.html', {'screening': screening})
