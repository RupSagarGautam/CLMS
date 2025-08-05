# from django.shortcuts import render
# from datetime import date, datetime, timedelta
# from django.db.models import Count
# from staff.models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit
# from itertools import chain

# def dashboard(request):
#     today = date.today()
#     visit_type = request.GET.get('visit_type', 'All')

#     # Map visit types to models
#     visit_type_map = {
#         'Client Visit': ClientVisit,
#         'Online Class': OnlineClassInquiry,
#         'Office Visit': OfficeVisit,
#         'College/School Visit': CollegeVisit,
#     }

#     # Bar chart data (all time counts)
#     client_visit_count = ClientVisit.objects.count()
#     online_class_count = OnlineClassInquiry.objects.count()
#     office_visit_count = OfficeVisit.objects.count()
#     college_visit_count = CollegeVisit.objects.count()
#     type_labels = ['Client Visit', 'Online Class', 'Office Visit', 'College/School Visit']
#     type_counts = [client_visit_count, online_class_count, office_visit_count, college_visit_count]


#     visit_type = request.GET.get('visit_type', 'All')
#     if visit_type in visit_type_map:
#         visits_qs = visit_type_map[visit_type].objects.all().values('date', 'purpose', 'name')
#         visits = list(visits_qs)
#         for v in visits:
#             v['visit_type'] = visit_type
#             v['count'] = 1
#     else:
#         visits = list(chain(
#         ({**v, 'visit_type': 'Client Visit', 'count': 1} for v in ClientVisit.objects.all().values('date', 'purpose', 'name')),
#         ({**v, 'visit_type': 'Online Class', 'count': 1} for v in OnlineClassInquiry.objects.all().values('date', 'purpose', 'name')),
#         ({**v, 'visit_type': 'Office Visit', 'count': 1} for v in OfficeVisit.objects.all().values('date', 'purpose', 'name')),
#         ({**v, 'visit_type': 'College/School Visit', 'count': 1} for v in CollegeVisit.objects.all().values('date', 'purpose', 'name')),
#     ))
        
#     # Group visits by date
#     visits_by_date = {}
#     for visit in visits:
#         visit_date = visit['date']
#         visits_by_date[visit_date] = visits_by_date.get(visit_date, 0) + 1

#     # Determine date range for chart
#     if request.GET.get('start_date') and request.GET.get('end_date'):
#         try:
#             min_date = datetime.strptime(request.GET['start_date'], '%Y-%m-%d').date()
#             max_date = datetime.strptime(request.GET['end_date'], '%Y-%m-%d').date()
#         except ValueError:
#             min_date = today - timedelta(days=6)
#             max_date = today
#     else:
#         max_date = today
#         min_date = today - timedelta(days=6)

#     # Fill in missing dates with 0
#     full_dates = []
#     current_date = min_date
#     while current_date <= max_date:
#         full_dates.append(current_date)
#         if current_date not in visits_by_date:
#             visits_by_date[current_date] = 0
#         current_date += timedelta(days=1)

#     full_dates.sort()
#     formatted_dates = [d.strftime('%d %B') for d in full_dates]
#     totals = [visits_by_date[d] for d in full_dates]

#     # Recent visit list
#     recent_visits = sorted(visits, key=lambda x: x['date'], reverse=True)[:20]

#     context = {
#         'dates': formatted_dates,
#         'totals': totals,
#         'type_labels': type_labels,
#         'type_counts': type_counts,
#         'visit_types': ['All'] + type_labels,
#         'selected_type': visit_type,
#         'detailed_visits': recent_visits,
#         'total_visits': sum(totals),
#         'todays_visits': visits_by_date.get(today, 0),
#         'monthly_visits': sum(count for d, count in visits_by_date.items() if d.month == today.month and d.year == today.year),
#         'start_date': request.GET.get('start_date', ''),
#         'end_date': request.GET.get('end_date', ''),
#     }

#     return render(request, 'pages/dashboard.html', context)



# from django.shortcuts import render
# from datetime import date, datetime, timedelta
# from staff.models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit
# from itertools import chain

# def dashboard(request):
#     today = date.today()
#     visit_type = request.GET.get('visit_type', 'All')
#     duration = request.GET.get('duration', 'all')  # New duration param

#     # Map visit types to models
#     visit_type_map = {
#         'Client Visit': ClientVisit,
#         'Online Class': OnlineClassInquiry,
#         'Office Visit': OfficeVisit,
#         'College/School Visit': CollegeVisit,
#     }

#     # Bar chart data (all time counts)
#     client_visit_count = ClientVisit.objects.count()
#     online_class_count = OnlineClassInquiry.objects.count()
#     office_visit_count = OfficeVisit.objects.count()
#     college_visit_count = CollegeVisit.objects.count()
#     type_labels = ['Client Visit', 'Online Class', 'Office Visit', 'College/School Visit']
#     type_counts = [client_visit_count, online_class_count, office_visit_count, college_visit_count]

#     # Fetch visits based on visit_type filter
#     if visit_type in visit_type_map:
#         visits_qs = visit_type_map[visit_type].objects.all().values('date', 'purpose', 'name')
#         visits = list(visits_qs)
#         for v in visits:
#             v['visit_type'] = visit_type
#             v['count'] = 1
#     else:
#         visits = list(chain(
#             ({**v, 'visit_type': 'Client Visit', 'count': 1} for v in ClientVisit.objects.all().values('date', 'purpose', 'name')),
#             ({**v, 'visit_type': 'Online Class', 'count': 1} for v in OnlineClassInquiry.objects.all().values('date', 'purpose', 'name')),
#             ({**v, 'visit_type': 'Office Visit', 'count': 1} for v in OfficeVisit.objects.all().values('date', 'purpose', 'name')),
#             ({**v, 'visit_type': 'College/School Visit', 'count': 1} for v in CollegeVisit.objects.all().values('date', 'purpose', 'name')),
#         ))

#     # Group visits by date
#     visits_by_date = {}
#     for visit in visits:
#         visit_date = visit['date']
#         visits_by_date[visit_date] = visits_by_date.get(visit_date, 0) + 1

#     # Prepare data according to duration
#     if duration == 'week':
#         # Last 7 days (daily)
#         min_date = today - timedelta(days=6)
#         max_date = today
#         date_range = [min_date + timedelta(days=i) for i in range(7)]
#         formatted_dates = [d.strftime('%d %b') for d in date_range]
#         totals = [visits_by_date.get(d, 0) for d in date_range]

#     elif duration == 'month':
#         # Last 4 weeks grouped by week (Week 1..Week 4)
#         start_date = today - timedelta(weeks=4)
#         # Initialize 4 week buckets
#         week_totals = [0, 0, 0, 0]
#         for d, count in visits_by_date.items():
#             if d >= start_date and d <= today:
#                 # Calculate week index (0 = oldest week, 3 = most recent)
#                 days_diff = (today - d).days
#                 week_index = 3 - (days_diff // 7)
#                 if 0 <= week_index < 4:
#                     week_totals[week_index] += count
#         formatted_dates = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
#         totals = week_totals

#     else:  # 'year' or 'all'
#         # Last 12 months grouped by month name
#         month_totals = [0]*12
#         for d, count in visits_by_date.items():
#             if d.year == today.year:
#                 month_totals[d.month-1] += count
#         formatted_dates = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
#                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#         totals = month_totals

#     # Recent visits (last 20)
#     recent_visits = sorted(visits, key=lambda x: x['date'], reverse=True)[:20]

#     context = {
#         'dates': formatted_dates,
#         'totals': totals,
#         'type_labels': type_labels,
#         'type_counts': type_counts,
#         'visit_types': ['All'] + type_labels,
#         'selected_type': visit_type,
#         'duration': duration,
#         'detailed_visits': recent_visits,
#         'total_visits': sum(totals),
#         'todays_visits': visits_by_date.get(today, 0),
#         'monthly_visits': sum(count for d, count in visits_by_date.items() if d.month == today.month and d.year == today.year),
#     }

#     return render(request, 'pages/dashboard.html', context)


from django.shortcuts import render
from datetime import date, datetime, timedelta
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

    # Bar chart data (visit counts by type)
    type_labels = ['Client Visit', 'Online Class', 'Office Visit', 'College/School Visit']
    type_counts = [
        ClientVisit.objects.count(),
        OnlineClassInquiry.objects.count(),
        OfficeVisit.objects.count(),
        CollegeVisit.objects.count()
    ]

    # Fetch visits based on visit_type
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
        month_totals = [0]*12
        for d, count in visits_by_date.items():
            if d.year == today.year:
                month_totals[d.month - 1] += count
        formatted_dates = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        totals = month_totals

    else:  # duration == 'all'
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
