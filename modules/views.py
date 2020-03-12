from rest_framework import viewsets, permissions

from .models import Module
from courses.models import Course
from .serializers import ModuleListSerializer, ModuleSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleListSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    http_method_names = ['get']

    # def __init__(self, *args, **kwargs):
    #     super(ModuleViewSet, self).__init__(*args, **kwargs)
    #     self.serializer_action_classes = {
    #         'list': ModuleSerializer,
    #         'retrieve': ModuleListSerializer,
    #     }

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Module.objects.filter(course=course_id)

    # def get_serializer_class(self, *args, **kwargs):
    #     """Instantiate the list of serializers per action from class attribute (must be defined)."""
    #     kwargs['partial'] = True
    #     try:
    #         return self.serializer_action_classes[self.action]
    #     except (KeyError, AttributeError):
    #         return super(ModuleViewSet, self).get_serializer_class()
