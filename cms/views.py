from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from django.db.models import Sum
from datetime import date
from dashboard.models import Visit, VisitType 
from django.shortcuts import render
from django.db.models import Count
from django.utils.timezone import now



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


def home_view(request):
    selected_type = request.GET.get('visit_type', 'All')

    # Get all VisitTypes
    visit_types = VisitType.objects.all()

    # Filter visits based on selected type
    if selected_type != 'All':
        visits = Visit.objects.filter(visit_type__name=selected_type)
    else:
        visits = Visit.objects.all()

    # Recent visits for table
    detailed_visits = (
        visits.values('visit_type__name', 'date')
        .annotate(count=Count('id'))
        .order_by('-date')[:15]
    )

    # Total stats
    total_visits = visits.count()
    todays_visits = visits.filter(date=timezone.now().date()).count()
    monthly_visits = visits.filter(date__month=timezone.now().month).count()

    # For charts
    visits_by_date = (
        visits.values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    dates = [v['date'].strftime('%Y-%m-%d') for v in visits_by_date]
    totals = [v['count'] for v in visits_by_date]

    visits_by_type = (
        visits.values('visit_type__name')
        .annotate(count=Count('id'))
    )
    type_labels = [v['visit_type__name'] for v in visits_by_type]
    type_counts = [v['count'] for v in visits_by_type]

    context = {
        'visit_types': visit_types,
        'selected_type': selected_type,
        'detailed_visits': detailed_visits,
        'total_visits': total_visits,
        'todays_visits': todays_visits,
        'monthly_visits': monthly_visits,
        'dates': dates,
        'totals': totals,
        'type_labels': type_labels,
        'type_counts': type_counts,
    }

    return render(request, 'pages/home.html', context)