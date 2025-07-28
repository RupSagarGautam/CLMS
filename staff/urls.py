from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_dashboard, name='add_dashboard'),

    # Add Data
    path('add/client/', views.add_client_visit, name='add_client'),
    path('add/online/', views.add_online_class, name='add_online'),
    path('add/office/', views.add_office_visit, name='add_office'),
    path('add/college/', views.add_college_visit, name='add_college'),

    # Edit Data
    path('edit/office/<int:id>/', views.edit_office_visit, name='edit_office'),

    # View Data
    path('client-visit/list/', views.client_visit_list, name='client_visit_list'),
    path('online-class/list/', views.online_class_list, name='online_class_list'),
    path('office-visit/list/', views.office_visit_list, name='office_visit_list'),
    path('college-visit/list/', views.college_visit_list, name='college_visit_list'),

    # Delete Data
    path('delete/client/<int:id>/', views.delete_client_visit, name='delete_client'),
    path('delete/online/<int:id>/', views.delete_online_class, name='delete_online'),
    path('delete/office/<int:id>/', views.delete_office_visit, name='delete_office'),
    path('delete/college/<int:id>/', views.delete_college_visit, name='delete_college'),
]
