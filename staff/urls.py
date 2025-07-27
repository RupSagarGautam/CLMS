from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Main Page
    path('', views.visit_dashboard, name='visit_dashboard'),

    # Add Forms (POST Requests)
    path('add/client/', views.add_client_visit, name='add_client'),
    path('add/online/', views.add_online_class, name='add_online'),
    path('add/office/', views.add_office_visit, name='add_office'),
    path('add/college/', views.add_college_visit, name='add_college'),

    # View Lists
    path('client-visit/list/', views.client_visit_list, name='client_visit_list'),
    path('online-class/list/', views.online_class_list, name='online_class_list'),  # ✅ Add this

    # Delete Views
    path('delete/client/<int:id>/', views.delete_client_visit, name='delete_client'),
    path('delete/online/<int:id>/', views.delete_online_class, name='delete_online'),  # ✅ Add this
]
