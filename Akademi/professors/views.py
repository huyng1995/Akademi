from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from user.models import UserProfessor, UserSemester
from user.models import UserCurrentCourses, UserCourse, UserStudent
from django.http import JsonResponse
from user.decorators import professor_required
from datetime import date
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Create your views here.
@professor_required
def professors_dashboard(request):
    professor_id = request.session.get('professor_id')
    if not professor_id:
        return redirect('login')

    professor = UserProfessor.objects.get(professor_id=professor_id)
    active_semester = UserSemester.objects.filter(is_active=True).first()

    courses = []
    if active_semester:
        courses = UserCourse.objects.filter(
            professor_id=professor_id,
            semester=active_semester
        )
    
    today = date.today()
    active_semester = UserSemester.objects.filter(start_date__lte=today, end_date__gte=today).first()

    return render(request, 'professors/professors_dashboard.html', {
        'professor': professor,
        'courses': courses,
        'active_semester': active_semester,
    })

@professor_required
def course_detail(request, course_id):
    course = get_object_or_404(UserCourse, course_id=course_id)

    # Get all courses for sidebar
    professor_id = request.session.get('professor_id')
    professor = UserProfessor.objects.get(professor_id=professor_id)
    active_semester = UserSemester.objects.filter(is_active=True).first()
    courses = UserCourse.objects.filter(professor_id=professor_id, semester=active_semester)

    # Get enrolled students for this course
    enrolled_records = UserCurrentCourses.objects.filter(course_id=course_id, isdropped=False)
    student_ids = enrolled_records.values_list('student_id', flat=True)
    students = UserStudent.objects.filter(student_id__in=student_ids)

    # Get all student IDs already enrolled in this course
    enrolled_ids = UserCurrentCourses.objects.filter(
        course=course,
        semester=active_semester
    ).values_list('student_id', flat=True)

    # Exclude already enrolled students
    available_students = UserStudent.objects.exclude(student_id__in=enrolled_ids)

    room = course.room

    return render(request, 'professors/course_detail.html', {
        'course': course,
        'courses': courses,
        'professor': professor,
        'room': room,
        'students': students,
        'available_students': available_students,
    })

@professor_required
def drop_student_from_course(request, course_id, student_id):
    try:
        record = UserCurrentCourses.objects.get(course_id=course_id, student_id=student_id)
        record.delete()
    except UserCurrentCourses.DoesNotExist:
        pass
    return redirect('professor_course_detail', course_id=course_id) 

def add_student_to_course(request, course_id, student_id):
    if request.method == 'POST':
        course = get_object_or_404(UserCourse, course_id=course_id)
        student = get_object_or_404(UserStudent, student_id=student_id)

        # Prevent duplicates
        existing = UserCurrentCourses.objects.filter(
            course=course,
            student=student,
            isdropped=False
        ).first()

        if not existing:
            UserCurrentCourses.objects.create(
                course=course,
                student=student,
                semester=course.semester,
                date_enrolled=timezone.now(),
                isdropped=False
            )

    return redirect('professor_course_detail', course_id=course_id)

def professors_logout(request):
    logout(request)  # Clears Django auth user session
    request.session.flush()  # Clears student/professor session
    return redirect('index')

def professors_update_avatar(request):
    print('DEBUG: method =', request.method)
    print('DEBUG: FILES =', request.FILES)
    print('DEBUG: session =', request.session.items())

    if request.method == 'POST' and request.FILES.get('avatar'):
        professor_id = request.session.get('professor_id')
        print('DEBUG: professor_id =', professor_id)
        if not professor_id:
            print('DEBUG: Student id not found')
            return JsonResponse({'status': 'error', 'message': 'Not logged in'}, status=401)

        professor = UserProfessor.objects.filter(professor_id=professor_id).first()
        
        if not professor:
            print('DEBUG: Student not found')
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)

        professor.avatar = request.FILES['avatar']
        professor.save()
        
        print('DEBUG: Avatar saved')
        return JsonResponse({'status': 'success', 'avatar_url': professor.avatar.url})
    
    print('DEBUG: Invalid request')
    return JsonResponse({'status': 'error'}, status=400)