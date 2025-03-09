from django.shortcuts import render

# Create your views here.
def professors_dashboard(request):
    return render(request, 'professors/professors_dashboard.html')