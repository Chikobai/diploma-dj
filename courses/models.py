from django.conf import settings
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    code = models.AutoField(primary_key=True)


class Course(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    title = models.CharField(max_length=100, blank=True, default='')
    info = models.TextField(default='')
    video_url = models.TextField(default='')

    rating = models.DecimalField(default=0.00, blank=True, max_digits=3, decimal_places=2)
    language = models.CharField(max_length=50, blank=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)


class CourseSkills(models.Model):
    skill = models.ForeignKey(Skill, related_name='skill_id', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course_id', on_delete=models.CASCADE)


class OrderList(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_owner', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='order_course', on_delete=models.CASCADE)
