from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserStudent, UserProfessor

# Create your views here.

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # First, try Django superuser (admin)
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Administrator account is inactive.')
                return redirect('login')

        # Then try Student model
        try:
            student = UserStudent.objects.get(username=username, password=password)
            if not student.is_active:
                messages.error(request, 'Your student account is inactive.')
                return redirect('login')
            request.session['student_id'] = student.student_id
            return redirect('students_dashboard')
        except UserStudent.DoesNotExist:
            pass

        # Then try Professor model
        try:
            professor = UserProfessor.objects.get(username=username, password=password)
            if not professor.is_active:
                messages.error(request, 'Your professor account is inactive.')
                return redirect('login')
            request.session['professor_id'] = professor.professor_id
            return redirect('professors_dashboard')
        except UserProfessor.DoesNotExist:
            pass

        # Invalid login fallback
        messages.error(request, 'Invalid credentials')

    return render(request, 'user/index.html')

def access_denied(request, reason=""):
    return render(request, 'user/403.html', {
        'message': "Access denied.",
        'reason': reason,
    }, status=403)