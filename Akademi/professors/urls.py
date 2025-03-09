from django.urls import path
from . import views

urlpatterns = [
    path('', views.professors_dashboard, name='professors_dashboard'),
]