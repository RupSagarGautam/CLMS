from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/log-in")
def Office_Visit(request):
    return render(request, 'pages/staff/Office_Visit.html')
