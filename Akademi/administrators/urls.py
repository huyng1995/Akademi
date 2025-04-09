from django.urls import path
from . import views

urlpatterns = [
    # Main admin paths
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('calendar/events/', views.get_calendar_events, name='calendar_events'),
    path('calendar/events/create/', views.create_event, name='create_event'),
    path('semester/create/', views.create_semester, name='create_semester'),

    path('manage_courses/list/', views.admin_courses_manage, name='admin_courses_manage'),
    path('manage_professors/list/', views.admin_professors_manage, name='admin_professors_manage'),
    path('students/', views.admin_students, name='admin_students'),

    # Admin course create (corrected)
    # path('courses_create/admin/', views.admin_courses_create, name='admin_courses_create'),
    path('courses_create/', views.create_course, name='create_course'),

    path('manage_courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('manage_courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('manage_courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),

    # Admin professor paths
    path('professor_create', views.create_professor, name='create_professor'),
    path('manage_professors/<int:professor_id>/', views.professor_detail, name='professor_detail'),
    path('manage_professors/<int:professor_id>/edit/', views.edit_professor, name='edit_professor'),
    path('manage_professors/<int:professor_id>/delete/', views.delete_professor, name='delete_professor'),

    # Admin student
    path('students_create/', views.admin_students_create, name='admin_students_create'),

    path('logout/', views.administrators_logout, name='logout'),
    path('update-avatar/', views.update_avatar, name='update_avatar'),
]
