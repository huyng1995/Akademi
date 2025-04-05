from django import forms
from user.models import UserCourse


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
        fields = ['subject_name', 'subject', 'professor', 'room', 'semester', 'isavailable', 'start_time', 'end_time', 'day']
