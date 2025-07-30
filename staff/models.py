from django.db import models
from django.contrib.auth.models import User

class ClientVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name


class OnlineClassInquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    purpose = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name


class OfficeVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name


class CollegeVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    person_name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=255)
    date = models.DateField()  

    def __str__(self):
        return self.name
