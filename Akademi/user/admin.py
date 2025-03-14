from django.contrib import admin
from .models import Student
from .models import Professor
from .models import Department
from .models import Major
from .models import Classroom
from .models import Semester
from .models import Course
from .models import Enrollment_History
from .models import Current_Courses


# Register your models here.
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Department)
admin.site.register(Major)
admin.site.register(Classroom)
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Enrollment_History)
admin.site.register(Current_Courses)
