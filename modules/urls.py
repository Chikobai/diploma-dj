from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModuleViewSet

router = DefaultRouter()
router.register(r'course/(?P<course_id>.+)/modules', ModuleViewSet, "modules")

urlpatterns = [
    path('', include(router.urls)),
]
