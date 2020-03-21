from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import (LoginSerializer, RegistrationSerializer)


class UserViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.data['success']:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def registration(self, request):
        serializer = RegistrationSerializer(data=request.data)
        response_data = {}
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data['success'] = True
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data['success'] = False
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


def user_confirm(request, id):
    user = User.objects.get(pk=id)
    user.email_verified = True
    user.save()
    return render(request, 'users/confirm_user.html', {'user': user})
