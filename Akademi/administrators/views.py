from django.shortcuts import render, get_object_or_404, redirect
from administrators.forms import CourseForm, ProfessorForm, StudentForm
from django.utils.timezone import now

from django.http import JsonResponse
from .models import CalendarEvent

from django.utils.dateparse import parse_datetime

from django.views.decorators.csrf import csrf_exempt
from user.models import UserStudent
from user.models import UserProfessor
from user.models import UserCourse
from user.models import UserSemester
from datetime import date

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from user.models import AdminProfile
from user.decorators import admin_required
from django.db.models import Max
from django.contrib import messages

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

        messages.success(request, "Event created successfully!")
        # return JsonResponse({'status': 'success', 'id': event.id})
        return redirect('admin_dashboard')
    
    messages.error(request, "Failed to create event!")
    # return JsonResponse({'status': 'error'}, status=400)
    return redirect('admin_dashboard')

@csrf_exempt
def create_semester(request):
    if request.method == 'POST':
        term = request.POST.get('term')
        year = request.POST.get('academic_year')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')

        max_id = UserSemester.objects.aggregate(Max('semester_id'))['semester_id__max'] or 0
        next_id = max_id + 1

        UserSemester.objects.create(
            semester_id=next_id,
            term=term,
            academic_year=year,
            start_date=start,
            end_date=end
        )

        messages.success(request, "Semester created successfully!")
        return redirect('admin_dashboard')  # adjust to your dashboard view name

    messages.error(request, "Failed to create semester.")
    return redirect('admin_dashboard')

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

@admin_required
def admin_dashboard(request):
    today = date.today()
    active_semester = UserSemester.objects.filter(start_date__lte=today, end_date__gte=today).first()

    context = {
        'user': request.user,
        'profile': request.user.adminprofile,
        'active_semester': active_semester,
        'semester_name': str(active_semester) if active_semester else 'N/A',
        'student_count': UserStudent.objects.count(),
        'professor_count': UserProfessor.objects.count(),
        'course_count': UserCourse.objects.count(),
    }

    return render(request, 'administrators/admin_dashboard.html',context,)

@login_required(login_url='login')
def update_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar = request.FILES['avatar']
        user = request.user

        # ✅ If avatar is on the user model
        if hasattr(user, 'avatar'):
            user.avatar = avatar
            user.save()
            return JsonResponse({'status': 'success', 'avatar_url': user.avatar.url})

        # ✅ If avatar is on the adminprofile
        elif hasattr(user, 'adminprofile'):
            profile = user.adminprofile
            profile.avatar = avatar
            profile.save()
            return JsonResponse({'status': 'success', 'avatar_url': profile.avatar.url})

    return JsonResponse({'status': 'error'}, status=400)

def admin_courses_manage(request):
    courses = UserCourse.objects.all()
    return render(request, 'administrators/admin_courses_manage.html', {'courses': courses})

def admin_professors_manage(request):
    professors = UserProfessor.objects.all()
    return render(request, 'administrators/admin_professors_manage.html', {'professors': professors})

def admin_students_manage(request):
    students = UserStudent.objects.all()
    return render(request, 'administrators/admin_students_manage.html', {'students': students})

def admin_students(request):
    return render(request, 'administrators/admin_students.html')

def admin_students_create(request):
    return render(request, 'administrators/admin_students_create.html')

def admin_courses(request):
    return render(request, 'administrators/admin_courses.html')

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

# View professor details
def professor_detail(request, professor_id):
    professor = get_object_or_404(UserProfessor, professor_id=professor_id)
    return render(request, 'administrators/admin_professor_view_details.html', {'professor': professor})

# Create new professor profile
def create_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_professors_manage')
        else:
            print(form.errors)  # <-- Print form errors for debugging
    else:
        form = ProfessorForm()
    return render(request, 'administrators/admin_professor_create.html', {'form': form})

# Edit an existing professor
def edit_professor(request, professor_id):
    professor = get_object_or_404(UserProfessor, professor_id=professor_id)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('admin_professors_manage')
    else:
        form = ProfessorForm(instance=professor)
    return render(request, 'administrators/admin_professor_form.html', {'professor': professor, 'form': form})

# Soft delete a professor by deactivating
def delete_professor(request, professor_id):
    professor = get_object_or_404(UserProfessor, professor_id=professor_id)
    if request.method == 'POST':
        professor.is_active = False
        professor.save()
        return redirect('admin_professors_manage')
    return render(request, 'administrators/admin_professor_delete.html', {'professor': professor})


# View student details
def student_detail(request, student_id):
    student = get_object_or_404(UserStudent, student_id=student_id)
    return render(request, 'administrators/admin_students_view_details.html', {'student': student})


# Create a new student
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_students')
        else:
            print(form.errors)  # <-- Print form errors for debugging
    else:
        form = StudentForm()
    return render(request, 'administrators/admin_students_create.html', {'form': form})

# Edit an existing student
def edit_student(request, student_id):
    student = get_object_or_404(UserStudent, student_id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('admin_students_manage')
    else:
        form = StudentForm(instance=student)
    return render(request, 'administrators/admin_student_form.html', {'student': student, 'form': form})

# Soft delete a student by deactivating
def delete_student(request, student_id):
    student = get_object_or_404(UserStudent, student_id=student_id)
    if request.method == 'POST':
        student.is_active = False
        student.save()
        return redirect('admin_students')
    return render(request, 'administrators/admin_confirm_student_delete.html', {'student': student})

def administrators_logout(request):
    logout(request)  # Clears Django auth user session
    request.session.flush()  # Clears student/professor session
    return redirect('index')



