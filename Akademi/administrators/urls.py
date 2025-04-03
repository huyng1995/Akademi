from django.urls import path
from . import views

urlpatterns = [
    # Main admin paths
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('calendar/events/', views.get_calendar_events, name='calendar_events'),
    path('calendar/events/create/', views.create_event, name='create_event'),

    path('manage_courses/list/', views.admin_courses_manage, name='admin_courses_manage'),

    path('professors/', views.admin_professors, name='admin_professors'),
    path('students/', views.admin_students, name='admin_students'),

    # Admin course create (corrected)
    # path('courses_create/admin/', views.admin_courses_create, name='admin_courses_create'),
    path('courses_create/', views.create_course, name='create_course'),

    path('manage_courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('manage_courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('manage_courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),

    # Admin professor and student create paths
    path('professors_create/', views.admin_professors_create, name='admin_professors_create'),
    path('students_create/', views.admin_students_create, name='admin_students_create'),
]
