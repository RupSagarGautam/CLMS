from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit


#  DASHBOARD 

@login_required
def visit_dashboard(request):
    if request.user.is_superuser:
        client_visits = ClientVisit.objects.all().order_by('-id')
        online_classes = OnlineClassInquiry.objects.all().order_by('-id')
        office_visits = OfficeVisit.objects.all().order_by('-id')
        college_visits = CollegeVisit.objects.all().order_by('-id')
    else:
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


#  ADD FORMS 

@login_required
def add_client_visit(request):
    if request.method == 'POST':
        ClientVisit.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            contact_number=request.POST.get('contact_number'),
            purpose=request.POST.get('purpose'),
            date=request.POST.get('date')
        )
        messages.success(request, "Client Visit added successfully.")
        return redirect('client_visit_list')
    return redirect('visit_dashboard')


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
    return redirect('visit_dashboard')


@login_required
def add_office_visit(request):
    if request.method == 'POST':
        OfficeVisit.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            contact=request.POST.get('contact'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            purpose=request.POST.get('purpose'),
            date=request.POST.get('date')
        )
        messages.success(request, "Office Visit added successfully.")
        return redirect('office_visit_list')
    return redirect('visit_dashboard')


@login_required
def add_college_visit(request):
    if request.method == 'POST':
        CollegeVisit.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            contact_number=request.POST.get('contact'),
            person_name=request.POST.get('person_name'),
            purpose=request.POST.get('purpose')
        )
        messages.success(request, "College/School Visit added successfully.")
        return redirect('college_visit_list')
    return redirect('visit_dashboard')


#  VIEW LISTS 

@login_required
def client_visit_list(request):
    if request.user.is_superuser:
        client_visits = ClientVisit.objects.all().order_by('-date')
    else:
        client_visits = ClientVisit.objects.filter(user=request.user).order_by('-date')
    return render(request, 'pages/staff/Client_Visit.html', {'client_visits': client_visits})


@login_required
def online_class_list(request):
    if request.user.is_superuser:
        online_classes = OnlineClassInquiry.objects.all().order_by('-date')
    else:
        online_classes = OnlineClassInquiry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'pages/staff/Online_Class.html', {'online_classes': online_classes})


@login_required
def office_visit_list(request):
    if request.user.is_superuser:
        office_visits = OfficeVisit.objects.all().order_by('-date')
    else:
        office_visits = OfficeVisit.objects.filter(user=request.user).order_by('-date')
    return render(request, 'pages/staff/Office_Visit.html', {'office_visits': office_visits})


@login_required
def college_visit_list(request):
    if request.user.is_superuser:
        college_visits = CollegeVisit.objects.all().order_by('-id')
    else:
        college_visits = CollegeVisit.objects.filter(user=request.user).order_by('-id')
    return render(request, 'pages/staff/College_SchoolVisit.html', {'college_visits': college_visits})


#  DELETE 

@login_required
def delete_client_visit(request, id):
    visit = get_object_or_404(ClientVisit, id=id)
    if request.user.is_superuser or visit.user == request.user:
        visit.delete()
        messages.success(request, "Client Visit deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this.")
    return redirect('client_visit_list')


@login_required
def delete_online_class(request, id):
    inquiry = get_object_or_404(OnlineClassInquiry, id=id)
    if request.user.is_superuser or inquiry.user == request.user:
        inquiry.delete()
        messages.success(request, "Online Class Inquiry deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this.")
    return redirect('online_class_list')


@login_required
def delete_office_visit(request, id):
    visit = get_object_or_404(OfficeVisit, id=id)
    if request.user.is_superuser or visit.user == request.user:
        visit.delete()
        messages.success(request, "Office Visit deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this.")
    return redirect('office_visit_list')


@login_required
def delete_college_visit(request, id):
    visit = get_object_or_404(CollegeVisit, id=id)
    if request.user.is_superuser or visit.user == request.user:
        visit.delete()
        messages.success(request, "College/School Visit deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this.")
    return redirect('college_visit_list')
