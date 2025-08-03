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


def dashboard(request):
    return render(request, 'pages/dashboard.html')