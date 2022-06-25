from django.contrib.auth.models import Group
from rest_framework import serializers

from rest_framework.authtoken.models import Token

from Assignment2.models import *


class courseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'name']

class semesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['year', 'semester','courses']


class lecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['staffID', 'first_Name','last_Name','email','course','dateOfBirth']

        extra_Kwargs = {
            'first_Name':{
                'write_only':True,
                'required':True
            }
        }

    def create(self, validated_data):
        lecturer = Lecturer.objects.create(**validated_data)
        first_name = self.validated_data.get("first_Name")
        last_name = self.validated_data.get("last_Name")
        email = self.validated_data.get("email")

        try:
            user = User.objects.create_user(username=first_name.lower())
            user.set_password(first_name.lower())
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            lecturer_group = Group.objects.get(name='lecturer')
            user.groups.add(lecturer_group)

            lecturer.user = user
            lecturer.save()
            Token.objects.create(user=user)
            user.save()
            print('sucksex')
        except Exception as e:
            print(e)
            return e

        return lecturer



class classSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['number', 'semester','course','lecturer']


class studentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['studentID', 'first_Name','last_Name','email','dateOfBirth']

        extra_Kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }

    def create(self, validated_data):

        student = Student.objects.create(**validated_data)
        first_name = self.validated_data.get("first_Name")
        last_name = self.validated_data.get("last_Name")
        email = self.validated_data.get("email")
        dob = self.validated_data.get("dateOfBirth")
        try:
            user = User.objects.create_user(username=first_name.lower())
            user.set_password(first_name.lower())
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            student_group = Group.objects.get(name='student')
            user.groups.add(student_group)
            Token.objects.create(user=user)
            user.save()
        except Exception as e:
            print(e)
        return student


class studentEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEnrollment
        fields = ['student_id', 'class_id','grade','gradeTime']


