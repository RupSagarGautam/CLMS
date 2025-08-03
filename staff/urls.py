# URL patterns for staff app
from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_dashboard, name='add_dashboard'),
<<<<<<< HEAD
    # Add data
=======

    # Add Data
>>>>>>> 3e7a35ee888d3205cac12d20b58f29908d0efc9e
    path('add/client/', views.add_client_visit, name='add_client'),
    path('add/online/', views.add_online_class, name='add_online'),
    path('add/office/', views.add_office_visit, name='add_office'),
    path('add/college/', views.add_college_visit, name='add_college'),
<<<<<<< HEAD
    # Edit data
=======

    # Edit Data
>>>>>>> 3e7a35ee888d3205cac12d20b58f29908d0efc9e
    path('edit/office/<int:id>/', views.edit_office_visit, name='edit_office'),
    path('edit/client/<int:id>/', views.edit_client_visit, name='edit_client'),
    path('edit/college/<int:id>/', views.edit_college_visit, name='edit_college'),
    path('edit/online/<int:id>/', views.edit_online_class, name='edit_online'),
<<<<<<< HEAD
    # View data
=======

    # View Data
>>>>>>> 3e7a35ee888d3205cac12d20b58f29908d0efc9e
    path('client-visit/list/', views.client_visit_list, name='client_visit_list'),
    path('online-class/list/', views.online_class_list, name='online_class_list'),
    path('office-visit/list/', views.office_visit_list, name='office_visit_list'),
    path('college-visit/list/', views.college_visit_list, name='college_visit_list'),
    # Delete data
    path('delete/client/<int:id>/', views.delete_client_visit, name='delete_client'),
    path('delete/online/<int:id>/', views.delete_online_class, name='delete_online'),
    path('delete/office/<int:id>/', views.delete_office_visit, name='delete_office'),
    path('delete/college/<int:id>/', views.delete_college_visit, name='delete_college'),
]
