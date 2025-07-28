from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def staff_login(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in")
        return redirect("/")

    errors = {}

    if request.method == "POST":
        identifier = request.POST.get("username")
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
                if not authenticated_user.is_staff and not authenticated_user.is_superuser:
                    messages.info(request, "You are not authorized to access this page")
                    return redirect("/log-in")
                login(request, authenticated_user)
                messages.success(request, "You have successfully logged in")
                return redirect("/")
            else:
                errors["password"] = "Incorrect password"

        return render(request, 'pages/login.html', {'errors': errors})
    else:
        return render(request, 'pages/login.html')


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
    return render(request, 'pages/home.html')


@login_required
def profile(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page")
        return render(request, "pages/login.html", status=403)

    user = request.user

    context = {
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "phone": getattr(user, 'phone', ''),
        "roles": "Super Admin" if user.is_superuser else ("Staff" if user.is_staff else "User"),
    }

    return render(request, 'pages/profile.html', context)


@login_required(login_url="/log-in")
def editProfile(request):
    user = request.user

    if not user.is_staff:
        messages.error(request, "You are not authorized to access this page")
        return render(request, "pages/login.html", status=403)

    field_errors = {}
    first_name = user.first_name
    last_name = user.last_name

    if request.method == "POST":
        first_name = request.POST.get("firstName", "").strip()
        last_name = request.POST.get("lastName", "").strip()

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
    }

    return render(request, "pages/edit_profile.html", context)
