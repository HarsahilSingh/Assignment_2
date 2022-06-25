from django.contrib import admin
from .models import Class, Student,StudentEnrollment,Semester,Course,Lecturer

admin.site.register (Class)
admin.site.register (Student)
admin.site.register (Semester)
admin.site.register (StudentEnrollment)
admin.site.register (Course)
admin.site.register (Lecturer)