from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModuleViewSet

router = DefaultRouter()
router.register(r'course/(?P<course_id>.+)/modules', ModuleViewSet, "modules")


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]