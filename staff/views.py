
# --- Imports: Django core, models, forms ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime
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
            contact = form.cleaned_data.get('contact_number')

            if ClientVisit.objects.filter(contact_number=contact).exists():
                messages.error(request, "Client Visit with this contact number already exists.")
                return render(request, 'pages/staff/add_dashboard.html', {
                    'client_form': form,
                    'online_form': OnlineClassInquiryForm(),
                    'office_form': OfficeVisitForm(),
                    'college_form': CollegeVisitForm(),
                })

            client_visit = form.save(commit=False)
            client_visit.user = request.user
            client_visit.save()
            messages.success(request, "Client Visit added successfully.")
            return redirect('client_visit_list')

        # Show validation errors
        return render(request, 'pages/staff/add_dashboard.html', {
            'client_form': form,
            'online_form': OnlineClassInquiryForm(),
            'office_form': OfficeVisitForm(),
            'college_form': CollegeVisitForm(),
        })

    return redirect('add_dashboard')




@login_required
def add_online_class(request):
    if request.method == 'POST':
        form = OnlineClassInquiryForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data.get('contact')
            if OnlineClassInquiry.objects.filter(contact=contact).exists():
                messages.error(request, "Online Class Inquiry with this contact number already exists.")
                return render(request, 'pages/staff/add_dashboard.html', {
                    'online_form': form,
                    'client_form': ClientVisitForm(),
                    'office_form': OfficeVisitForm(),
                    'college_form': CollegeVisitForm(),
                })
            inquiry = form.save(commit=False)
            inquiry.user = request.user
            inquiry.save()
            messages.success(request, "Online Class Inquiry added successfully.")
            return redirect('online_class_list')
        # Show validation errors
        return render(request, 'pages/staff/add_dashboard.html', {
            'online_form': form,
            'client_form': ClientVisitForm(),
            'office_form': OfficeVisitForm(),
            'college_form': CollegeVisitForm(),
        })
    return redirect('add_dashboard')



@login_required
def add_office_visit(request):
    if request.method == 'POST':
        form = OfficeVisitForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data.get('contact')

            # ✅ Check if contact already exists
            if OfficeVisit.objects.filter(contact=contact).exists():
                messages.error(request, "An Office Visit with this contact number already exists.")
                return render(request, 'pages/staff/add_dashboard.html', {
                    'office_form': form,
                    'client_form': ClientVisitForm(),
                    'online_form': OnlineClassInquiryForm(),
                    'college_form': CollegeVisitForm(),
                })

            visit = form.save(commit=False)
            visit.user = request.user
            visit.save()
            messages.success(request, "Office Visit added successfully.")
            return redirect('office_visit_list')

        # If form validation fails
        return render(request, 'pages/staff/add_dashboard.html', {
            'office_form': form,
            'client_form': ClientVisitForm(),
            'online_form': OnlineClassInquiryForm(),
            'college_form': CollegeVisitForm(),
        })
    return redirect('add_dashboard')


@login_required
def add_college_visit(request):
    if request.method == 'POST':
        form = CollegeVisitForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data.get('contact')
            if CollegeVisit.objects.filter(contact=contact).exists():
                messages.error(request, "College Visit with this contact number already exists.")
                return render(request, 'pages/staff/add_dashboard.html', {
                    'college_form': form,
                    'client_form': ClientVisitForm(),
                    'office_form': OfficeVisitForm(),
                    'online_form': OnlineClassInquiryForm(),
                })
            visit = form.save(commit=False)
            visit.user = request.user
            visit.save()
            messages.success(request, "College/School Visit added successfully.")
            return redirect('college_visit_list')
        # Show validation errors
        return render(request, 'pages/staff/add_dashboard.html', {
            'college_form': form,
            'client_form': ClientVisitForm(),
            'office_form': OfficeVisitForm(),
            'online_form': OnlineClassInquiryForm(),
        })
    return redirect('add_dashboard')

# --- Edit Views ---
@login_required
def edit_office_visit(request, id):
    """Edit an existing office visit record."""
    visit = get_object_or_404(OfficeVisit, id=id)
    if request.user.is_superuser or visit.user == request.user:
        if request.method == 'POST':
            form = OfficeVisitForm(request.POST, instance=visit)
            if form.is_valid():
                # Only save if changes were made
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

@login_required
def edit_client_visit(request, id):
    visit = get_object_or_404(ClientVisit, id=id)
    if request.user.is_superuser or visit.user == request.user:
        if request.method == 'POST':
            form = ClientVisitForm(request.POST, instance=visit)
            if form.is_valid():
                if form.has_changed():
                    form.save()
                    messages.success(request, "Client Visit updated successfully.")
                else:
                    messages.info(request, "No changes were made to the client visit.")
                return redirect('client_visit_list')
            else:
                messages.error(request, "There were errors in your form. Please check the fields below.")
        else:
            form = ClientVisitForm(instance=visit)
        return render(request, 'pages/staff/edit_client_visit.html', {'form': form, 'visit': visit})
    else:
        messages.error(request, "You are not authorized to edit this.")
        return redirect('client_visit_list')

@login_required
def edit_college_visit(request, id):
    visit = get_object_or_404(CollegeVisit, id=id)
    if request.user.is_superuser or visit.user == request.user:
        if request.method == 'POST':
            form = CollegeVisitForm(request.POST, instance=visit)
            if form.is_valid():
                if form.has_changed():
                    form.save()
                    messages.success(request, "College/School Visit updated successfully.")
                else:
                    messages.info(request, "No changes were made to the college/school visit.")
                return redirect('college_visit_list')
            else:
                messages.error(request, "There were errors in your form. Please check the fields below.")
        else:
            form = CollegeVisitForm(instance=visit)
        return render(request, 'pages/staff/edit_college_visit.html', {'form': form, 'visit': visit})
    else:
        messages.error(request, "You are not authorized to edit this.")
        return redirect('college_visit_list')

@login_required
def edit_online_class(request, id):
    inquiry = get_object_or_404(OnlineClassInquiry, id=id)
    if request.user.is_superuser or inquiry.user == request.user:
        if request.method == 'POST':
            form = OnlineClassInquiryForm(request.POST, instance=inquiry)
            if form.is_valid():
                if form.has_changed():
                    form.save()
                    messages.success(request, "Online Class Inquiry updated successfully.")
                else:
                    messages.info(request, "No changes were made to the online class inquiry.")
                return redirect('online_class_list')
            else:
                messages.error(request, "There were errors in your form. Please check the fields below.")
        else:
            form = OnlineClassInquiryForm(instance=inquiry)
        return render(request, 'pages/staff/edit_online_class.html', {'form': form, 'inquiry': inquiry})
    else:
        messages.error(request, "You are not authorized to edit this.")
        return redirect('online_class_list')


# --- List Views with Filtering (Admin) ---
@login_required
def client_visit_list(request):
    """
    List all client visits. Admins can filter by staff and date range.
    Regular staff see only their own records.
    """
    if request.user.is_superuser:
        client_visits = ClientVisit.objects.all().order_by('-date')
        
        # Filter by staff
        staff_filter = request.GET.get('staff')
        if staff_filter and staff_filter != 'all':
            client_visits = client_visits.filter(user_id=staff_filter)
        
        # Filter by date range
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                client_visits = client_visits.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                client_visits = client_visits.filter(date__lte=end_date)
            except ValueError:
                pass
        
        # Get all staff users for filter dropdown
        staff_users = User.objects.filter(is_staff=True).order_by('username')
    else:
        client_visits = ClientVisit.objects.filter(user=request.user).order_by('-date')
        staff_users = None
    
    return render(request, 'pages/staff/Client_Visit.html', {
        'client_visits': client_visits,
        'staff_users': staff_users,
        'current_filters': {
            'staff': request.GET.get('staff', ''),
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
        }
    })


@login_required
def online_class_list(request):
    """
    List all online class inquiries. Admins can filter by staff and date range.
    Regular staff see only their own records.
    """
    if request.user.is_superuser:
        online_classes = OnlineClassInquiry.objects.all().order_by('-date')
        
        # Filter by staff
        staff_filter = request.GET.get('staff')
        if staff_filter and staff_filter != 'all':
            online_classes = online_classes.filter(user_id=staff_filter)
        
        # Filter by date range
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                online_classes = online_classes.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                online_classes = online_classes.filter(date__lte=end_date)
            except ValueError:
                pass
        
        # Get all staff users for filter dropdown
        staff_users = User.objects.filter(is_staff=True).order_by('username')
    else:
        online_classes = OnlineClassInquiry.objects.filter(user=request.user).order_by('-date')
        staff_users = None
    
    return render(request, 'pages/staff/Online_Class.html', {
        'online_classes': online_classes,
        'staff_users': staff_users,
        'current_filters': {
            'staff': request.GET.get('staff', ''),
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
        }
    })


@login_required
def office_visit_list(request):
    """
    List all office visits. Admins can filter by staff and date range.
    Regular staff see only their own records.
    """
    if request.user.is_superuser:
        office_visits = OfficeVisit.objects.all().order_by('-date')
        
        # Filter by staff
        staff_filter = request.GET.get('staff')
        if staff_filter and staff_filter != 'all':
            office_visits = office_visits.filter(user_id=staff_filter)
        
        # Filter by date range
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                office_visits = office_visits.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                office_visits = office_visits.filter(date__lte=end_date)
            except ValueError:
                pass
        
        # Get all staff users for filter dropdown
        staff_users = User.objects.filter(is_staff=True).order_by('username')
    else:
        office_visits = OfficeVisit.objects.filter(user=request.user).order_by('-date')
        staff_users = None
    
    return render(request, 'pages/staff/Office_Visit.html', {
        'office_visits': office_visits,
        'staff_users': staff_users,
        'current_filters': {
            'staff': request.GET.get('staff', ''),
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
        }
    })


@login_required
def college_visit_list(request):
    """
    List all college/school visits. Admins can filter by staff and date range.
    Regular staff see only their own records.
    """
    if request.user.is_superuser:
        college_visits = CollegeVisit.objects.all().order_by('-id')
        
        # Filter by staff
        staff_filter = request.GET.get('staff')
        if staff_filter and staff_filter != 'all':
            college_visits = college_visits.filter(user_id=staff_filter)
        
        # Filter by date range
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                college_visits = college_visits.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                college_visits = college_visits.filter(date__lte=end_date)
            except ValueError:
                pass
        
        # Get all staff users for filter dropdown
        staff_users = User.objects.filter(is_staff=True).order_by('username')
    else:
        college_visits = CollegeVisit.objects.filter(user=request.user).order_by('-id')
        staff_users = None
    
    return render(request, 'pages/staff/College_SchoolVisit.html', {
        'college_visits': college_visits,
        'staff_users': staff_users,
        'current_filters': {
            'staff': request.GET.get('staff', ''),
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
        }
    })


# --- Delete ---
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
