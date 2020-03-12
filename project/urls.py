from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('api/v1/', include('courses.urls')),
    path('api/v1/', include('posts.urls')),
    path('api/v1/', include('lessons.urls')),
    path('api/v1/', include('modules.urls')),
    path('api/v1/', include('reviews.urls')),
]
