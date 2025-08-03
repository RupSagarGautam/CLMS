# clientapp/models.py

from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

<<<<<<< HEAD

=======
>>>>>>> def59db0b4ba08b0312d692277c5ab2145c33b7a
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.email} - {self.otp} - {'Used' if self.used else 'Unused'}"