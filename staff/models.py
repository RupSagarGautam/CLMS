from django.db import models

class ClientVisit(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    purpose = models.CharField(max_length=255)
    date = models.DateField()
    remarks = models.TextField(blank=True)
    
class OnlineClassInquiry(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    interest_area = models.CharField(max_length=200)
    date = models.DateField()

class OfficeVisit(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    date = models.DateField()

class CollegeVisit(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    institution = models.CharField(max_length=200)
    date = models.DateField()


    def __str__(self):
        return f"{self.name} - {self.date}"