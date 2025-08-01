# dashboard/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard_home'),
    # path('home/', dashboard_view, name='home'),  # change this line!


]
