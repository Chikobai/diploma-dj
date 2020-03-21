import time
from datetime import datetime
from rest_framework import serializers
from users.serializers import UserSerializer
from users.models import User
from .models import Review
from courses.models import Course


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))

    def to_internal_value(self, value):
        ms = datetime.fromtimestamp(int(value))
        return ms


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(many=False, read_only=True)

    created_in_sec = TimestampField(source='created', required=False, read_only=True)
    reviewer_id = serializers.IntegerField(write_only=True)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'rating', 'created', 'created_in_sec', 'reviewer', 'reviewer_id', 'course_id',]

    def create(self, validated_data):
        course_id = validated_data['course_id']
        reviewer_id = validated_data['reviewer_id']
        text = validated_data['text']
        rating = validated_data['rating']
        reviewer = User.objects.get(id=reviewer_id)
        course = Course.objects.get(id=course_id)

        review = Review.objects.update_or_create(reviewer=reviewer, course=course,
                                                 defaults={'text': text, 'rating': rating})
        return review
