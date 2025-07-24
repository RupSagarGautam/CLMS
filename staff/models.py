from django.db import models
from django.contrib.auth.models import User

class OfficeVisit(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=100)
    purpose = models.TextField()
    visit_date = models.DateField(auto_now_add=True)

class OnlineClassInquiry(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    inquiry_date = models.DateField(auto_now_add=True)

class ClientVisit(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    reason = models.TextField()
    visit_date = models.DateField(auto_now_add=True)

class SchoolCollegeVisit(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=150)
    details = models.TextField()
    visit_date = models.DateField(auto_now_add=True)
