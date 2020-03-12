from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from cryptography.fernet import Fernet


class UserManager(BaseUserManager):

    def sendEmailConfirm(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        if not first_name:
            raise ValueError('The given first_name must be set')

        if not last_name:
            raise ValueError('The given last_name must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.email_verified = False
        user.is_active = True
        user.save(using=self._db)

        subject = 'Thank you for registering'
        # uid = str(user.token).split('.')[2]
        message = render_to_string('users/base.html', {
            'user': user,
            'domain': 'http://127.0.0.1:8000/',
            'url': 'user/confirm/',
            'uid': user.pk
        })

        from_email = settings.EMAIL_HOST_USER
        to_list = [email, settings.EMAIL_HOST_USER]

        send_mail(subject, message, from_email, to_list, fail_silently=False)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self.sendEmailConfirm(email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
