from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet

router = DefaultRouter()
router.register(r'course/modules/(?P<module_id>.+)/lessons', LessonViewSet, "lessons")

urlpatterns = [
    path('', include(router.urls)),
]
