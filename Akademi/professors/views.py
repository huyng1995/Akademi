from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from user.models import UserProfessor
from django.http import JsonResponse
from user.decorators import professor_required

# Create your views here.
@professor_required
def professors_dashboard(request):
    professor_id = request.session.get('professor_id')
    if not professor_id:
        return redirect('login')

    professor = UserProfessor.objects.get(professor_id=professor_id)
    return render(request, 'professors/professors_dashboard.html', {'professor': professor})

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