from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit
from .forms import ClientVisitForm, OnlineClassInquiryForm, OfficeVisitForm, CollegeVisitForm

#  DASHBOARD 

@login_required
def add_dashboard(request):
    return render(request, 'pages/staff/add_dashboard.html', {
        'client_form': ClientVisitForm(),
        'online_form': OnlineClassInquiryForm(),
        'office_form': OfficeVisitForm(),
        'college_form': CollegeVisitForm(),
    })

#  ADD FORMS 

@login_required
def add_client_visit(request):
    if request.method == 'POST':
        form = ClientVisitForm(request.POST)
        if form.is_valid():
            client_visit = form.save(commit=False)
            client_visit.user = request.user
            client_visit.save()
            messages.success(request, "Client Visit added successfully.")
            return redirect('client_visit_list')
        else:
            messages.error(request, "There were errors in your form.")
    return redirect('add_dashboard')


@login_required
def add_online_class(request):
    if request.method == 'POST':
        form = OnlineClassInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = request.user
            inquiry.save()
            messages.success(request, "Online Class Inquiry added successfully.")
            return redirect('online_class_list')
        else:
            messages.error(request, "There were errors in your form.")
    return redirect('add_dashboard')


@login_required
def add_office_visit(request):
    if request.method == 'POST':
        form = OfficeVisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.user = request.user
            visit.save()
            messages.success(request, "Office Visit added successfully.")
            return redirect('office_visit_list')
        else:
            messages.error(request, "There were errors in your form.")
    return redirect('add_dashboard')


@login_required
def add_college_visit(request):
    if request.method == 'POST':
        form = CollegeVisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.user = request.user
            visit.save()
            messages.success(request, "College/School Visit added successfully.")
            return redirect('college_visit_list')
        else:
            messages.error(request, "There were errors in your form.")
    return redirect('add_dashboard')


#  EDIT FORMS 

@login_required
def edit_office_visit(request, id):
    visit = get_object_or_404(OfficeVisit, id=id)
    if request.user.is_superuser or visit.user == request.user:
        if request.method == 'POST':
            form = OfficeVisitForm(request.POST, instance=visit)
            if form.is_valid():
                # Check if any changes were made
                if form.has_changed():
                    form.save()
                    messages.success(request, "Office Visit updated successfully.")
                else:
                    messages.info(request, "No changes were made to the office visit.")
                return redirect('office_visit_list')
            else:
                messages.error(request, "There were errors in your form. Please check the fields below.")
        else:
            form = OfficeVisitForm(instance=visit)
        return render(request, 'pages/staff/edit_office_visit.html', {'form': form, 'visit': visit})
    else:
        messages.error(request, "You are not authorized to edit this.")
        return redirect('office_visit_list')


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
