from rest_framework import serializers
from .models import Lesson, Question, VideoLesson


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLesson
        fields = ['id', 'video_url', 'order_num', ]


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
        count, passed = 0, 0
        questions = obj.questions.all()
        videos = obj.videos.all()
        count += questions.count() + videos.count()

        return {
            'count': count,
            'passed': passed
        }


class LessonSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    videos = VideoLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'time', 'questions', 'videos']
