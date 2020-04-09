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

    questions = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'time', 'videos' ,'questions']

    def get_videos(self, obj):
        response_data = list()
        videos = VideoLesson.objects.filter(lesson=obj)
        for video in videos:
            values = dict()
            values["id"] = video.pk
            values["video_url"] = video.video_url
            values["order"] = video.order
            response_data.append(values)
        return response_data

    def get_questions(self, obj):
        response_data = list()
        questions = Question.objects.filter(lesson=obj)
        for i in range(questions.count()):
            question = questions[i]
            values = dict()
            values["id"] = question.pk
            values["label"] = question.label
            values["order"] = question.order
            response_data.append(values)
        return response_data
