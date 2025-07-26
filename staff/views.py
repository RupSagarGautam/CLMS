from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit

# Dashboard View
def visit_dashboard(request):
    client_visits = ClientVisit.objects.all().order_by('-id')
    online_classes = OnlineClassInquiry.objects.all().order_by('-id')
    office_visits = OfficeVisit.objects.all().order_by('-id')
    college_visits = CollegeVisit.objects.all().order_by('-id')

    return render(request, 'pages/staff/visit_dashboard.html', {
        'client_visits': client_visits,
        'online_classes': online_classes,
        'office_visits': office_visits,
        'college_visits': college_visits,
    })


# Add Client Visit
def add_client_visit(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact_number']
        purpose = request.POST.get('purpose', '')
        date = request.POST['date']
        remarks = request.POST.get('remarks', '')

        ClientVisit.objects.create(
            name=name,
            contact_number=contact,
            purpose=purpose,
            date=date,
            remarks=remarks
        )
        messages.success(request, " Client Visit added successfully.")
        return redirect('client_visit_list')
    return redirect('visit_dashboard')


# Add Online Class Inquiry
def add_online_class(request):
    if request.method == 'POST':
        OnlineClassInquiry.objects.create(
            contact=request.POST.get('contact'),
            purpose=request.POST.get('purpose'),
            date=request.POST.get('date'),
            remarks=request.POST.get('remarks')
        )
        messages.success(request, " Online Class Inquiry added successfully.")
        return redirect('visit_dashboard')
    return redirect('visit_dashboard')


# Add Office Visit
def add_office_visit(request):
    if request.method == 'POST':
        OfficeVisit.objects.create(
            name=request.POST.get('name'),
            contact=request.POST.get('contact'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            purpose=request.POST.get('purpose'),
            date=request.POST.get('date'),
            remarks=request.POST.get('remarks')
        )
        messages.success(request, " Office Visit added successfully.")
        return redirect('visit_dashboard')
    return redirect('visit_dashboard')


# Add College Visit
def add_college_visit(request):
    if request.method == 'POST':
        CollegeVisit.objects.create(
            name=request.POST.get('name'),
            contact=request.POST.get('contact_number'),
            purpose=request.POST.get('purpose'),
            person=request.POST.get('person'),
            remarks=request.POST.get('remarks')
        )
        messages.success(request, " College Visit added successfully.")
        return redirect('visit_dashboard')
    return redirect('visit_dashboard')


# View Client Visit List
def client_visit_list(request):
    client_visits = ClientVisit.objects.all().order_by('-date')
    return render(request, 'pages/staff/Client_Visit.html', {'client_visits': client_visits})


# Delete Client Visit
def delete_client_visit(request, id):
    visit = get_object_or_404(ClientVisit, id=id)
    visit.delete()
    messages.success(request, " Client Visit deleted successfully.")
    return redirect('client_visit_list')
