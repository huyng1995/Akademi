from django.urls import path
from . import views

urlpatterns = [
    path('', views.professors_dashboard, name='professors_dashboard'),
    path('professors_logout/', views.professors_logout, name='professors_logout'),
    path('professors_update_avatar/', views.professors_update_avatar, name='professors_update_avatar'),
    path('course/<int:course_id>/', views.course_detail, name='professor_course_detail'),
    path('drop/<int:course_id>/<int:student_id>/', views.drop_student_from_course, name='drop_student_from_course'),
    path('professors/course/<int:course_id>/add/<int:student_id>/', views.add_student_to_course, name='add_student_to_course'),
] 