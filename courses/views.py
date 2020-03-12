from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from users.models import User
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from .serializers import CourseSerializer, MyCourseSerializer, OrderListSerializer
from .models import Course, OrderList


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