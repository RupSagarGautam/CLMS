"""
URL configuration for cms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cms import views as cms_views
from clientapp import views as clientapp_views
from staff import views as staff_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cms_views.home),
    path('log-in/', cms_views.staff_login, name='staff_login'),
    path('logout/', cms_views.logoutUser, name='logout_user'),
    path('request-otp/', clientapp_views.request_otp, name='request_otp'),
    path('reset-password/', clientapp_views.reset_password, name='reset_password'),
    path('forgot-password/', clientapp_views.forgot_password, name='forgot_password'),
    path('verify-otp/', clientapp_views.verify_otp, name='verify_otp'),
    path('dashboard/', include('dashboard.urls')), 
    path('dashboard/', include('staff.urls')),
    path('home/', cms_views.home_view, name='home'),

]
