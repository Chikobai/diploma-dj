from rest_framework import serializers
from .models import Module
from lessons.models import Lesson
from lessons.serializers import LessonShortSerializer


class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ['id', 'title']


class ModuleListSerializer(serializers.ModelSerializer):

    result = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(source="lesson_module", many=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'result', 'lessons']

    # get lesson count
    def get_result(self, obj):
        lesson = Lesson.objects.filter(module=obj)
        count, passed = 0, 0
        for i in range(0, len(lesson)):
            questions = lesson[i].questions.all()
            videos = lesson[i].videos.all()
            count += questions.count() + videos.count()

        return {
            'count': count,
            'passed': passed
        }