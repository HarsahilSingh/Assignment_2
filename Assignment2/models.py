from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Course(models.Model):
    code = models.CharField(max_length=30, null=False, blank=False, unique=True)
    name = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list_course')


class Semester(models.Model):
    SEMESTERS = [
        ('S1', 'S1'),
        ('S2', 'S2'),
    ]
    current_year = int(datetime.now().year)
    year = models.PositiveIntegerField(validators=[MaxValueValidator(9999)], null=False, blank=False)
    semester = models.CharField(choices=SEMESTERS, max_length=2, default='S1')
    courses = models.ManyToManyField(Course, blank=True)
    def __str__(self):
        return str(self.year)+""+str(self.semester)
    def get_absolute_url(self):
        return reverse('list_semester')


class Lecturer(models.Model):
    user =models.OneToOneField(User, null= True, blank=True,on_delete=models.CASCADE )
    staffID = models.PositiveIntegerField(unique=True,null=False,blank= False)
    first_Name = models.CharField(max_length=50, null=False, blank=False)
    last_Name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    course = models.ForeignKey(Course,blank=True, null=True, on_delete=models.SET_NULL)
    dateOfBirth = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.first_Name+" " +self.last_Name
    def get_absolute_url(self):
        return reverse('list_lecturer')


class Class(models.Model):
    number = models.PositiveIntegerField(null=False, blank=False)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer,  on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse('list_classes')


class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    studentID = models.PositiveIntegerField(unique=True,null=False,blank= False)
    first_Name = models.CharField(max_length=50, null=False, blank=False)
    last_Name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    dateOfBirth = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.first_Name + " " + self.last_Name

    def get_absolute_url(self):
        return reverse('list_students')

class StudentEnrollment(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    grade = models.PositiveIntegerField(validators=[MaxValueValidator(100)], blank=True, null=True)
    enrollTime = models.DateTimeField(auto_now_add=True)
    gradeTime = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.student_id.first_Name + " " + str(self.class_id.number)

    def get_absolute_url(self):
        return reverse('list_student')
