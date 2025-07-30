from django.shortcuts import render
from django.db.models import Sum
from datetime import date  # <-- add this import
from .models import Visit, VisitType
from django.db.models import Count
from staff.models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit
from datetime import datetime
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.utils.timezone import now


def home(request):
    # Get selected type from query string, or default to 'All'
    selected_type = request.GET.get('visit_type', 'All')

    # Base queryset
    visits = ClientVisit.objects.filter(date__isnull=False)

    # Filter by selected type if not 'All'
    if selected_type != 'All':
        visits = visits.filter(visit_type__name=selected_type)

    # Group by date and count visits
    visits_per_day = (
        visits
        .values('date')
        .annotate(total=Count('id'))
        .order_by('date')
    )

    raw_dates = [visit['date'].strftime('%Y-%m-%d') for visit in visits_per_day]
    totals = [visit['total'] for visit in visits_per_day]

    visit_types = VisitType.objects.all()

    context = {
        'allDates': raw_dates,
        'allVisitCounts': totals,
        'visit_types': visit_types,
        'selected_type': selected_type,  # <-- Pass this to keep dropdown selected
    }

    return render(request, 'pages/home.html', context)


def dashboard_view(request):
    visit_types = VisitType.objects.all()
    selected_type = request.GET.get('visit_type', 'All')

    # Filter based on selected type
    visits = Visit.objects.all()
    if selected_type != 'All':
        visits = visits.filter(visit_type__name=selected_type)

    # Total visits
    total_visits = visits.count()

    # Today's visits
    today = now().date()
    todays_visits = visits.filter(date=today).count()

    # Monthly visits (e.g., July 2025)
    monthly_visits = visits.filter(date__year=today.year, date__month=today.month).count()

    # Data for line chart: group by date
    date_counts = (
        visits
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    dates = [item['date'].strftime('%Y-%m-%d') for item in date_counts]
    totals = [item['count'] for item in date_counts]

    # Bar chart data: group by type
    type_data = (
        visits
        .values('visit_type__name')
        .annotate(count=Count('id'))
        .order_by('visit_type__name')
    )
    type_labels = [item['visit_type__name'] for item in type_data]
    type_counts = [item['count'] for item in type_data]

    # Table data
    detailed_visits = visits.select_related('visit_type').order_by('-date')[:20]


    context = {
        'visit_types': visit_types,
        'selected_type': selected_type,
        'total_visits': total_visits,
        'todays_visits': todays_visits,
        'monthly_visits': monthly_visits,
        'detailed_visits': detailed_visits,
        'dates': dates,
        'totals': totals,
        'type_labels': type_labels,
        'type_counts': type_counts
    }

    return render(request, 'pages/staff/visit_dashboard.html', context)