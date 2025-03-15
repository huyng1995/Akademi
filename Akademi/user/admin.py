from django.contrib import admin
from .models import UserStudent
from .models import UserProfessor
from .models import UserMajor
from .models import UserSubject
from .models import UserClassroom
from .models import UserSemester
from .models import UserCourse
from .models import UserEnrollmentHistory
from .models import UserCurrentCourses


# Register your models here.
admin.site.register(UserStudent)
admin.site.register(UserProfessor)
admin.site.register(UserMajor)
admin.site.register(UserSubject)
admin.site.register(UserClassroom)
admin.site.register(UserSemester)
admin.site.register(UserCourse)
admin.site.register(UserEnrollmentHistory)
admin.site.register(UserCurrentCourses)
