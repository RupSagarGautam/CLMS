# from django.shortcuts import render
# from django.db.models import Sum
# from django.utils.dateparse import parse_date
# from datetime import datetime
# from .models import Visit, VisitType

# def dashboard(request):
#      # Get filter parameters from GET request
#     selected_type = request.GET.get('visit_type', 'All')
#     start_date_str = request.GET.get('start_date')
#     end_date_str = request.GET.get('end_date')

#     # Parse date strings safely
#     start_date = parse_date(start_date_str) if start_date_str else None
#     end_date = parse_date(end_date_str) if end_date_str else None

#     # Base queryset
#     visits = Visit.objects.all()
    
#     # Filter by visit type if not "All"
#     if selected_type != 'All':
#         visits = visits.filter(visit_type__name=selected_type)

#     # Filter by date range
#     if start_date:
#         visits = visits.filter(date__gte=start_date)
#     if end_date:
#         visits = visits.filter(date__lte=end_date)
        
#      # Aggregated totals
#     total_visits = visits.aggregate(total=Sum('count'))['total'] or 0

#     today = datetime.today().date()
#     todays_visits = visits.filter(date=today).aggregate(total=Sum('count'))['total'] or 0

#     monthly_visits = visits.filter(date__year=today.year, date__month=today.month).aggregate(total=Sum('count'))['total'] or 0

#     # Visit types list for dropdown
#     visit_types = VisitType.objects.values_list('name', flat=True).order_by('name')

#     # Visits over time (grouped by date)
#     visits_by_date = visits.values('date').annotate(total=Sum('count')).order_by('date')
#     dates = [v['date'].strftime('%Y-%m-%d') for v in visits_by_date]
#     totals = [v['total'] for v in visits_by_date]

#     # Distribution by visit type (grouped by visit_type)
#     visits_by_type = visits.values('visit_type__name').annotate(total=Sum('count')).order_by('visit_type__name')
#     type_labels = [v['visit_type__name'] for v in visits_by_type]
#     type_counts = [v['total'] for v in visits_by_type]

#     # Detailed visits for table (grouped by visit_type and date)
#     detailed_visits = visits.values('visit_type__name', 'date').annotate(count=Sum('count')).order_by('-date')

#     context = {
#         'selected_type': selected_type,
#         'start_date': start_date_str or '',
#         'end_date': end_date_str or '',
#         'total_visits': total_visits,
#         'todays_visits': todays_visits,
#         'monthly_visits': monthly_visits,
#         'visit_types': visit_types,
#         'dates': dates,
#         'totals': totals,
#         'type_labels': type_labels,
#         'type_counts': type_counts,
#         'detailed_visits': detailed_visits,
#     }

#     return render(request, 'pages/dashboard.html')

from django.shortcuts import render
from django.db.models import Sum
from datetime import date  # <-- add this import
from .models import Visit, VisitType

def dashboard(request):
    # Visits over time (all)
    visits_by_date = (
        Visit.objects
        .values('date')
        .annotate(total=Sum('count'))
        .order_by('date')
    )
    dates = [v['date'].strftime('%Y-%m-%d') for v in visits_by_date]
    totals = [v['total'] for v in visits_by_date]

    # Visits by type (for bar chart)
    visits_by_type = (
        Visit.objects
        .values('visit_type__name')
        .annotate(total=Sum('count'))
    )
    type_labels = [v['visit_type__name'] for v in visits_by_type]
    type_counts = [v['total'] for v in visits_by_type]

    # All visit types (for filter dropdown)
    visit_types = list(VisitType.objects.values_list('name', flat=True))

    # Detailed visits for table (optional: order by date desc)
    detailed_visits = Visit.objects.select_related('visit_type').order_by('-date')[:20]

    context = {
        'dates': dates,
        'totals': totals,
        'type_labels': type_labels,
        'type_counts': type_counts,
        'visit_types': visit_types,
        'detailed_visits': detailed_visits,
        'selected_type': 'All',
        'total_visits': sum(totals),
        'todays_visits': sum(v['total'] for v in visits_by_date if v['date'] == date.today()),
        'monthly_visits': sum(v['total'] for v in visits_by_date if v['date'].month == date.today().month),
    }

    return render(request, 'pages/dashboard.html', context)
