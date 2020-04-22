from django.contrib.auth.base_user import BaseUserManager
from users.send_email import send_email_confirm_url


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
        send_email_confirm_url(user)
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
