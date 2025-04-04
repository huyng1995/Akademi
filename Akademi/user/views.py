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

        # First, try Django superuser
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard')

        # Then try Student model
        try:
            student = UserStudent.objects.get(username=username, password=password)
            request.session['student_id'] = student.student_id
            return redirect('students_dashboard')
        except UserStudent.DoesNotExist:
            pass

        # Then try Professor model
        try:
            professor = UserProfessor.objects.get(username=username, password=password)
            request.session['professor_id'] = professor.professor_id
            return redirect('professors_dashboard')
        except UserProfessor.DoesNotExist:
            pass

        # Invalid login
        messages.error(request, 'Invalid credentials')

    return render(request, 'user/index.html')

def access_denied(request, reason=""):
    return render(request, 'user/403.html', {
        'message': "Access denied.",
        'reason': reason,
    }, status=403)