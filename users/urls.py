from django.conf.urls import url
from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from .views import UserAuthViewSet, UserViewSet, user_confirm_view, reset_password_view, save_new_password_view

router = DefaultRouter()
router.register('auth', UserAuthViewSet, 'auth')
router.register('user', UserViewSet, 'user')

urlpatterns = [
    re_path(r'', include(router.urls)),
    url(r'^user/confirm/(?P<id>\w+)$', user_confirm_view, name='user_confirm'),
    url(r'^user/reset-password-confirm/', reset_password_view, name='reset_password'),
    url(r'^user/save-password/', save_new_password_view, name='save_password'),
]