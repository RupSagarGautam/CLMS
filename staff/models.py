from django.db import models
from django.contrib.auth.models import User

class ClientVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    purpose = models.CharField(max_length=255)
    date = models.DateField()
    remarks = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.name} - {self.date}"

class OnlineClassInquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    purpose = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.date}"

class OfficeVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    date = models.DateField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.date}"

class CollegeVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    institution = models.CharField(max_length=200)
    date = models.DateField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
