import mixins as mixins
from django.http import HttpResponse, JsonResponse
from rest_framework import status, generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from Assignment2.serializers import *
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Assignment2.models import Course, Semester, Lecturer, Class, Student, StudentEnrollment
from Assignment2.serializers import courseSerializer, semesterSerializer, lecturerSerializer, classSerializer, \
    studentSerializer, studentEnrollmentSerializer


def Index(request):
    return (HttpResponse("Hello World"))

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = courseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = semesterSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = lecturerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        lecturer = self.get_object()
        lecturer.user.delete()
        lecturer.delete()
        return Response(data='Lecturer Deleted Successfully!')

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = classSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = studentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        student = self.get_object()
        student.user.delete()
        student.delete()
        return Response(data='Student Deleted Successfully!')

class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrollment.objects.all()
    serializer_class = studentEnrollmentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        groups = self.request.user.groups.values_list('name', flat=True)
        if self.request.user.is_superuser:
            studentEnrollments = self.queryset.all()
            return studentEnrollments
        elif 'student' in groups:
            students = self.queryset.filter(student_id__user=self.request.user)
            return students
        elif 'lecturer' in groups:
            lecturers = self.queryset.filter(class_id__lecturer__user=self.request.user)
            return lecturers


    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
            return HttpResponse(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        groups = self.request.user.groups.values_list('name', flat=True)
        if self.request.user.is_superuser or 'lecturer' in groups:
            serializer.save()
            return HttpResponse(status=status.HTTP_202_ACCEPTED)
        elif 'student' in groups:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'group': user.groups.all()[0].name
        })
