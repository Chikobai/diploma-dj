from django.contrib import admin
from .models import Lesson, VideoLesson, Question, Answer, Response, LessonTaker


class VideoLessonInline(admin.TabularInline):
    model = VideoLesson
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    max_num = 4


class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [AnswerInline, ]
    extra = 1


class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    # filter_horizontal = ('questions', 'videos')
    inlines = [VideoLessonInline, QuestionInline, ]


class ResponseInline(admin.TabularInline):
    model = Response


class LessonTakersAdmin(admin.ModelAdmin):
    inlines = [ResponseInline,]


admin.site.register(Lesson, LessonAdmin)
admin.site.register(VideoLesson)
admin.site.register(LessonTaker, LessonTakersAdmin)
admin.site.register(Response)
admin.site.register(Answer)
