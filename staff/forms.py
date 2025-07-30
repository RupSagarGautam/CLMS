from django import forms
from .models import OfficeVisit, ClientVisit, OnlineClassInquiry, CollegeVisit
import re

# ------------------------
# Office Visit Form
# ------------------------
from django import forms
from .models import OfficeVisit

class OfficeVisitForm(forms.ModelForm):
    class Meta:
        model = OfficeVisit
        fields = ['name', 'contact', 'email', 'address', 'purpose', 'date']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            return email  # Let Django handle required validation if blank

        # Convert to lowercase (optional: if you want to auto-correct instead of raising error)
        if any(char.isupper() for char in email):
            raise forms.ValidationError("Email must be in lowercase letters only.")

        # Check if email already exists
        if OfficeVisit.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")

        return email


    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact')
        if contact:
            if not contact.isdigit():
                raise forms.ValidationError("Contact must be numbers only.")
            if len(contact) < 10:
                raise forms.ValidationError("Contact number must be at least 10 digits.")
            if OfficeVisit.objects.filter(contact=contact).exists():
                raise forms.ValidationError("Contact number already exists.")
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
    class Meta:
        model = ClientVisit
        fields = ['name', 'contact_number', 'purpose', 'date']

    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if contact:
            if not contact.isdigit():
                raise forms.ValidationError("Contact must be numbers only.")
            if len(contact) < 10:
                raise forms.ValidationError("Contact number must be at least 10 digits.")
            if ClientVisit.objects.filter(contact_number=contact).exists():
                raise forms.ValidationError("Contact number already exists.")
        return contact

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if re.search(r'\d|@', name):
                raise forms.ValidationError("Name must contain only letters.")
        return name

# ------------------------
# Online Class Inquiry Form
# ------------------------
class OnlineClassInquiryForm(forms.ModelForm):
    class Meta:
        model = OnlineClassInquiry
        fields = ['name', 'contact', 'purpose', 'date']

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if contact:
            if not contact.isdigit():
                raise forms.ValidationError("Contact must be numbers only.")
            if len(contact) < 10:
                raise forms.ValidationError("Contact number must be at least 10 digits.")
            if OnlineClassInquiry.objects.filter(contact=contact).exists():
                raise forms.ValidationError("Contact number already exists.")
        return contact

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if re.search(r'\d|@', name):
                raise forms.ValidationError("Name must contain only letters.")
        return name

# ------------------------
# College Visit Form
# ------------------------
class CollegeVisitForm(forms.ModelForm):
    class Meta:
        model = CollegeVisit
        fields = ['name', 'contact', 'person_name', 'purpose', 'date']

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if contact:
            if not contact.isdigit():
                raise forms.ValidationError("Contact must be numbers only.")
            if len(contact) < 10:
                raise forms.ValidationError("Contact number must be at least 10 digits.")
            if CollegeVisit.objects.filter(contact=contact).exists():
                raise forms.ValidationError("Contact number already exists.")
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
