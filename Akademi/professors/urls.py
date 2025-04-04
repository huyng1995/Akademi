from django.urls import path
from . import views

urlpatterns = [
    path('', views.professors_dashboard, name='professors_dashboard'),
    path('professors_logout/', views.professors_logout, name='professors_logout'),
    path('professors_update_avatar/', views.professors_update_avatar, name='professors_update_avatar'),
] 