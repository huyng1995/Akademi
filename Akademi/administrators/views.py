from django.shortcuts import render, get_object_or_404, redirect
from user.models import UserCourse
from administrators.forms import CourseForm
from django.utils.timezone import now

# Create your views here.
def admin_dashboard(request):
    return render(request, 'administrators/admin_dashboard.html')

def admin_courses_manage(request):
    courses = UserCourse.objects.all()
    return render(request, 'administrators/admin_courses_manage.html', {'courses': courses})

def admin_professors(request):
    return render(request, 'administrators/admin_professors.html')

def admin_students(request):
    return render(request, 'administrators/admin_students.html')

# def admin_courses_create(request):
#     return render(request, 'administrators/admin_courses_create.html')

def admin_professors_create(request):
    return render(request, 'administrators/admin_professors_create.html')

def admin_students_create(request):
    return render(request, 'administrators/admin_students_create.html')

def admin_courses(request):
    return render(request, 'administrators/admin_courses.html')


# Create your views here.
def index(request):
    return render(request, 'administrators/index.html')

def base(request):
    return render(request, 'base.html')


# View course details
def course_detail(request, course_id):
    course = get_object_or_404(UserCourse, course_id=course_id)
    return render(request, 'administrators/admin_courses_view_details.html', {'course': course})

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_courses_manage')
        else:
            print(form.errors)  # <-- Print form errors for debugging
    else:
        form = CourseForm()
    return render(request, 'administrators/admin_courses_create.html', {'form': form})


# Edit an existing course
def edit_course(request, course_id):
    course = get_object_or_404(UserCourse, course_id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin_courses_manage')
    else:
        form = CourseForm(instance=course)
    return render(request, 'administrators/admin_course_form.html', {'course': course, 'form': form})

# Delete a course
def delete_course(request, course_id):
    course = get_object_or_404(UserCourse, course_id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('admin_courses_manage')
    return render(request, 'administrators/admin_confirm_delete.html', {'course': course})

