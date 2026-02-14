from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Property, RentalApplication


class UserRegistrationForm(UserCreationForm):
    """User registration form with role selection"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'


class PropertyForm(forms.ModelForm):
    """Property creation/edit form"""
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'address', 'city', 'state', 'zip_code',
            'bedrooms', 'bathrooms', 'square_feet', 'monthly_rent',
            'security_deposit', 'status', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-textarea'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-file'
            else:
                field.widget.attrs['class'] = 'form-input'


class RentalApplicationForm(forms.ModelForm):
    """Rental application form"""
    class Meta:
        model = RentalApplication
        fields = [
            'current_address', 'move_in_date', 'employer_name', 'job_title',
            'annual_income', 'employment_duration', 'number_of_occupants',
            'has_pets', 'pet_details', 'additional_notes'
        ]
        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
            'pet_details': forms.Textarea(attrs={'rows': 3}),
            'additional_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-textarea'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-checkbox'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-input'
