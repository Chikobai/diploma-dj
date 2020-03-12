from django.conf import settings
from django.db import models
from courses.models import Course


class UrlType(models.Model):
    url_name = models.CharField(max_length=100, blank=True, default='')


class PostType(models.Model):
    post_type = models.CharField(max_length=100, blank=True, default='')


class Post(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(default='')

    url = models.TextField(default='')
    date = models.DateTimeField(blank=False, null=True)

    url_type = models.ForeignKey(UrlType, related_name='url_types', on_delete=models.CASCADE)
    post_type = models.ForeignKey(PostType, related_name='post_types', on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='parcels', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='courses', on_delete=models.CASCADE)

    date_create = models.DateTimeField(auto_now=True)
    date_update = models.DateTimeField(auto_now_add=True)
    viewed = models.IntegerField(default=0)

