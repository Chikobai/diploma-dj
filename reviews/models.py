from django.conf import settings
from django.db import models
from courses.models import Course


class Review(models.Model):
    text = models.TextField(default='')
    rating = models.DecimalField(default=0.00, blank=True, max_digits=3, decimal_places=2)

    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewer', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='review_course', on_delete=models.CASCADE)

    is_reviewed = models.BooleanField(default=False, null=False)
    created = models.DateTimeField(auto_now=True)
