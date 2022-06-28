from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from Assignment2.views import Index, CourseViewSet, SemesterViewSet, LecturerViewSet, ClassViewSet, StudentViewSet, \
    StudentEnrollmentViewSet, CustomAuthToken

router = DefaultRouter()
router.register('course',CourseViewSet,"course")
router.register('semester',SemesterViewSet,"semester")
router.register('lecturer',LecturerViewSet,"lecturer")
router.register('class',ClassViewSet,"class")
router.register('student',StudentViewSet,"student")
router.register('studentEnollment',StudentEnrollmentViewSet,"studentEnrollment")


urlpatterns = [
    path('', Index, name="home"),
    path('api/', include(router.urls)),
    path('auth/',obtain_auth_token),
    path('login/', CustomAuthToken.as_view()),
]


