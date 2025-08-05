from django.shortcuts import render
from datetime import date, datetime, timedelta
from django.db.models import Count
from staff.models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit
from itertools import chain

def dashboard(request):
    today = date.today()
    visit_type = request.GET.get('visit_type', 'All')

    # Map visit types to models
    visit_type_map = {
        'Client Visit': ClientVisit,
        'Online Class': OnlineClassInquiry,
        'Office Visit': OfficeVisit,
        'College/School Visit': CollegeVisit,
    }

    # Bar chart data (all time counts)
    client_visit_count = ClientVisit.objects.count()
    online_class_count = OnlineClassInquiry.objects.count()
    office_visit_count = OfficeVisit.objects.count()
    college_visit_count = CollegeVisit.objects.count()
    type_labels = ['Client Visit', 'Online Class', 'Office Visit', 'College/School Visit']
    type_counts = [client_visit_count, online_class_count, office_visit_count, college_visit_count]


    visit_type = request.GET.get('visit_type', 'All')
    if visit_type in visit_type_map:
        visits_qs = visit_type_map[visit_type].objects.all().values('date', 'purpose', 'name')
        visits = list(visits_qs)
        for v in visits:
            v['visit_type'] = visit_type
            v['count'] = 1
    else:
        visits = list(chain(
        ({**v, 'visit_type': 'Client Visit', 'count': 1} for v in ClientVisit.objects.all().values('date', 'purpose', 'name')),
        ({**v, 'visit_type': 'Online Class', 'count': 1} for v in OnlineClassInquiry.objects.all().values('date', 'purpose', 'name')),
        ({**v, 'visit_type': 'Office Visit', 'count': 1} for v in OfficeVisit.objects.all().values('date', 'purpose', 'name')),
        ({**v, 'visit_type': 'College/School Visit', 'count': 1} for v in CollegeVisit.objects.all().values('date', 'purpose', 'name')),
    ))
        
    # Group visits by date
    visits_by_date = {}
    for visit in visits:
        visit_date = visit['date']
        visits_by_date[visit_date] = visits_by_date.get(visit_date, 0) + 1

    # Determine date range for chart
    if request.GET.get('start_date') and request.GET.get('end_date'):
        try:
            min_date = datetime.strptime(request.GET['start_date'], '%Y-%m-%d').date()
            max_date = datetime.strptime(request.GET['end_date'], '%Y-%m-%d').date()
        except ValueError:
            min_date = today - timedelta(days=6)
            max_date = today
    else:
        max_date = today
        min_date = today - timedelta(days=6)

    # Fill in missing dates with 0
    full_dates = []
    current_date = min_date
    while current_date <= max_date:
        full_dates.append(current_date)
        if current_date not in visits_by_date:
            visits_by_date[current_date] = 0
        current_date += timedelta(days=1)

    full_dates.sort()
    formatted_dates = [d.strftime('%d %B') for d in full_dates]
    totals = [visits_by_date[d] for d in full_dates]

    # Recent visit list
    recent_visits = sorted(visits, key=lambda x: x['date'], reverse=True)[:20]

    context = {
        'dates': formatted_dates,
        'totals': totals,
        'type_labels': type_labels,
        'type_counts': type_counts,
        'visit_types': ['All'] + type_labels,
        'selected_type': visit_type,
        'detailed_visits': recent_visits,
        'total_visits': sum(totals),
        'todays_visits': visits_by_date.get(today, 0),
        'monthly_visits': sum(count for d, count in visits_by_date.items() if d.month == today.month and d.year == today.year),
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
    }

    return render(request, 'pages/dashboard.html', context)
