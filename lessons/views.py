from rest_framework import viewsets, permissions
from .models import Lesson
from .serializers import LessonSerializer


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        id = self.kwargs['module_id']
        querysets = Lesson.objects.filter(module=id)
        return querysets


