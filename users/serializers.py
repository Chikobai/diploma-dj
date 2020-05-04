from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User

MEDIA_BASE_URL = "https://www.pythonanywhere.com/user/usernotfound/files/home/usernotfound/"

class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'image']

    def get_image(self, obj):
        image_name = getattr(obj, 'image', None)
        if image_name == '':
            return None
        return f'{MEDIA_BASE_URL}{image_name}'



class RegistrationSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8,
                                     max_length=128,
                                     write_only=True)

    first_name = serializers.CharField(
        max_length=25,
        write_only=True)
    last_name = serializers.CharField(
        max_length=25,
        write_only=True)
    email = serializers.EmailField(
        max_length=128,
        write_only=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='This email is already associated with an account.')
        ])
    # token = serializers.CharField(read_only=True)
    success = serializers.BooleanField(read_only=True, default=False)

    def validate(self, data):
        password = data.get('password', None)
        if password is not None:
            validate_password(password)
        else:
            raise serializers.ValidationError('A password is required.')

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    success = serializers.BooleanField(read_only=True, default=False)

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            data['success'] = False
            data['message'] = 'An email address is required to log in.'

        if password is None:
            data['success'] = False
            data['message'] = 'A password is required to log in.'

        user = authenticate(username=email, password=password)

        if user is None:
            data['success'] = False
            data['message'] = 'A user with this email and password was not found.'

        elif not user.email_verified:
            data['success'] = False
            data['message'] = 'This user email not verified.'

        elif not user.is_active:
            data['success'] = False
            data['message'] = 'This user has been deactivated.'
        else:
            data['success'] = True
            data['token'] = user.token
        return data


class ResetPasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
