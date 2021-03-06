from courses.models import Course
from django.db import models


class Module(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    course = models.ForeignKey(Course, related_name='module_courses', on_delete=models.CASCADE)
