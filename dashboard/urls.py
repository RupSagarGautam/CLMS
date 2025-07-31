# dashboard/urls.py
from django.urls import path
from dashboard import views as d_views


urlpatterns = [
    path('', d_views.dashboard, name='dashboard'),

]
