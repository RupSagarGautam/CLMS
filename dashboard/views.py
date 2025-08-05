from django.shortcuts import render
from datetime import date, timedelta
from staff.models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit
from itertools import chain
from collections import defaultdict

def dashboard(request):
    today = date.today()
    visit_type = request.GET.get('visit_type', 'All')
    duration = request.GET.get('duration', '7 days')
    selected_month = request.GET.get('month', str(today.month))  # default to current month

    visit_type_map = {
        'Client Visit': ClientVisit,
        'Online Class': OnlineClassInquiry,
        'Office Visit': OfficeVisit,
        'College/School Visit': CollegeVisit,
    }

    # Conditional filtering logic
    def get_queryset(model):
        if request.user.is_superuser:
            return model.objects.all()
        elif request.user.is_staff:
            return model.objects.filter(user=request.user)  # Adjust field name if different
        return model.objects.none()

    # Bar chart data (visit counts by type)
    type_labels = ['Client Visit', 'Online Class', 'Office Visit', 'College/School Visit']
    type_counts = [
        get_queryset(ClientVisit).count(),
        get_queryset(OnlineClassInquiry).count(),
        get_queryset(OfficeVisit).count(),
        get_queryset(CollegeVisit).count()
    ]

    # Fetch visits based on selected type
    if visit_type in visit_type_map:
        visits_qs = get_queryset(visit_type_map[visit_type]).values('date', 'purpose', 'name')
        visits = list(visits_qs)
        for v in visits:
            v['visit_type'] = visit_type
            v['count'] = 1
    else:
        visits = list(chain(
            ({**v, 'visit_type': 'Client Visit', 'count': 1}
             for v in get_queryset(ClientVisit).values('date', 'purpose', 'name')),
            ({**v, 'visit_type': 'Online Class', 'count': 1}
             for v in get_queryset(OnlineClassInquiry).values('date', 'purpose', 'name')),
            ({**v, 'visit_type': 'Office Visit', 'count': 1}
             for v in get_queryset(OfficeVisit).values('date', 'purpose', 'name')),
            ({**v, 'visit_type': 'College/School Visit', 'count': 1}
             for v in get_queryset(CollegeVisit).values('date', 'purpose', 'name')),
        ))

    # Group visits by date
    visits_by_date = defaultdict(int)
    for visit in visits:
        visits_by_date[visit['date']] += 1

    # Prepare chart data
    if duration == '7 days':
        min_date = today - timedelta(days=6)
        date_range = [min_date + timedelta(days=i) for i in range(7)]
        formatted_dates = [d.strftime('%d %b') for d in date_range]
        totals = [visits_by_date.get(d, 0) for d in date_range]

    elif duration == 'month':
        selected_month = int(selected_month)
        year = today.year
        start_date = date(year, selected_month, 1)
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month.replace(day=1) - timedelta(days=1)

        week_totals = [0, 0, 0, 0]
        for d, count in visits_by_date.items():
            if d.month == selected_month and d.year == year:
                week_index = min((d.day - 1) // 7, 3)
                week_totals[week_index] += count
        formatted_dates = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
        totals = week_totals

    elif duration == 'year':
        month_totals = [0] * 12
        for d, count in visits_by_date.items():
            if d.year == today.year:
                month_totals[d.month - 1] += count
        formatted_dates = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        totals = month_totals

    else:  # 'all'
        yearly_data = defaultdict(int)
        for d, count in visits_by_date.items():
            yearly_data[d.year] += count
        years_sorted = sorted(yearly_data)
        formatted_dates = [str(year) for year in years_sorted]
        totals = [yearly_data[year] for year in years_sorted]

    # Recent visits
    recent_visits = sorted(visits, key=lambda x: x['date'], reverse=True)[:20]

    context = {
        'dates': formatted_dates,
        'totals': totals,
        'type_labels': type_labels,
        'type_counts': type_counts,
        'visit_types': ['All'] + type_labels,
        'selected_type': visit_type,
        'duration': duration,
        'selected_month': str(selected_month),
        'detailed_visits': recent_visits,
        'total_visits': sum(totals),
        'todays_visits': visits_by_date.get(today, 0),
        'monthly_visits': sum(count for d, count in visits_by_date.items()
                              if d.month == today.month and d.year == today.year),
    }

    return render(request, 'pages/dashboard.html', context)
