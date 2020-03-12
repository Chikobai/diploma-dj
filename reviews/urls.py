from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet

router = DefaultRouter()
router.register(r'course/(?P<course_id>.+)/reviews', ReviewViewSet, "reviews")

urlpatterns = [
    path('', include(router.urls)),
]
