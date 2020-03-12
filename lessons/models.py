from django.db import models
from modules.models import Module


class VideoLesson(models.Model):
    video_url = models.TextField(default='')
    order_num = models.IntegerField(default=1)


class Question(models.Model):
    text = models.TextField(default='')
    order_num = models.IntegerField(default=1)


class Answer(models.Model):
    text = models.TextField(default='')
    is_true = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)


class Lesson(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(default='')
    time = models.CharField(max_length=50, blank=True, default='')

    questions = models.ManyToManyField(Question, related_name='questions')
    videos = models.ManyToManyField(VideoLesson, related_name='videos')
    module = models.ForeignKey(Module, related_name='lesson_module', on_delete=models.CASCADE)



