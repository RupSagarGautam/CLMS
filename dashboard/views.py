# # from django.shortcuts import render
# # from django.db.models import Sum
# # from django.utils.dateparse import parse_date
# # from datetime import datetime
# # from .models import Visit, VisitType

# # def dashboard(request):
# #      # Get filter parameters from GET request
# #     selected_type = request.GET.get('visit_type', 'All')
# #     start_date_str = request.GET.get('start_date')
# #     end_date_str = request.GET.get('end_date')

# #     # Parse date strings safely
# #     start_date = parse_date(start_date_str) if start_date_str else None
# #     end_date = parse_date(end_date_str) if end_date_str else None

# #     # Base queryset
# #     visits = Visit.objects.all()
    
# #     # Filter by visit type if not "All"
# #     if selected_type != 'All':
# #         visits = visits.filter(visit_type__name=selected_type)

# #     # Filter by date range
# #     if start_date:
# #         visits = visits.filter(date__gte=start_date)
# #     if end_date:
# #         visits = visits.filter(date__lte=end_date)
        
# #      # Aggregated totals
# #     total_visits = visits.aggregate(total=Sum('count'))['total'] or 0

# #     today = datetime.today().date()
# #     todays_visits = visits.filter(date=today).aggregate(total=Sum('count'))['total'] or 0

# #     monthly_visits = visits.filter(date__year=today.year, date__month=today.month).aggregate(total=Sum('count'))['total'] or 0

# #     # Visit types list for dropdown
# #     visit_types = VisitType.objects.values_list('name', flat=True).order_by('name')

# #     # Visits over time (grouped by date)
# #     visits_by_date = visits.values('date').annotate(total=Sum('count')).order_by('date')
# #     dates = [v['date'].strftime('%Y-%m-%d') for v in visits_by_date]
# #     totals = [v['total'] for v in visits_by_date]

# #     # Distribution by visit type (grouped by visit_type)
# #     visits_by_type = visits.values('visit_type__name').annotate(total=Sum('count')).order_by('visit_type__name')
# #     type_labels = [v['visit_type__name'] for v in visits_by_type]
# #     type_counts = [v['total'] for v in visits_by_type]

# #     # Detailed visits for table (grouped by visit_type and date)
# #     detailed_visits = visits.values('visit_type__name', 'date').annotate(count=Sum('count')).order_by('-date')

# #     context = {
# #         'selected_type': selected_type,
# #         'start_date': start_date_str or '',
# #         'end_date': end_date_str or '',
# #         'total_visits': total_visits,
# #         'todays_visits': todays_visits,
# #         'monthly_visits': monthly_visits,
# #         'visit_types': visit_types,
# #         'dates': dates,
# #         'totals': totals,
# #         'type_labels': type_labels,
# #         'type_counts': type_counts,
# #         'detailed_visits': detailed_visits,
# #     }

# #     return render(request, 'pages/dashboard.html')

# # from django.shortcuts import render
# # from django.db.models import Sum
# # from datetime import date  # <-- add this import
# # from .models import Visit, VisitType
# # from django.db.models import Count
# # from staff.models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit
# # from datetime import datetime
# # from django.db.models.functions import TruncDate
# # from django.db.models import Count
# # from django.utils.timezone import now


# # def dashboard(request):
# #     # Visits over time (all)
# #     visits_by_date = (
# #         Visit.objects
# #         .values('date')
# #         .annotate(total=Sum('count'))
# #         .order_by('date')
# #     )
# #     dates = [v['date'].strftime('%Y-%m-%d') for v in visits_by_date]
# #     totals = [v['total'] for v in visits_by_date]

# #     # Visits by type (for bar chart)
# #     visits_by_type = (
# #         Visit.objects
# #         .values('visit_type__name')
# #         .annotate(total=Sum('count'))
# #     )
# #     type_labels = [v['visit_type__name'] for v in visits_by_type]
# #     type_counts = [v['total'] for v in visits_by_type]

# #     # All visit types (for filter dropdown)
# #     visit_types = list(VisitType.objects.values_list('name', flat=True))

# #     # Detailed visits for table (optional: order by date desc)
# #     detailed_visits = Visit.objects.select_related('visit_type').order_by('-date')[:20]

# #     context = {
# #         'dates': dates,
# #         'totals': totals,
# #         'type_labels': type_labels,
# #         'type_counts': type_counts,
# #         'visit_types': visit_types,
# #         'detailed_visits': detailed_visits,
# #         'selected_type': 'All',
# #         'total_visits': sum(totals),
# #         'todays_visits': sum(v['total'] for v in visits_by_date if v['date'] == date.today()),
# #         'monthly_visits': sum(v['total'] for v in visits_by_date if v['date'].month == date.today().month),
# #     }

# #     return render(request, 'pages/dashboard.html', context)



# # from django.shortcuts import render
# # from datetime import date
# # from django.db.models import Count
# # from staff.models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit
# # from itertools import chain

# # def dashboard(request):
# #     today = date.today()
    
# #     # Count for each visit type
# #     client_visit_count = ClientVisit.objects.count()
# #     online_class_count = OnlineClassInquiry.objects.count()
# #     office_visit_count = OfficeVisit.objects.count()
# #     college_visit_count = CollegeVisit.objects.count()

# #     # Gather all visits
# #     all_visits = list(chain(
# #         ClientVisit.objects.all().values('date', 'purpose', 'name'),
# #         OnlineClassInquiry.objects.all().values('date', 'purpose', 'name'),
# #         OfficeVisit.objects.all().values('date', 'purpose', 'name'),
# #         CollegeVisit.objects.all().values('date', 'purpose', 'name'),
# #     ))

# #     # Line Chart: visits per day
# #     visits_by_date = {}
# #     for visit in all_visits:
# #         visit_date = visit['date']
# #         visits_by_date[visit_date] = visits_by_date.get(visit_date, 0) + 1

# #     dates = sorted(visits_by_date)
# #     totals = [visits_by_date[d] for d in dates]
# #     formatted_dates = [d.strftime('%Y-%m-%d') for d in dates]

# #     # Bar Chart: visits by purpose
# #      # Prepare labels and counts for bar chart
# #     type_labels = ['Client Visit', 'Online Class', 'Office Visit', 'College/School Visit']
# #     type_counts = [client_visit_count, online_class_count, office_visit_count, college_visit_count]

# #     # Table: most recent 20 visits across all models
# #     recent_visits = sorted(all_visits, key=lambda x: x['date'], reverse=True)[:20]

# #     context = {
# #         'dates': formatted_dates,
# #         'totals': totals,
# #         'type_labels': type_labels,
# #         'type_counts': type_counts,
# #         'visit_types': list(set(type_labels)),
# #         'detailed_visits': recent_visits,
# #         'selected_type': 'All',
# #         'total_visits': sum(totals),
# #         'todays_visits': visits_by_date.get(today, 0),
# #         'monthly_visits': sum(count for d, count in visits_by_date.items() if d.month == today.month and d.year == today.year),
# #     }

# #     return render(request, 'pages/dashboard.html', context)

# from django.shortcuts import render
# from datetime import date
# from django.db.models import Count
# from staff.models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit
# from itertools import chain

# def dashboard(request):
#     today = date.today()
#     visit_type = request.GET.get('visit_type', 'All')  # Get filter type from dropdown

#     # Initialize variables
#     all_visits = []
#     selected_type = visit_type

#     # Visit type mapping
#     visit_type_map = {
#         'Client Visit': ClientVisit,
#         'Online Class': OnlineClassInquiry,
#         'Office Visit': OfficeVisit,
#         'College/School Visit': CollegeVisit
#     }

#     # Bar Chart Counts
#     client_visit_count = ClientVisit.objects.count()
#     online_class_count = OnlineClassInquiry.objects.count()
#     office_visit_count = OfficeVisit.objects.count()
#     college_visit_count = CollegeVisit.objects.count()

#     # For bar chart
#     type_labels = ['Client Visit', 'Online Class', 'Office Visit', 'College/School Visit']
#     type_counts = [client_visit_count, online_class_count, office_visit_count, college_visit_count]

#     # Filtered visits for line chart
#     if visit_type in visit_type_map:
#         visits_qs = visit_type_map[visit_type].objects.all().values('date', 'purpose', 'name')
#         all_visits = list(visits_qs)
#     else:
#         # "All" selected — chain everything
#         all_visits = list(chain(
#             ClientVisit.objects.all().values('date', 'purpose', 'name'),
#             OnlineClassInquiry.objects.all().values('date', 'purpose', 'name'),
#             OfficeVisit.objects.all().values('date', 'purpose', 'name'),
#             CollegeVisit.objects.all().values('date', 'purpose', 'name'),
#         ))

#     # Group visits by date for line chart
#     visits_by_date = {}
#     for visit in all_visits:
#         visit_date = visit['date']
#         visits_by_date[visit_date] = visits_by_date.get(visit_date, 0) + 1

#     dates = sorted(visits_by_date)
#     totals = [visits_by_date[d] for d in dates]
#     formatted_dates = [d.strftime('%Y-%m-%d') for d in dates]

#     # Table: show recent 20 visits
#     recent_visits = sorted(all_visits, key=lambda x: x['date'], reverse=True)[:20]

#     context = {
#         'dates': formatted_dates,
#         'totals': totals,
#         'type_labels': type_labels,
#         'type_counts': type_counts,
#         'visit_types': ['All'] + type_labels,
#         'detailed_visits': recent_visits,
#         'selected_type': selected_type,
#         'total_visits': sum(totals),
#         'todays_visits': visits_by_date.get(today, 0),
#         'start_date': request.GET.get('start_date', ''),
#         'end_date': request.GET.get('end_date', ''),
#         'monthly_visits': sum(count for d, count in visits_by_date.items() if d.month == today.month and d.year == today.year),
#     }

#     return render(request, 'pages/dashboard.html', context)

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

    # Get visit data based on filter
    if visit_type in visit_type_map:
        visits_qs = visit_type_map[visit_type].objects.all().values('date', 'purpose', 'name')
    else:
        visits_qs = chain(
            ClientVisit.objects.all().values('date', 'purpose', 'name'),
            OnlineClassInquiry.objects.all().values('date', 'purpose', 'name'),
            OfficeVisit.objects.all().values('date', 'purpose', 'name'),
            CollegeVisit.objects.all().values('date', 'purpose', 'name'),
        )

    visits = list(visits_qs)

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
