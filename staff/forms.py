# forms.py
from django import forms
from .models import OfficeVisit, ClientVisit, OnlineClassInquiry, CollegeVisit
import re

class OfficeVisitForm(forms.ModelForm):
    class Meta:
        model = OfficeVisit
        fields = ['name', 'contact', 'email', 'address', 'purpose', 'date']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Exclude current instance when checking for duplicates
        if self.instance.pk:
            if OfficeVisit.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Email already exists.")
        else:
            if OfficeVisit.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists.")
        return email

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact.isdigit():
            raise forms.ValidationError("Contact must be numbers only.")
        # Exclude current instance when checking for duplicates
        if self.instance.pk:
            if OfficeVisit.objects.filter(contact=contact).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Contact number already exists.")
        else:
            if OfficeVisit.objects.filter(contact=contact).exists():
                raise forms.ValidationError("Contact number already exists.")
        return contact

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if re.search(r'\d|@', name):
            raise forms.ValidationError("Name must contain only letters.")
        return name


class ClientVisitForm(forms.ModelForm):
    class Meta:
        model = ClientVisit
        fields = ['name', 'contact_number', 'purpose', 'date']

    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if not contact.isdigit():
            raise forms.ValidationError("Contact must be numbers only.")
        if ClientVisit.objects.filter(contact_number=contact).exists():
            raise forms.ValidationError("Contact number already exists.")
        return contact

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if re.search(r'\d|@', name):
            raise forms.ValidationError("Name must contain only letters.")
        return name


class OnlineClassInquiryForm(forms.ModelForm):
    class Meta:
        model = OnlineClassInquiry
        fields = ['name', 'contact', 'purpose', 'date']

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact.isdigit():
            raise forms.ValidationError("Contact must be numbers only.")
        if OnlineClassInquiry.objects.filter(contact=contact).exists():
            raise forms.ValidationError("Contact number already exists.")
        return contact

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if re.search(r'\d|@', name):
            raise forms.ValidationError("Name must contain only letters.")
        return name


class CollegeVisitForm(forms.ModelForm):
    class Meta:
        model = CollegeVisit
        fields = ['name', 'contact_number', 'person_name', 'purpose']

    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if not contact.isdigit():
            raise forms.ValidationError("Contact must be numbers only.")
        if CollegeVisit.objects.filter(contact_number=contact).exists():
            raise forms.ValidationError("Contact number already exists.")
        return contact

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if re.search(r'\d|@', name):
            raise forms.ValidationError("Name must contain only letters.")
        return name

    def clean_person_name(self):
        person_name = self.cleaned_data.get('person_name')
        if re.search(r'\d|@', person_name):
            raise forms.ValidationError("Person name must contain only letters.")
        return person_name
