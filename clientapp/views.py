from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .models import PasswordResetOTP
import random
from datetime import timedelta
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.

def request_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
            return redirect('forgot_password')
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=2)  # 2 minutes expiry
        # Save OTP in DB
        PasswordResetOTP.objects.create(email=email, otp=otp, expires_at=expires_at)
        # Send OTP via email
        send_mail(
            'Your Password Reset OTP',
            f'Your OTP for password reset is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        # Redirect to OTP verification page
        return redirect(f'/verify-otp/?email={email}')
    return redirect('forgot_password')

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages

def verify_otp(request):
    email = request.GET.get('email') or request.POST.get('email')
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            otp_obj = PasswordResetOTP.objects.filter(email=email, otp=otp, used=False).latest('created_at')
        except PasswordResetOTP.DoesNotExist:
            messages.error(request, 'Invalid OTP or email.')
            return render(request, 'pages/verify_otp.html', {'email': email})
        if otp_obj.is_expired():
            messages.error(request, 'OTP has expired. Please request a new one.')
            return render(request, 'pages/verify_otp.html', {'email': email})
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
            return render(request, 'pages/verify_otp.html', {'email': email})
        # Mark OTP as used
        otp_obj.used = True
        otp_obj.save()
        # Set the backend and log the user in
        user.backend = 'cms.backends.EmailOrUsernameModelBackend'  # Specify your custom backend
        auth_login(request, user)
        messages.success(request, 'OTP verified. You are now logged in.')
        return redirect('/')
    return render(request, 'pages/verify_otp.html', {'email': email})

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        try:
            otp_obj = PasswordResetOTP.objects.filter(email=email, otp=otp, used=False).latest('created_at')
        except PasswordResetOTP.DoesNotExist:
            messages.error(request, 'Invalid OTP or email.')
            return redirect('staff_login')
        if otp_obj.is_expired():
            messages.error(request, 'OTP has expired.')
            return redirect('staff_login')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
            return redirect('staff_login')
        user.set_password(new_password)
        user.save()
        otp_obj.used = True
        otp_obj.save()
        messages.success(request, 'Password reset successful. You can now log in with your new password.')
        return redirect('staff_login')
    return redirect('staff_login')

def forgot_password(request):
    return render(request, 'pages/forget_password.html')
