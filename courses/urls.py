from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, MyCourseViewSet, JoinCourseView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, "courses")
router.register(r'mycourses', MyCourseViewSet, "mycourses")

urlpatterns = [
    path('', include(router.urls)),
    path('course/join/', JoinCourseView.as_view())
]
