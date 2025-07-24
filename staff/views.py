from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import OfficeVisit

@login_required
def office_visits(request):
    if request.user.is_superuser:
        visits = OfficeVisit.objects.all()
    else:
        visits = OfficeVisit.objects.filter(staff=request.user)
    return render(request, 'visits/office_visits.html', {'visits': visits})
