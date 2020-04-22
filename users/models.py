from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.core.validators import (validate_email)
from django.db import models
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(validators=[validate_email], max_length=128, unique=True)
    email_verified = models.BooleanField(default=False)

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    last_token_expired = models.DateTimeField(default=datetime.now(), blank=True)

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.last_name

    def _generate_jwt_token(self):
        exp = datetime.now() + timedelta(days=60)
        iat = self.last_token_expired
        token = jwt.encode(
            {
                'email': self.email,
                'id': self.pk,
                'iat': iat,
                'exp': exp
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token.decode("utf-8")


# class Token(models.Model):
#     user = models.OneToOneField(
#         User, related_name='auth_token',
#         on_delete=models.CASCADE
#     )
