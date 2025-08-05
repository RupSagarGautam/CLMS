from django.shortcuts import get_object_or_404, redirect, render
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
from django.db.models import Q, Count
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from staff.models import ClientVisit, OfficeVisit, CollegeVisit, OnlineClassInquiry
from django.contrib.admin.models import LogEntry
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType


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
    if request.user.is_staff and not request.user.is_superuser:
        return render(request, "pages/staff/add_dashboard.html")
    elif request.user.is_superuser and request.user.is_staff:
        if not request.user.is_authenticated or (not request.user.is_staff and not request.user.is_superuser):
            messages.error(request, "You are not authorized to access this page")
            return render(request, "pages/login.html", status=403)

        last_7_days = now() - timezone.timedelta(days=7)
        query = LogEntry.objects.filter(
            action_time__gte=last_7_days,
            user__is_staff=True
        ).select_related('user', 'content_type').order_by('-action_time')

        view_all = request.GET.get('view') == 'all'
        recent_staff_activity = query if (view_all and request.user.is_superuser) else query[:10]

        context = {
            'total_client_visits': ClientVisit.objects.count(),
            'total_online_inquiries': OnlineClassInquiry.objects.count(),
            'total_office_visits': OfficeVisit.objects.count(),
            'total_college_visits': CollegeVisit.objects.count(),
            'recent_staff_activity': recent_staff_activity,
            'view_all': view_all,
        }

        return render(request, 'pages/recent_activity.html', context)
    return render(request, 'pages/recent_activity.html', context)



# ...

@login_required(login_url="/log-in")
def recent_activity(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page, Only Admin can view Staff Activity")
        if request.user.is_staff:
            return redirect('/logout')
        return render(request, "pages/login.html", status=403)
    else:

        last_7_days = now() - timezone.timedelta(days=7)
        query = LogEntry.objects.filter(
            action_time__gte=last_7_days,
            user__is_staff=True
        ).select_related('user', 'content_type').order_by('-action_time')

        view_all = request.GET.get('view') == 'all'
        recent_staff_activity = query if (view_all and request.user.is_superuser) else query[:10]

        context = {
            'total_client_visits': ClientVisit.objects.count(),
            'total_online_inquiries': OnlineClassInquiry.objects.count(),
            'total_office_visits': OfficeVisit.objects.count(),
            'total_college_visits': CollegeVisit.objects.count(),
            'recent_staff_activity': recent_staff_activity,
            'view_all': view_all,
        }

        return render(request, 'pages/recent_activity.html', context)

def log_action(request, obj, action_flag, message=""):
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=action_flag,
        change_message=message
    )

@login_required(login_url="/log-in")
def delete_online_class(request, id):
    inquiry = get_object_or_404(OnlineClassInquiry, id=id)
    if request.user.is_superuser or inquiry.user == request.user:
        log_action(request, inquiry, DELETION, "Deleted Online Class Inquiry")
        inquiry.delete()
        messages.success(request, "Online Class Inquiry deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this.")
    return redirect('online_class_list')


    
@login_required
def delete_client_visit(request, id):
    visit = get_object_or_404(ClientVisit, id=id)
    if request.user.is_superuser or visit.user == request.user:
        log_action(request, visit, DELETION, "Deleted Client Visit")
        visit.delete()
        messages.success(request, "Client Visit deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this.")
    return redirect('client_visit_list')

@login_required
def delete_office_visit(request, id):
    visit = get_object_or_404(OfficeVisit, id=id)
    if request.user.is_superuser or visit.user == request.user:
        log_action(request, visit, DELETION, "Deleted Office Visit")
        visit.delete()
        messages.success(request, "Office Visit deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this.")
    return redirect('office_visit_list')


@login_required
def delete_college_visit(request, id):
    visit = get_object_or_404(CollegeVisit, id=id)
    if request.user.is_superuser or visit.user == request.user:
        log_action(request, visit, DELETION, "Deleted College/School Visit")
        visit.delete()
        messages.success(request, "College/School Visit deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this.")
    return redirect('college_visit_list')



from clientapp.models import UserProfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

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
                if user_profile.profile_picture:
                    if os.path.isfile(user_profile.profile_picture.path):
                        os.remove(user_profile.profile_picture.path)
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
