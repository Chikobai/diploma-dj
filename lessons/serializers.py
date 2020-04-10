from rest_framework import serializers
from .models import Lesson, Question, VideoLesson, LessonTaker


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'label', 'order', ]


class VideoLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'order_num', ]


class LessonShortSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'time', 'result']

    # get lesson count
    def get_result(self, obj):
        # user = self.context['request'].user
        # count = Question.objects.filter(lesson=obj).count()
        # lesson_taker = LessonTaker.objects.get(user=user.pk, lesson=obj.pk)
        # passed = lesson_taker.correct_answers
        count, passed = 0, 0
        return {
            'count': count,
            'passed': passed
        }


class LessonSerializer(serializers.ModelSerializer):

    pages = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'time', 'pages']

    def get_pages(self, obj):
        response_data = list()
        videos = VideoLesson.objects.filter(lesson=obj)
        questions = Question.objects.filter(lesson=obj)

        for video in videos:
            values = dict()
            values["id"] = video.pk
            values["label"] = video.video_url
            values["order"] = video.order
            values["type"] = 1
            response_data.append(values)

        for i in range(questions.count()):
            question = questions[i]
            values = dict()
            values["id"] = question.pk
            values["label"] = question.label
            values["order"] = question.order
            values["type"] = 2
            response_data.append(values)

        return response_data
