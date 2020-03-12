from django.conf.urls import url
from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, user_confirm

router = DefaultRouter()
router.register('auth', UserViewSet, 'user')

urlpatterns = [
    re_path(r'', include(router.urls)),
    url(r'^user/confirm/(?P<id>\w+)$', user_confirm, name='user_confirm'),
]