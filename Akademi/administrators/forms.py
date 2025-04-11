from django import forms
from user.models import UserCourse, UserProfessor, UserStudent


DAYS_OF_WEEK = [
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
]

class CourseForm(forms.ModelForm):
    day = forms.ChoiceField(choices=DAYS_OF_WEEK)

    class Meta:
        model = UserCourse
        fields = ['course_name', 'subject', 'professor', 'room', 'semester', 'isavailable', 'start_time', 'end_time', 'day']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = UserProfessor
        fields = ['major', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'username', 'password', 'email', 'date_created']

class StudentForm(forms.ModelForm):

    class Meta:
        model = UserStudent
        fields = ['first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'enrollment_date', 'username', 'password', 'total_units', 'date_created', 'email', 'gpa', 'avatar', 'grade_level']

