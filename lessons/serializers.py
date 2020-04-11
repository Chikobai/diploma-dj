from rest_framework import serializers
from .models import Lesson, Question, VideoLesson, Answer, LessonTaker, Response
from operator import itemgetter


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
        user = self.context['request'].user
        questions = Question.objects.filter(lesson=obj)
        count = questions.count()

        try:
            taker = LessonTaker.objects.get(user=user, lesson=obj)
            responses = Response.objects.filter(lesson_taker=taker)
            passed = responses.count()
        except LessonTaker.DoesNotExist:
            passed = 0

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

        for question in questions:
            answers = Answer.objects.filter(question=question)
            values = dict()
            values["id"] = question.pk
            values["label"] = question.label
            values["order"] = question.order
            values["type"] = 2
            answers_data = list()
            for answer in answers:
                data = dict()
                data['id'] = answer.pk
                data['text'] = answer.text
                data['is_true'] = answer.is_true
                answers_data.append(data)

            values['answers'] = answers_data
            response_data.append(values)

        for video in videos:
            values = dict()
            values["id"] = video.pk
            values["label"] = video.video_url
            values["order"] = video.order
            values["type"] = 1
            values["answers"] = None
            response_data.append(values)

        sorted_data = sorted(response_data, key=itemgetter('order'))
        return sorted_data
