import time
from datetime import datetime
from courses.serializers import CourseShortSerializer
from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Post


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))

    def to_internal_value(self, value):
        ms = datetime.fromtimestamp(int(value))
        return ms


class PostSerializer(serializers.ModelSerializer):
    course = CourseShortSerializer(many=False, read_only=True)
    teacher = UserSerializer(many=False, read_only=True)

    date_create_in_sec = TimestampField(source='date_create', required=False)
    date_updated_in_sec = TimestampField(source='date_update', required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'url', 'url_type', 'date_create', 'date_update', 'date_create_in_sec',
                  'date_updated_in_sec', 'viewed', 'teacher', 'course', 'post_type']
