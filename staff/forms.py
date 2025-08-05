from django import forms
from .models import OfficeVisit, ClientVisit, OnlineClassInquiry, CollegeVisit
import re

# ------------------------
# Office Visit Form
# ------------------------
from django import forms
from .models import OfficeVisit

class OfficeVisitForm(forms.ModelForm):
    # Override the default date field to use a hidden input
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), error_messages={
        'required': 'Date is required.',
        'invalid': 'Please enter a valid date in YYYY-MM-DD format.'
    })
    
    class Meta:
        model = OfficeVisit
        fields = ['name', 'contact', 'email', 'address', 'purpose', 'date']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise forms.ValidationError("Date is required.")
        return date
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            return email  # Let Django handle required validation if blank

        # Convert to lowercase for consistent validation
        email = email.lower()

        # Check if email already exists, excluding current instance if editing
        queryset = OfficeVisit.objects.filter(email=email)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError("Email already exists. Please use a different email address.")

        return email

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if contact:
            # Validate contact is digits only
            if not contact.isdigit():
                raise forms.ValidationError("Contact must contain numbers only.")
            
            # Validate contact length (max 15 characters)
            if len(contact) > 15:
                raise forms.ValidationError("Contact number must not exceed 15 digits.")
            
            # Validate minimum length
            if len(contact) < 10:
                raise forms.ValidationError("Contact number must be at least 10 digits.")
            
            # Check if contact already exists, excluding current instance if editing
            queryset = OfficeVisit.objects.filter(contact=contact)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError("Contact number already exists.")
        else:
            raise forms.ValidationError("Contact number is required.")
            
        return contact

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if re.search(r'\d|@', name):
                raise forms.ValidationError("Name must contain only letters.")
        return name

# ------------------------
# Client Visit Form
# ------------------------
class ClientVisitForm(forms.ModelForm):
    # Override the default date field to use a hidden input with backend validation
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), error_messages={
        'required': 'Date is required.',
        'invalid': 'Please enter a valid date in YYYY-MM-DD format.'
    })
    
    class Meta:
        model = ClientVisit
        fields = ['name', 'contact_number', 'purpose', 'date']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise forms.ValidationError("Date is required.")
        return date
        
    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if contact:
            # Validate contact is digits only
            if not contact.isdigit():
                raise forms.ValidationError("Contact must contain numbers only.")
            
            # Validate contact length (max 15 characters)
            if len(contact) > 15:
                raise forms.ValidationError("Contact number must not exceed 15 digits.")
            
            # Validate minimum length
            if len(contact) < 10:
                raise forms.ValidationError("Contact number must be at least 10 digits.")
            
            # Check if contact already exists, excluding current instance if editing
            queryset = ClientVisit.objects.filter(contact_number=contact)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError("Contact number already exists.")
        else:
            raise forms.ValidationError("Contact number is required.")
            
        return contact

# ------------------------
# Online Class Inquiry Form
# ------------------------
class OnlineClassInquiryForm(forms.ModelForm):
    # Override the default date field to use a hidden input with backend validation
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), error_messages={
        'required': 'Date is required.',
        'invalid': 'Please enter a valid date in YYYY-MM-DD format.'
    })
    
    class Meta:
        model = OnlineClassInquiry
        fields = ['name', 'contact', 'purpose', 'date']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise forms.ValidationError("Date is required.")
        return date

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if contact:
            # Validate contact is digits only
            if not contact.isdigit():
                raise forms.ValidationError("Contact must contain numbers only.")
            
            # Validate contact length (max 15 characters)
            if len(contact) > 15:
                raise forms.ValidationError("Contact number must not exceed 15 digits.")
            
            # Validate minimum length
            if len(contact) < 10:
                raise forms.ValidationError("Contact number must be at least 10 digits.")
            
            # Check if contact already exists, excluding current instance if editing
            queryset = OnlineClassInquiry.objects.filter(contact=contact)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError("Contact number already exists.")
        else:
            raise forms.ValidationError("Contact number is required.")
            
        return contact

# ------------------------
# College Visit Form
# ------------------------
class CollegeVisitForm(forms.ModelForm):
    # Override the default date field to use a hidden input with backend validation
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), error_messages={
        'required': 'Date is required.',
        'invalid': 'Please enter a valid date in YYYY-MM-DD format.'
    })
    
    class Meta:
        model = CollegeVisit
        fields = ['name', 'contact', 'person_name', 'purpose', 'date']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise forms.ValidationError("Date is required.")
        return date

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if contact:
            # Validate contact is digits only
            if not contact.isdigit():
                raise forms.ValidationError("Contact must contain numbers only.")
            
            # Validate contact length (max 15 characters)
            if len(contact) > 15:
                raise forms.ValidationError("Contact number must not exceed 15 digits.")
            
            # Validate minimum length
            if len(contact) < 10:
                raise forms.ValidationError("Contact number must be at least 10 digits.")
            
            # Check if contact already exists, excluding current instance if editing
            queryset = CollegeVisit.objects.filter(contact=contact)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError("Contact number already exists.")
        else:
            raise forms.ValidationError("Contact number is required.")
            
        return contact

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if re.search(r'\d|@', name):
                raise forms.ValidationError("Name must contain only letters.")
        return name

    def clean_person_name(self):
        person_name = self.cleaned_data.get('person_name')
        if person_name:
            if re.search(r'\d|@', person_name):
                raise forms.ValidationError("Person name must contain only letters.")
        return person_name
    
