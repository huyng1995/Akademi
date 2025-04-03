from django.shortcuts import render, get_object_or_404, redirect
from administrators.forms import CourseForm
from django.utils.timezone import now

import calendar
from datetime import datetime
from django.shortcuts import render

from django.http import JsonResponse
from .models import CalendarEvent
import datetime
from django.utils.dateparse import parse_datetime

from django.views.decorators.csrf import csrf_exempt
from user.models import UserStudent
from user.models import UserProfessor
from user.models import UserCourse
from user.models import UserSemester
from datetime import date

@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')
        description = request.POST.get('description', '')

        event = CalendarEvent.objects.create(
            title=title,
            start=start,
            end=end or None,
            description=description
        )

        return JsonResponse({'status': 'success', 'id': event.id})
    return JsonResponse({'status': 'error'}, status=400)

def get_calendar_events(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    events = CalendarEvent.objects.all()
    if start and end:
        events = events.filter(start__gte=start, start__lte=end)

    data = [
        {
            'title': event.title,
            'start': event.start.isoformat(),
            'end': event.end.isoformat() if event.end else None,
            'description': event.description,
        }
        for event in CalendarEvent.objects.all()
    ]
    return JsonResponse(data, safe=False)

def admin_dashboard(request):
    today = date.today()
    active_semester = UserSemester.objects.filter(start_date__lte=today, end_date__gte=today).first()

    context = {
        'semester_name': str(active_semester) if active_semester else 'N/A',
        'student_count': UserStudent.objects.count(),
        'professor_count': UserProfessor.objects.count(),
        'course_count': UserCourse.objects.count(),
    }

    return render(request, 'administrators/admin_dashboard.html',context)

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




