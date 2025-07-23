# clientapp/models.py

from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    company = models.CharField(max_length=100, blank=True)
    joined_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
