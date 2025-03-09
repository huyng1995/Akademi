from django.shortcuts import render

# Create your views here.
def students_dashboard(request):
    return render(request, 'students/students_dashboard.html')