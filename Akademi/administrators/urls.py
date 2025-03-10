from django.urls import path
from administrators import views
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('courses/', views.admin_courses, name='admin_courses'),
    path('professors/', views.admin_professors, name='admin_professors'),
    path('students/', views.admin_students, name='admin_students'),
    path('courses_create/', views.admin_courses_create, name='admin_courses_create'),
    path('professors_create/', views.admin_professors_create, name='admin_professors_create'),
    path('students_create/', views.admin_students_create, name='admin_students_create'),
]