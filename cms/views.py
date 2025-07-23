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
    else:
        errors = {}
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
    
            try:
                user_obj = User.objects.get(username=username)
            except User.DoesNotExist:
                user_obj = None
    
            if user_obj:
                authenticated_user = authenticate(request, username=username, password=password)
                if authenticated_user:
                    login(request, authenticated_user)
                    messages.success(request, "You have successfully logged in")
                    return redirect("/")
                else:
                    errors['password'] = "Password does not match"
                    print(errors['password'])
            else:
                errors['username'] = "Username does not match"
                print(errors['username'])
    
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
    if request.method == "GET":
        print("Home Page")
        # You can add more logic here if needed
    else:
        return redirect('/log-in')
    return render(request, 'pages/home.html')