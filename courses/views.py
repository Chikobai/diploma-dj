from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, OrderList, CourseCategory, Skill
from .permissions import IsOwnerOrReadOnly
from .serializers import CourseSerializer, CourseCategorySerializer, \
    SkillSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_queryset(self):

        category = self.request.query_params.get("category_id", None)
        if category is not None:
            return Course.objects.filter(category__id=category)
        else:
            return Course.objects.all()


class MyCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_queryset(self):
        orders = OrderList.objects.filter(owner_id=self.request.user.pk)
        queryset = list()
        for item in orders:
            queryset.append(item.course)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class JoinCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response_data = {}
        user = request.user
        id = request.data['course_id']
        try:
            course = Course.objects.get(id=id)
        except ObjectDoesNotExist:
            course = None

        if course is None:
            response_data['success'] = False
            response_data['message'] = 'Данный обьект не существует'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        order, created = OrderList.objects.get_or_create(owner_id=user.id, course_id=id)

        if created:
            response_data['success'] = True
            response_data['message'] = 'Все успешно сохранено'
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data['success'] = False
            response_data['message'] = 'Данный обьект уже имеется'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


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