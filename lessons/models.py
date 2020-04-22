from datetime import datetime

from django.db import models
from modules.models import Module

from users.models import User


class Lesson(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(default='')
    time = models.CharField(max_length=50, blank=True, default='')

    # questions = models.ManyToManyField(Question, related_name='questions')
    # videos = models.ManyToManyField(VideoLesson, related_name='videos')
    module = models.ForeignKey(Module, related_name='lesson_module', on_delete=models.CASCADE)


class VideoLesson(models.Model):
    video_url = models.TextField(default='')
    order = models.IntegerField(default=1)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class Question(models.Model):
    label = models.TextField(default='')
    order = models.IntegerField(default=1)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class Answer(models.Model):
    text = models.TextField(default='')
    is_true = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)


class LessonTaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


class Response(models.Model):
    lesson_taker = models.ForeignKey(LessonTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.question.label