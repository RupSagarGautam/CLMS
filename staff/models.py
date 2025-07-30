"""
Models for staff app: defines data structure for Office Visit, Client Visit, Online Class Inquiry, and College/School Visit.
"""

# --- Imports: Django core models ---
from django.db import models
from django.contrib.auth.models import User

# --- Client Visit Model ---
class ClientVisit(models.Model):
    """Model for storing client visit records."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name

# --- Online Class Inquiry Model ---
class OnlineClassInquiry(models.Model):
    """Model for storing online class inquiry records."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    purpose = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name

# --- Office Visit Model ---
class OfficeVisit(models.Model):
    """Model for storing office visit records."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name

# --- College/School Visit Model ---
class CollegeVisit(models.Model):
    """Model for storing college/school visit records."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    person_name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=255)
    date = models.DateField()  

    def __str__(self):
        return self.name
