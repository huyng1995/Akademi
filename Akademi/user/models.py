from django.db import models

# Create your models here.


class Department(models.Model):
    dept_id = models.PositiveIntegerField(primary_key=True)  # Set primary_key=True
    dept_name = models.CharField(max_length=50)

    def __str__(self): #convert data stored in the model into readable info
        return f'Department: {self.dept_name} {self.dept_id} '
    
class Major(models.Model):
    major_id = models.PositiveIntegerField(primary_key=True)  # Set primary_key=True
    department_id = models.ForeignKey(Department, on_delete=models.SET_NULL, null = True)
    major_name = models.CharField(max_length=50)
    
    def __str__(self): #convert data stored in the model into readable info
        return f'Major: {self.major_name} {self.major_id} '
    
class Classroom(models.Model):
    room_id = models.PositiveIntegerField(primary_key=True)  # Set primary_key=True
    room_name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    def __str__(self): #convert data stored in the model into readable info
        return f'Classroom: {self.room_name} {self.room_id} '


class Student(models.Model): #create a class called student that will inherate from models
    student_id = models.PositiveIntegerField(primary_key=True)  # Set primary_key=True
    major_id = models.ForeignKey(Major, on_delete=models.SET_NULL, null = True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    enrollment_date = models.DateField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    total_units = models.FloatField()
    create_at = models.DateField()
    grade_level = models.FloatField()
    email = models.EmailField(max_length=100)
    gpa = models.FloatField()


    def __str__(self): #convert data stored in the model into readable info
        return f'Student: {self.first_name} {self.last_name} {self.student_id}'
    

class Professor(models.Model): #create a class called professor that will inherate from models
    professor_id = models.PositiveIntegerField(primary_key=True)  # Set primary_key=True
    department_id = models.ForeignKey(Department, on_delete=models.SET_NULL, null = True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    create_at = models.DateField()


    def __str__(self): #convert data stored in the model into readable info
        return f'Professor: {self.first_name} {self.last_name} {self.professor_id}'
    



class Semester(models.Model):

    TERM_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    ]

    semester_id = models.PositiveIntegerField(primary_key=True)  # Set primary_key=True
    student_id = models.ForeignKey(Student, on_delete=models.SET_NULL, null = True)
    academic_year = models.CharField(max_length=10, choices = TERM_CHOICES)
    term = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self): #convert data stored in the model into readable info
        return f'Semester: {self.term} {self.academic_year} '

class Course(models.Model):
    course_id = models.PositiveIntegerField(primary_key=True)  # Set primary_key=True
    major_id = models.ForeignKey(Major, on_delete=models.SET_NULL, null = True)
    professor_id = models.ForeignKey(Professor, on_delete=models.SET_NULL, null = True)
    room_id = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null = True)
    semester_id = models.ForeignKey(Semester, on_delete=models.SET_NULL, null = True)
    course_name = models.CharField(max_length=50)
    isAvailable = models.BooleanField(default=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def __str__(self): #convert data stored in the model into readable info
        return f'Course: {self.course_name} {self.course_id} '

class Enrollment_History(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.SET_NULL, null = True)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True)
    semester = models.CharField(max_length=10)
    grade = models.CharField(max_length = 3, blank = True, null = True)

    class Meta:
        unique_together = ['student_id', 'course_id', 'semester']  # A student cannot enroll in the same course twice in a semester

    def str(self):
        return f"{Student.student.name} - {Course.course.name} ({self.semester})"
    

class Current_Courses(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.SET_NULL, null = True)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True)
    date_enrolled = models.DateTimeField()
    isDropped = models.BooleanField(default=False)
    
    def __str__(self): #convert data stored in the model into readable info
        return f'Current_Courses: {Course.course_name} {self.course_id} '