import time
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from modules.models import Module
from rest_framework import serializers
from reviews.models import Review
from users.serializers import UserSerializer
from .models import Skill, Course, OrderList, CourseSkills, CourseCategory


class TimestampField(serializers.Field):

    def to_representation(self, value):
        dt = int(time.mktime(value.timetuple()))
        return dt * 1000

    def to_internal_value(self, value):
        ms = datetime.fromtimestamp(int(value))
        return ms


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['code', 'name']


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name_ru', 'name_kz']


class CourseShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'name', 'info', 'video_url']


class CourseSkillsSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSkills
        fields = ['skills']


class CourseSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    category = CourseCategorySerializer(many=False, read_only=True)
    # modules = ModuleSerializer(source='module_courses', many=True)
    user_counts = serializers.SerializerMethodField()
    module_counts = serializers.SerializerMethodField()
    is_my_course = serializers.SerializerMethodField()
    course_skills = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'name', 'info', 'video_url', 'language', 'rating', 'user_counts', 'is_my_course',
                  'module_counts',
                  'owner', 'category','is_my_course', 'course_skills']

    def get_user_counts(self, obj):
        count = OrderList.objects.filter(course=obj).count()
        return count

    def get_module_counts(self, obj):
        count = Module.objects.filter(course=obj).count()
        return count

    def get_is_my_course(self, obj):
        user = self.context['request'].user
        try:
            order = OrderList.objects.get(course=obj, owner=user)
            return True
        except OrderList.DoesNotExist:
            return False

    def get_course_skills(self, obj):
        course_skils = CourseSkills.objects.filter(course=obj)
        d = []
        for i in range(0, len(course_skils)):
            data = {
                'code': course_skils[i].skill.code,
                'name': course_skils[i].skill.name
            }
            d.append(data)
        return d

    def get_rating(self, obj):
        reviews = Review.objects.filter(course=obj)
        result = 0
        review_count = len(reviews)
        for index in range(0, review_count):
            result += reviews[index].rating

        if review_count == 0:
            return None
        return result / review_count


