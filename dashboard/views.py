from django.shortcuts import render
from django.db.models import Sum
from datetime import date  # <-- add this import
from .models import Visit, VisitType

def dashboard_view(request):
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

    return render(request, 'dashboard/dashboard.html', context)
