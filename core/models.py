from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Custom user model with role support"""
    ROLE_CHOICES = [
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Property(models.Model):
    """Rental property listing"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('rented', 'Rented'),
    ]
    
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    bedrooms = models.IntegerField(validators=[MinValueValidator(0)])
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0)])
    square_feet = models.IntegerField(validators=[MinValueValidator(1)])
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.city}, {self.state}"


class RentalApplication(models.Model):
    """Tenant application for a property"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='applications')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    
    # Personal Information
    current_address = models.CharField(max_length=300)
    move_in_date = models.DateField()
    
    # Employment Information
    employer_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    employment_duration = models.CharField(max_length=50)
    
    # Additional Information
    number_of_occupants = models.IntegerField(validators=[MinValueValidator(1)])
    has_pets = models.BooleanField(default=False)
    pet_details = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    
    # Status & Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['property', 'tenant']
    
    def __str__(self):
        return f"Application by {self.tenant.username} for {self.property.title}"


class ScreeningReport(models.Model):
    """Background and credit screening report"""
    CREDIT_SCORE_CHOICES = [
        ('excellent', 'Excellent (750+)'),
        ('good', 'Good (700-749)'),
        ('fair', 'Fair (650-699)'),
        ('poor', 'Poor (Below 650)'),
    ]
    
    application = models.OneToOneField(RentalApplication, on_delete=models.CASCADE, related_name='screening')
    
    # Credit Check (Simulated)
    credit_score_range = models.CharField(max_length=20, choices=CREDIT_SCORE_CHOICES)
    
    # Background Check (Simulated)
    criminal_record_clear = models.BooleanField(default=True)
    eviction_history_clear = models.BooleanField(default=True)
    
    # Verification
    employment_verified = models.BooleanField(default=False)
    income_verified = models.BooleanField(default=False)
    references_verified = models.BooleanField(default=False)
    
    # Overall Assessment
    recommendation = models.TextField(blank=True)
    risk_level = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='low'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Screening for {self.application.tenant.username}"


class LeaseDocument(models.Model):
    """Lease agreement document"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent for Signature'),
        ('signed_tenant', 'Signed by Tenant'),
        ('signed_both', 'Fully Executed'),
        ('terminated', 'Terminated'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='leases')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leases')
    
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    
    document_file = models.FileField(upload_to='leases/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    special_terms = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    signed_by_tenant_at = models.DateTimeField(null=True, blank=True)
    signed_by_landlord_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Lease for {self.property.title} - {self.tenant.username}"


class Message(models.Model):
    """Messages between landlord and tenant"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    
    subject = models.CharField(max_length=200)
    body = models.TextField()
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"
