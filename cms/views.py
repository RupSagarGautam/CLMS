from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.contrib.auth import logout
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from dashboard.models import Visit, VisitType 
from django.shortcuts import render
from django.db.models import Count
from clientapp.models import UserProfile
import os


=======
>>>>>>> def59db0b4ba08b0312d692277c5ab2145c33b7a

def staff_login(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in")
        return redirect("/")

    errors = {}

    if request.method == "POST":
<<<<<<< HEAD
        identifier = request.POST.get("username")  # can be email or username
=======
        identifier = request.POST.get("username")
>>>>>>> def59db0b4ba08b0312d692277c5ab2145c33b7a
        password = request.POST.get("password")

        user_obj = None

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

        if user_obj:
            authenticated_user = authenticate(request, username=user_obj.username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, "You have successfully logged in")
                return redirect("/")
            else:
                errors["password"] = "Incorrect password"

        return render(request, 'pages/login.html', {'errors': errors})
<<<<<<< HEAD
    
    return render(request, 'pages/login.html')
=======
    else:
        return render(request, 'pages/login.html')

>>>>>>> def59db0b4ba08b0312d692277c5ab2145c33b7a

@login_required(login_url="/log-in")
def logoutUser(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect("/log-in")


@login_required(login_url="/log-in")
def home(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access this page")
        return render(request, "pages/login.html", status=403)
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page")
        return render(request, "pages/login.html", status=403)
<<<<<<< HEAD
    if request.user.is_staff and not request.user.is_superuser:
        return render(request, "pages/staff/add_dashboard.html")
    elif request.user.is_superuser and request.user.is_staff:
        return render(request, "pages/home.html")
    return render(request, 'pages/home.html')


=======
    return render(request, 'pages/home.html')


from clientapp.models import UserProfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

>>>>>>> def59db0b4ba08b0312d692277c5ab2145c33b7a
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
<<<<<<< HEAD
                import os

                if user_profile.profile_picture:
                    image_path = user_profile.profile_picture.path
                    if os.path.isfile(image_path):
                        os.remove(image_path)
=======
                if user_profile.profile_picture:
                    if os.path.isfile(user_profile.profile_picture.path):
                        os.remove(user_profile.profile_picture.path)
>>>>>>> def59db0b4ba08b0312d692277c5ab2145c33b7a
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
