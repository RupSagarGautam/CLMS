from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


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
    return render(request, 'pages/home.html')