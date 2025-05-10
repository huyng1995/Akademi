from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_dashboard, name='students_dashboard'),
    path('students_logout/', views.students_logout, name='students_logout'),
    path('students_update_avatar/', views.students_update_avatar, name='students_update_avatar'),
    path('course/<int:course_id>/', views.student_course_detail, name='student_course_detail'),
    path('search/', views.course_search, name='course_search'),
    path('cart/', views.course_cart, name='course_cart'),
    path('cart/add/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:course_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('history/', views.enrollment_history, name='enrollment_history'),
    path('transcript/', views.student_transcript, name='student_transcript'),
]