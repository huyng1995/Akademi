from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from user.models import UserStudent
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from user.decorators import student_required
from django.shortcuts import get_object_or_404
from user.models import UserCourse, UserCurrentCourses, UserProfessor, UserStudent, UserSemester, UserStudentCart
from datetime import date
from django.utils import timezone
from django.contrib import messages


# Create your views here.
@student_required
def students_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = UserStudent.objects.get(student_id=student_id)

    today = date.today()
    active_semester = UserSemester.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).first()

    current_courses = UserCurrentCourses.objects.filter(
        student=student,
        semester=active_semester,
        isdropped=False
    ).select_related('course__professor', 'course__room', 'course__semester')

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

@student_required
def course_search(request):
    
    student_id = request.session.get('student_id')
    student = get_object_or_404(UserStudent, student_id=student_id)

    # Include current and future semesters (that are active)
    today = date.today()
    future_semesters = UserSemester.objects.filter(
        end_date__gte=today,  # includes current and future
        is_active=True
    ).order_by('start_date')

    # Get current enrolled and cart course IDs
    enrolled_ids = UserCurrentCourses.objects.filter(
        student=student,
        isdropped=False
    ).values_list('course_id', flat=True)

    cart_ids = UserStudentCart.objects.filter(
        student=student
    ).values_list('course_id', flat=True)

    excluded_ids = list(enrolled_ids) + list(cart_ids)

    # Get search courses excluding already enrolled or in cart
    search_courses = UserCourse.objects.filter(
        semester__in=future_semesters,
        isavailable=True
    ).exclude(course_id__in=excluded_ids).select_related('semester', 'professor', 'room')

    # Get courses enrolled for sidebar
    today = date.today()
    active_semester = UserSemester.objects.filter(start_date__lte=today, end_date__gte=today).first()

    current_courses = UserCurrentCourses.objects.filter(
        student=student,
        semester=active_semester,
        isdropped=False
    ).select_related('course')

    courses = [entry.course for entry in current_courses]

    return render(request, 'students/course_search.html', {
        'student': student,
        'courses': courses,  # enrolled courses for sidebar
        'search_courses': search_courses,
        'future_semesters': future_semesters,
    })

@student_required
def course_cart(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(UserStudent, student_id=student_id)

    today = date.today()
    active_semester = UserSemester.objects.filter(start_date__lte=today, end_date__gte=today).first()

    current_courses = UserCurrentCourses.objects.filter(
        student=student,
        semester=active_semester,
        isdropped=False
    ).select_related('course')

    courses = [entry.course for entry in current_courses]

    cart_items = UserStudentCart.objects.filter(student=student).select_related('course__professor', 'course__room', 'course__semester')

    return render(request, 'students/course_cart.html', {
        'cart_items': cart_items,
        'student': student,
        'courses': courses,
    })

@student_required
def add_to_cart(request, course_id): 
    student = UserStudent.objects.get(student_id=request.session['student_id'])
    course = get_object_or_404(UserCourse, pk=course_id)

    cart_item, created = UserStudentCart.objects.get_or_create(student=student, course=course)
    if created:
        messages.success(request, f"{course.course_name} has been added to your cart.")
    else:
        messages.info(request, f"{course.course_name} is already in your cart.")

    return redirect('course_search')

@student_required
def remove_from_cart(request, course_id):
    student = UserStudent.objects.get(student_id=request.session['student_id'])
    course = get_object_or_404(UserCourse, course_id=course_id)
    UserStudentCart.objects.filter(student=student, course_id=course_id).delete()
    messages.success(request, f"{course.course_name} has been removed from your cart.")
    return redirect('course_cart')

@student_required
def enroll_course(request, course_id):
    student = UserStudent.objects.get(student_id=request.session['student_id'])
    course = get_object_or_404(UserCourse, pk=course_id)
    semester = course.semester

    # Enroll
    UserCurrentCourses.objects.create(
        student=student, course=course, semester=semester,
        date_enrolled=timezone.now(), 
        isdropped=False
    )

    # Remove from cart
    UserStudentCart.objects.filter(student=student, course=course).delete()

    # Add confirmation message
    messages.success(request, f"{course.course_name} has been successfully enrolled.")
    
    return redirect('students_dashboard')



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