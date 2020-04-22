
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from datetime import datetime

from lessons.models import LessonTaker, Response as UserResponse

from users.send_email import send_reset_password_url
from .models import User
from .serializers import (LoginSerializer, RegistrationSerializer, ResetPasswordSerializer)


class UserAuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.data['success']:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
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

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        user = request.user
        user.last_token_expired = datetime.now()
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def refresh(self, request):
        user = request.user
        user.last_token_expired = datetime.now()
        user.save()
        response_data = dict()
        response_data['token'] = user.token
        return Response(response_data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'], permission_classes=[permissions.BasePermission])
    # def access(self, request):
    #     token = request.user.token
    #     return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def statistics(self, request):
        user = request.user
        takers = LessonTaker.objects.filter(user=user)
        user_responses = UserResponse.objects.filter(lesson_taker__in=takers)
        data = dict()
        correct = 0
        for resp in user_responses:
            if resp.answer.is_true:
                correct += 1
        data['count'] = len(user_responses)
        data['passed'] = correct
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='change-password', permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        user = request.user
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.set_password(serializer.data.get("new_password"))
                user.last_token_expired = datetime.now()
                user.save()
                response = dict()
                response['message_kz'] = 'Password satty ozgertildi'
                response['message_ru'] = 'Password успешно изменен'
                response['success'] = True
                response['token'] = user.token
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='reset-password',
            permission_classes=[permissions.AllowAny])
    def reset_password(self, request):
        email = request.data.get('email', None)
        if email is None:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"email": ["account with this email exists."]}, status=status.HTTP_400_BAD_REQUEST)

        send_reset_password_url(user,request)
        response = dict()
        response['message_kz'] = 'Сіздің электронды жәшігіңізге құпия сөзді алмастыру сілтемесі жіберілді'
        response['message_ru'] = 'Вам отпралено ссылка изменеие пароля в электронную почту.'
        response['success'] = True
        return Response(response, status=status.HTTP_200_OK)


def user_confirm_view(request, id):
    user = User.objects.get(pk=id)
    user.email_verified = True
    user.save()
    return render(request, 'users/confirm_user.html', {'user': user})


@csrf_exempt
def reset_password_view(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        return render(request, 'users/reset_password.html', {'user': user_id})
    else:
        return render(request, 'users/confirm_user.html')


@csrf_exempt
def save_new_password_view(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id", None)
        password1 = request.POST.get("password1", "")
        print(user_id)
        print(password1)
        if user_id is None:
            return HttpResponse('This page does not exist.')
        try:
            user = User.objects.get(pk=user_id)
            user.set_password(password1)
            user.last_token_expired = datetime.now()
            user.save()
            return render(request, 'users/confirm_user.html')
        except User.DoesNotExist:
            return HttpResponse('This page does not exist.')

    else:
        return HttpResponse('This page does not exist.')