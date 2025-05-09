from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from user.models import UserStudent
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from user.decorators import student_required
from django.shortcuts import get_object_or_404
from user.models import UserCourse, UserCurrentCourses, UserProfessor, UserStudent, UserSemester
from datetime import date

# Create your views here.
@student_required
def students_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = UserStudent.objects.get(student_id=student_id)

    today = date.today()
    active_semester = UserSemester.objects.filter(start_date__lte=today, end_date__gte=today).first()

    current_courses = UserCurrentCourses.objects.filter(
        student=student,
        semester=active_semester,
        isdropped=False
    ).select_related('course')

    courses = [entry.course for entry in current_courses]

    return render(request, 'students/students_dashboard.html', {
        'student': student,
        'courses': courses,
        'active_semester': active_semester,
    })

@student_required
def student_course_detail(request, course_id):
    student_id = request.session.get('student_id')
    student = get_object_or_404(UserStudent, student_id=student_id)

    today = date.today()
    active_semester = UserSemester.objects.filter(start_date__lte=today, end_date__gte=today).first()

    course = get_object_or_404(UserCourse, course_id=course_id)
    professor = course.professor
    room = course.room
    
    current_courses = UserCurrentCourses.objects.filter(
        student=student,
        semester=active_semester,
        isdropped=False
    ).select_related('course')

    courses = [entry.course for entry in current_courses]

    return render(request, 'students/course_detail.html', {
        'student': student,
        'course': course,
        'professor': professor,
        'room': room,
        'courses': courses,
        'active_semester': active_semester,
    })



def students_logout(request):
    logout(request)  # Clears Django auth user session
    request.session.flush()  # Clears student/professor session
    return redirect('index')

def students_update_avatar(request):

    if request.method == 'POST' and request.FILES.get('avatar'):
        student_id = request.session.get('student_id')

        if not student_id:
            return JsonResponse({'status': 'error', 'message': 'Not logged in'}, status=401)

        student = UserStudent.objects.filter(student_id=student_id).first()
        
        if not student:
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)

        student.avatar = request.FILES['avatar']
        student.save()
        
        return JsonResponse({'status': 'success', 'avatar_url': student.avatar.url})
    
    return JsonResponse({'status': 'error'}, status=400)