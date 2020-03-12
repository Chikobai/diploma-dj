from rest_framework import viewsets, permissions

from .models import Lesson
from .serializers import LessonSerializer, LessonShortSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']