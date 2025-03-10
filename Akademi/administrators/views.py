from django.shortcuts import render

# Create your views here.
def admin_dashboard(request):
    return render(request, 'administrators/admin_dashboard.html')

def admin_courses(request):
    return render(request, 'administrators/admin_courses.html')

def admin_professors(request):
    return render(request, 'administrators/admin_professors.html')

def admin_students(request):
    return render(request, 'administrators/admin_students.html')

def admin_courses_create(request):
    return render(request, 'administrators/admin_courses_create.html')

def admin_professors_create(request):
    return render(request, 'administrators/admin_professors_create.html')

def admin_students_create(request):
    return render(request, 'administrators/admin_students_create.html')