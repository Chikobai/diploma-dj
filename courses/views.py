from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, OrderList, CourseCategory, Skill
from .permissions import IsOwnerOrReadOnly
from .serializers import CourseSerializer, MyCourseSerializer, OrderListSerializer, CourseCategorySerializer, \
    SkillSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class MyCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = MyCourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = OrderList.objects.filter(owner_id=self.request.user.pk)
        return queryset

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MyCourseSerializer(queryset, many=True)
        return Response(serializer.data)


class JoinCourseView(APIView):

    def post(self, request):
        serializer = OrderListSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCategoryViewSet(ListModelMixin, GenericAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_paginated_response(self, data):
        return Response(data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SkillsViewSet(ListModelMixin, GenericAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]

    def get_paginated_response(self, data):
        return Response(data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)