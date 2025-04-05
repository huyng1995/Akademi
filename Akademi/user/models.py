# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdministratorsCalendarevent(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'administrators_calendarevent'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class AdminProfile(models.Model):
    avatar = models.CharField(max_length=100)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_adminprofile'


class UserClassroom(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f'Classroom: {self.room_name} {self.room_id}'

    class Meta:
        managed = False
        db_table = 'user_classroom'


class UserCourse(models.Model):
    course_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey('UserSubject', models.DO_NOTHING, blank=True, null=True)
    professor = models.ForeignKey('UserProfessor', models.DO_NOTHING, blank=True, null=True)
    room = models.ForeignKey(UserClassroom, models.DO_NOTHING, blank=True, null=True)
    semester = models.ForeignKey('UserSemester', models.DO_NOTHING, blank=True, null=True)
    subject_name = models.CharField(max_length=50)
    isavailable = models.BooleanField(db_column='isAvailable')  # Field name made lowercase.
    start_time = models.TextField()
    end_time = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self): #convert data stored in the model into readable info
        return f'{self.subject_name} {self.course_id}'

    class Meta:
        managed = False
        db_table = 'user_course'


class UserCurrentCourses(models.Model):
    current_course_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('UserStudent', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(UserCourse, models.DO_NOTHING, blank=True, null=True)
    semester = models.ForeignKey('UserSemester', models.DO_NOTHING, blank=True, null=True)
    date_enrolled = models.DateTimeField()
    isdropped = models.BooleanField(db_column='isDropped')  # Field name made lowercase.

    def __str__(self):
        return f'{self.student}: {self.course.subject_name}'


    class Meta:
        managed = False
        db_table = 'user_current_courses'


class UserEnrollmentHistory(models.Model):
    enrollment_history_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('UserStudent', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(UserCourse, models.DO_NOTHING, blank=True, null=True)
    semester = models.ForeignKey('UserSemester', models.DO_NOTHING)
    grade = models.CharField(max_length=3, blank=True, null=True)
    course_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.student}: {self.course_name}, {self.semester.term} {self.semester.academic_year}'


    class Meta:
        managed = False
        db_table = 'user_enrollment_history'
        unique_together = (('student', 'course', 'semester'),)


class UserMajor(models.Model):
    major_id = models.AutoField(primary_key=True)
    major_name = models.CharField(max_length=50)

    def __str__(self):
        return self.major_name


    class Meta:
        managed = False
        db_table = 'user_major'


class UserProfessor(models.Model):
    professor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    date_created = models.DateField()
    major = models.ForeignKey(UserMajor, models.DO_NOTHING, blank=True, null=True)
    avatar = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self): #convert data stored in the model into readable info
        return f'Professor: {self.first_name} {self.last_name} {self.professor_id}'

    class Meta:
        managed = False
        db_table = 'user_professor'


class UserSemester(models.Model):
    semester_id = models.PositiveIntegerField(primary_key=True)
    academic_year = models.CharField(max_length=10)
    term = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(blank=True, null=True)

    def __str__(self): #convert data stored in the model into readable info
        return f'Semester: {self.term} {self.academic_year} '

    class Meta:
        managed = False
        db_table = 'user_semester'


class UserStudent(models.Model):
    student_id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    enrollment_date = models.DateField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    total_units = models.IntegerField()
    date_created = models.DateField()
    email = models.CharField(max_length=100)
    gpa = models.FloatField()
    avatar = models.CharField(max_length=100, blank=True, null=True)
    major = models.ForeignKey(UserMajor, models.DO_NOTHING, blank=True, null=True)
    grade_level = models.CharField(max_length=10)

    def __str__(self): #convert data stored in the model into readable info
        return f'Student: {self.first_name} {self.last_name} {self.student_id}'

    class Meta:
        managed = False
        db_table = 'user_student'


class UserSubject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    major = models.ForeignKey(UserMajor, models.DO_NOTHING, blank=True, null=True)
    subject_course_number = models.BinaryField()
    subject_name = models.CharField(max_length=50)
    is_active = models.IntegerField()

    def __str__(self):
        return f'{self.subject_course_number}: {self.subject_name}'

    class Meta:
        managed = False
        db_table = 'user_subject'
