from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OfficeVisit

@login_required(login_url="/log-in")
def Office_Visit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact_number = request.POST.get("contact")
        email = request.POST.get("email")
        address = request.POST.get("address")
        purpose = request.POST.get("purpose")
        date = request.POST.get("date")
        OfficeVisit.objects.create(
            user=request.user,
            name=name,
            contact_number=contact_number,
            email=email,
            address=address,
            purpose=purpose,
            date=date
        )
        messages.success(request, "Office visit added successfully!")
        return redirect("Office_Visit")
    return render(request, 'pages/staff/Office_Visit.html')


