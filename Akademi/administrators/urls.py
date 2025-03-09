from django.urls import path
from administrators import views
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
]