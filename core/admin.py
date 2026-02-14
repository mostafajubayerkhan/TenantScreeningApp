from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Property, RentalApplication, ScreeningReport, LeaseDocument, Message


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin"""
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'profile_picture')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number')}),
    )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'landlord', 'city', 'state', 'monthly_rent', 'status', 'created_at']
    list_filter = ['status', 'city', 'state', 'created_at']
    search_fields = ['title', 'address', 'city', 'landlord__username']
    ordering = ['-created_at']


@admin.register(RentalApplication)
class RentalApplicationAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'property', 'status', 'annual_income', 'submitted_at']
    list_filter = ['status', 'submitted_at', 'has_pets']
    search_fields = ['tenant__username', 'property__title', 'employer_name']
    ordering = ['-submitted_at']
    readonly_fields = ['submitted_at', 'updated_at']


@admin.register(ScreeningReport)
class ScreeningReportAdmin(admin.ModelAdmin):
    list_display = ['application', 'credit_score_range', 'risk_level', 'created_at']
    list_filter = ['credit_score_range', 'risk_level', 'criminal_record_clear']
    search_fields = ['application__tenant__username']
    ordering = ['-created_at']


@admin.register(LeaseDocument)
class LeaseDocumentAdmin(admin.ModelAdmin):
    list_display = ['property', 'tenant', 'lease_start_date', 'lease_end_date', 'status', 'monthly_rent']
    list_filter = ['status', 'lease_start_date', 'lease_end_date']
    search_fields = ['property__title', 'tenant__username']
    ordering = ['-created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'subject', 'body']
    ordering = ['-created_at']
