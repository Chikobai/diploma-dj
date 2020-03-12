from django.contrib import admin

from .models import Lesson, VideoLesson, Question, Answer


class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    filter_horizontal = ('questions', 'videos')


admin.site.register(Lesson, LessonAdmin)
admin.site.register(VideoLesson)
admin.site.register(Question)
admin.site.register(Answer)
