from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from dashboard.models import Visit, VisitType 
from django.shortcuts import render
from django.db.models import Count
from clientapp.models import UserProfile
import os



def staff_login(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in")
        return redirect("/")
    
    errors = {}

    if request.method == "POST":
        identifier = request.POST.get("username")  # can be email or username
        password = request.POST.get("password")

        user_obj = None

        # Determine if it's an email or a username
        if "@" in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
            except User.DoesNotExist:
                errors["username"] = "Email not found"
        else:
            try:
                user_obj = User.objects.get(username=identifier)
            except User.DoesNotExist:
                errors["username"] = "Username not found"

        # If user found, try to authenticate
        if user_obj:
            authenticated_user = authenticate(request, username=user_obj.username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, "You have successfully logged in")
                return redirect("/")
            else:
                errors["password"] = "Incorrect password"

        return render(request, 'pages/login.html', {'errors': errors})
    
    return render(request, 'pages/login.html')

@login_required(login_url="/log-in")
def logoutUser(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    print("Logout Success")
    return redirect("/log-in")

@login_required(login_url="/log-in")
def home(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access this page")
        return render(request, "pages/login.html", status=403)
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page")
        return render(request, "pages/login.html", status=403)
    if request.user.is_staff and not request.user.is_superuser:
        return render(request, "pages/staff/add_dashboard.html")
    elif request.user.is_superuser and request.user.is_staff:
        return render(request, "pages/home.html")
    return render(request, 'pages/home.html')


@login_required
def profile(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page")
        return render(request, "pages/login.html", status=403)

    user = request.user
    
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    context = {
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "phone": getattr(user, 'phone', ''),
        "roles": "Super Admin" if user.is_superuser else ("Staff" if user.is_staff else "User"),
        "profile_picture": user_profile.profile_picture,
    }

    return render(request, 'pages/profile.html', context)


@login_required(login_url="/log-in")
def editProfile(request):
    user = request.user

    if not user.is_staff:
        messages.error(request, "You are not authorized to access this page")
        return render(request, "pages/login.html", status=403)

    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    field_errors = {}
    first_name = user.first_name
    last_name = user.last_name

    if request.method == "POST":
        first_name = request.POST.get("firstName", "").strip()
        last_name = request.POST.get("lastName", "").strip()
        
        # Handle profile picture upload
        profile_picture = request.FILES.get('profile_picture')
        
        if profile_picture:
            # Check if file is an image
            if not profile_picture.content_type.startswith('image'):
                field_errors["profile_picture"] = "Please upload an image file only"
            else:
                # Delete old profile picture if it exists
                import os

                if user_profile.profile_picture:
                    image_path = user_profile.profile_picture.path
                    if os.path.isfile(image_path):
                        os.remove(image_path)
                # Save new profile picture
                user_profile.profile_picture = profile_picture
                user_profile.save()

        if not first_name:
            field_errors["firstName"] = "First name cannot be empty"
        elif len(first_name) < 3:
            field_errors["firstName"] = "First name must be at least 3 characters long"

        if not last_name:
            field_errors["lastName"] = "Last name cannot be empty"
        elif len(last_name) < 3:
            field_errors["lastName"] = "Last name must be at least 3 characters long"

        if not field_errors:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("/profile")

    context = {
        "firstName": first_name,
        "lastName": last_name,
        "email": user.email,
        "phone": getattr(user, 'phone', ''),
        "roles": "Super Admin" if user.is_superuser else ("Staff" if user.is_staff else "User"),
        "field_errors": field_errors,
        "profile_picture": user_profile.profile_picture,
    }

    return render(request, "pages/edit_profile.html", context)
