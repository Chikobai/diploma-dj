from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from datetime import datetime

from lessons.models import LessonTaker, Response as UserResponse

from users.send_email import send_reset_password_url, send_change_email
from .models import User
from .serializers import (LoginSerializer, RegistrationSerializer, ResetPasswordSerializer, UserSerializer)


class UserPartialUpdateView(GenericAPIView, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        # if request.user.phone != request.data['phone']:
        return self.partial_update(request, *args, **kwargs)


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
    def profile(self, request):
        user = request.user
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'], url_path='update-image', permission_classes=[permissions.IsAuthenticated])
    # def update_image(self, request):
    #     user = request.user
    #     serializer = UserSerializer(instance=user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

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

    @action(detail=False, methods=['post'], url_path='change-email',
            permission_classes=[permissions.AllowAny])
    def change_email(self, request):
        response = dict()
        if not request.user.is_authenticated:
            response['message_kz'] = 'Пайдаланушының аутентификациясы қажет'
            response['message_ru'] = 'Требуется аутентикация пользователя'
            response['success'] = False
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        current_user = request.user
        email = request.data.get('email', None)
        if email is None:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            response['message_kz'] = 'Бұл электрондық пошта мекенжайы бұрыннан бар. Жаңа электрондық пошта' \
                                     ' мекенжайын пайдаланып көріңіз.'
            response['message_ru'] = 'Этот адрес электронной почты уже существует. ' \
                                     'Попробуйте новый адрес электронной почты.'
            response['success'] = False
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            send_change_email(current_user, email, request)
            response['message_kz'] = 'Сіздің жаңа электрондық пошта мекенжайыңызға хабарлама жіберілді.'
            response['message_ru'] = 'Вам было отправлено сообщение на новый адрес электронной почты'
            response['success'] = True
            return Response(response, status=status.HTTP_200_OK)

@csrf_exempt
def email_confirm_view(request,):
    if request.method == 'POST':
        uid = request.POST.get("user_id", None)
        if uid is None:
            return HttpResponse('This page does not exist.')
        try:
            user = User.objects.get(pk=uid)
            user.email_verified = True
            user.last_token_expired = datetime.now()
            user.save()
            context = {
                'user': user,
                'message': "Ваша заявка успешно принято"
            }
            return render(request, 'users/confirm_user.html', context=context)
        except User.DoesNotExist:
            return HttpResponse('This page does not exist.')

    else:
        return HttpResponse('This page does not exist.')



@csrf_exempt
def reset_password_view(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        domain = request.POST.get("domain")
        return render(request, 'users/reset_password.html', {'user': user_id, 'domain': domain})
    else:
        return render(request, 'users/confirm_user.html')


@csrf_exempt
def save_new_password_view(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id", None)
        password1 = request.POST.get("password1", "")
        if user_id is None:
            return HttpResponse('This page does not exist.')
        try:
            user = User.objects.get(pk=user_id)
            user.set_password(password1)
            user.last_token_expired = datetime.now()
            user.save()
            context = {
                'user': user,
                'message': "Ваши данные успешно сохранены"
            }
            return render(request, 'users/confirm_user.html', context=context)
        except User.DoesNotExist:
            return HttpResponse('This page does not exist.')

    else:
        return HttpResponse('This page does not exist.')


@csrf_exempt
def change_email_confirm_view(request):
    if request.method == 'POST':
        uid = request.POST.get("user_id", None)
        email = request.POST.get("email", None)
        if uid is None:
            return HttpResponse('This page does not exist.')
        if email is None:
            return HttpResponse('This page does not exist.')
        try:
            user = User.objects.get(pk=uid)
            user.email = email
            user.last_token_expired = datetime.now()
            user.save()
            print(user.email)
            context = {
                'user': user,
                'message': "Вы успешно изменили."
            }
            return render(request, 'users/confirm_user.html', context=context)
        except User.DoesNotExist:
            return HttpResponse('This page does not exist.')

    else:
        return HttpResponse('This page does not exist.')