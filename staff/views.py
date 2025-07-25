from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/log-in")
def office_visit(request):
    return render(request, 'staff/OffileVisit.html')
