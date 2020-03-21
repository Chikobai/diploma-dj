from django.urls import path, include
from posts.views import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, "posts")

urlpatterns = [
    path('', include(router.urls)),
]
