from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit

# Dashboard View
@login_required
def visit_dashboard(request):
    client_visits = ClientVisit.objects.filter(user=request.user).order_by('-id')
    online_classes = OnlineClassInquiry.objects.filter(user=request.user).order_by('-id')
    office_visits = OfficeVisit.objects.filter(user=request.user).order_by('-id')
    college_visits = CollegeVisit.objects.filter(user=request.user).order_by('-id')

    return render(request, 'pages/staff/visit_dashboard.html', {
        'client_visits': client_visits,
        'online_classes': online_classes,
        'office_visits': office_visits,
        'college_visits': college_visits,
    })


# Add Client Visit
@login_required
def add_client_visit(request):
    if request.method == 'POST':
        ClientVisit.objects.create(
            user=request.user,
            name=request.POST['name'],
            contact_number=request.POST['contact_number'],
            purpose=request.POST.get('purpose', ''),
            date=request.POST['date'],
            remarks=request.POST.get('remarks', '')
        )
        messages.success(request, "Client Visit added successfully.")
        return redirect('client_visit_list')
    return redirect('visit_dashboard')


# Add Online Class Inquiry
@login_required
def add_online_class(request):
    if request.method == 'POST':
        OnlineClassInquiry.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            contact=request.POST.get('contact'),
            interest_area=request.POST.get('purpose'),
            date=request.POST.get('date'),
            remarks=request.POST.get('remarks')
        )
        messages.success(request, "Online Class Inquiry added successfully.")
        return redirect('visit_dashboard')
    return redirect('visit_dashboard')


# Add Office Visit
@login_required
def add_office_visit(request):
    if request.method == 'POST':
        OfficeVisit.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            contact=request.POST.get('contact'),
            department=request.POST.get('department'),
            date=request.POST.get('date'),
            remarks=request.POST.get('remarks')
        )
        messages.success(request, "Office Visit added successfully.")
        return redirect('visit_dashboard')
    return redirect('visit_dashboard')


# Add College Visit
@login_required
def add_college_visit(request):
    if request.method == 'POST':
        CollegeVisit.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            contact=request.POST.get('contact'),
            institution=request.POST.get('purpose'),
            date=request.POST.get('date'),
            remarks=request.POST.get('remarks')
        )
        messages.success(request, "College Visit added successfully.")
        return redirect('visit_dashboard')
    return redirect('visit_dashboard')


# View Client Visit List
@login_required
def client_visit_list(request):
    client_visits = ClientVisit.objects.filter(user=request.user).order_by('-date')
    return render(request, 'pages/staff/Client_Visit.html', {'client_visits': client_visits})


# Delete Client Visit
@login_required
def delete_client_visit(request, id):
    visit = get_object_or_404(ClientVisit, id=id, user=request.user)
    visit.delete()
    messages.success(request, "Client Visit deleted successfully.")
    return redirect('client_visit_list')

@login_required
def online_class_list(request):
    inquiries = OnlineClassInquiry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'pages/staff/Online_Class.html', {'online_classes': inquiries})

@login_required
def add_online_class(request):
    if request.method == 'POST':
        OnlineClassInquiry.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            contact=request.POST.get('contact'),
            purpose=request.POST.get('purpose'),
            date=request.POST.get('date')
        )
        messages.success(request, "Online Class Inquiry added successfully.")
        return redirect('online_class_list')
    return redirect('online_class_list')

@login_required
def delete_online_class(request, id):
    inquiry = get_object_or_404(OnlineClassInquiry, id=id, user=request.user)
    inquiry.delete()
    messages.success(request, "Inquiry deleted successfully.")
    return redirect('online_class_list')