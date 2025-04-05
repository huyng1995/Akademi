from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_dashboard, name='students_dashboard'),
    path('students_logout/', views.students_logout, name='students_logout'),
    path('students_update_avatar/', views.students_update_avatar, name='students_update_avatar'),
]