# dashboard/urls.py
from django.urls import path
from .views import dashboard_view  # remove import of `home`
from cms import views as cms_views

urlpatterns = [
    path('', dashboard_view, name='dashboard_home'),
    # path('home/', dashboard_view, name='home'),  # change this line!


]
