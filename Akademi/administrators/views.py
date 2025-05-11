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
from user.models import UserSemester, UserClassroom, UserSubject
from datetime import date
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from user.models import AdminProfile
from user.decorators import admin_required
from django.db.models import Max
from django.contrib import messages

# Generate Dashboard Page
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

#update Avatar
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

# Logout
def administrators_logout(request):
    logout(request)  # Clears Django auth user session
    request.session.flush()  # Clears student/professor session
    return redirect('index')

# View to Get Calendar Events
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

# View to Create Calendar Event
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
        return redirect('admin_dashboard')
    
    messages.error(request, "Failed to create event!")
    return redirect('admin_dashboard')

# View to create new semester
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

#####

# Students Manage Page
def admin_students_manage(request):
    students = UserStudent.objects.filter(is_active=True)
    return render(request, 'administrators/admin_students_manage.html', {'students': students})

# Student Details
def student_detail(request, student_id):
    student = get_object_or_404(UserStudent, student_id=student_id)
    return render(request, 'administrators/admin_students_view_details.html', {'student': student})

# Student Edit
def edit_student(request, student_id):
    student = get_object_or_404(UserStudent, student_id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('admin_students_manage')
    else:
        form = StudentForm(instance=student)
    messages.success(request, f"{student.first_name} {student.last_name} was edited.")
    return render(request, 'administrators/admin_student_form.html', {'student': student, 'form': form})

# Student Delete - Soft, deactivate only
def delete_student(request, student_id):
    student = get_object_or_404(UserStudent, student_id=student_id)
    if request.method == 'POST':
        student.is_active = False
        student.save()
        messages.success(request, f"{student.first_name} {student.last_name} was deactivated.")
        return redirect('admin_students_manage')
    
    return render(request, 'administrators/admin_confirm_student_delete.html', {'student': student})

# Students Create Page
def admin_students_create(request):
    return render(request, 'administrators/admin_students_create.html')

# Student Create
@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        # Manually generate the next student ID
        max_id = UserStudent.objects.aggregate(Max('student_id'))['student_id__max'] or 10000
        next_id = max_id + 1

        # Gather all POST values
        student = UserStudent.objects.create(
            student_id=next_id,
            first_name=request.POST.get('first_name'),
            middle_name=request.POST.get('middle_name'),
            last_name=request.POST.get('last_name'),
            date_of_birth=request.POST.get('date_of_birth'),
            gender=request.POST.get('gender'),
            enrollment_date=request.POST.get('enrollment_date'),
            grade_level=request.POST.get('grade_level'),
            total_units=request.POST.get('total_units') or 0,
            gpa=request.POST.get('gpa') or 0.0,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            email=request.POST.get('email'),
            avatar=request.FILES.get('avatar'),
            is_active=True,
        )

        messages.success(request, f"Student {student.first_name} created successfully with ID {next_id}!")
        return redirect('admin_students_create')

    messages.error(request, "Failed to create student.")
    return redirect('admin_students_create')

#####

# Professors Manage Page
def admin_professors_manage(request):
    professors = UserProfessor.objects.filter(is_active=True)
    return render(request, 'administrators/admin_professors_manage.html', {'professors': professors})

# Professor Details
def professor_detail(request, professor_id):
    professor = get_object_or_404(UserProfessor, professor_id=professor_id)
    return render(request, 'administrators/admin_professor_view_details.html', {'professor': professor})

# Professor Edit
def edit_professor(request, professor_id):
    professor = get_object_or_404(UserProfessor, professor_id=professor_id)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('admin_professors_manage')
    else:
        form = ProfessorForm(instance=professor)
    messages.success(request, f"{professor.first_name} {professor.last_name} was edited.")
    return render(request, 'administrators/admin_professor_form.html', {'professor': professor, 'form': form})

# Professor Delete - Soft, deactivate only
def delete_professor(request, professor_id):
    professor = get_object_or_404(UserProfessor, professor_id=professor_id)
    if request.method == 'POST':
        professor.is_active = False
        professor.save()
        messages.success(request, f"{professor.first_name} {professor.last_name} was deactivated.")
        return redirect('admin_professors_manage')
    return render(request, 'administrators/admin_confirm_professor_delete.html', {'professor': professor})

# Professors Create Page
def admin_professors_create(request):
    return render(request, 'administrators/admin_professors_create.html')

# Professor Create
@csrf_exempt
def create_professor(request):
    if request.method == 'POST':
        try:
            UserProfessor.objects.create(
                first_name=request.POST.get('first_name'),
                middle_name=request.POST.get('middle_name'),
                last_name=request.POST.get('last_name'),
                date_of_birth=request.POST.get('date_of_birth'),
                gender=request.POST.get('gender'),
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                email=request.POST.get('email'),
                date_created=request.POST.get('date_created'),
                is_active=True  # default to active
            )

            messages.success(request, "Professor created successfully.")
            return redirect('admin_professors_manage')

        except Exception as e:
            messages.error(request, f"Error creating professor: {str(e)}")

    return render(request, 'administrators/admin_professor_create.html')

#####

# Courses Manage Page
def admin_courses_manage(request):
    courses = UserCourse.objects.filter(isavailable=True)
    return render(request, 'administrators/admin_courses_manage.html', {'courses': courses})

# Course Details
def course_detail(request, course_id):
    course = get_object_or_404(UserCourse, course_id=course_id)
    return render(request, 'administrators/admin_courses_view_details.html', {'course': course})

# Course Edit
def edit_course(request, course_id):
    course = get_object_or_404(UserCourse, course_id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin_courses_manage')
    else:
        form = CourseForm(instance=course)
    messages.success(request, f"{course.course_name} was edited.")
    return render(request, 'administrators/admin_course_form.html', {'course': course, 'form': form})

# Course Delete - Soft, deactivate only
def delete_course(request, course_id):
    course = get_object_or_404(UserCourse, course_id=course_id)
    if request.method == 'POST':
        course.isavailable = False
        course.save()
        messages.success(request, f"{course.course_name} was removed.")
        return redirect('admin_courses_manage')
    return render(request, 'administrators/admin_confirm_course_delete.html', {'course': course})

# Courses Create Page
def admin_courses_create(request):
    professors = UserProfessor.objects.filter(is_active=True)
    rooms = UserClassroom.objects.all()
    semesters = UserSemester.objects.filter(is_active=True)
    subjects = UserSubject.objects.all()

    return render(request, 'administrators/admin_courses_create.html',{
            'professors': professors,
            'rooms': rooms,
            'semesters': semesters,
            'subjects': subjects
    })

# Course Create
@csrf_exempt
def create_course(request):
    if request.method == 'POST':
        try:
            course_name = request.POST.get('course_name')
            subject_id = request.POST.get('subject') or None  # optional
            professor_id = request.POST.get('professor')
            room_id = request.POST.get('room')
            semester_id = request.POST.get('semester')
            isavailable = bool(request.POST.get('isavailable'))
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            day = request.POST.getlist('day')

            UserCourse.objects.create(
                course_name=course_name,
                subject_id=subject_id,
                professor_id=professor_id,
                room_id=room_id,
                semester_id=semester_id,
                isavailable=isavailable,
                start_time=start_time,
                end_time=end_time,
                day=day
            )

            messages.success(request, "Course created successfully!")
            return redirect('admin_courses_manage')

        except Exception as e:
            print("Error creating course:", e)
            messages.error(request, "Failed to create course. Please check your inputs.")
            return redirect('admin_courses_manage')
    else:
        return render(request, 'administrators/admin_courses_create.html')























