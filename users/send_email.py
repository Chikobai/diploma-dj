from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail


def send_email_confirm_url(user):
    subject = 'Thank you for registering'
    message = render_to_string('users/send_email.html', {
        'user': user,
        'domain': 'http://127.0.0.1:8000/',
        'url': 'user/confirm/',
        'title': "Вы должны перейти на другую страницу, чтобы подтвердить электронную адресную пояту",
        'btn_text': "Подтвердить",
        'is_email_hidden': False
    })

    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email, settings.EMAIL_HOST_USER]

    send_mail(subject, "", from_email, to_list, fail_silently=False, html_message=message)


def send_reset_password_url(user, request=None):
    subject = 'Diploma.kz Reset Password'
    message = render_to_string(
        template_name='users/send_email.html',
        request=request,
        context={
            'user': user,
            'domain': 'http://127.0.0.1:8000/',
            'url': 'user/reset-password-confirm/',
            'title': "Чтобы изменить свой пароль вам необходимо перейти в другую страницу.",
            'btn_text': "Изменить",
            'is_email_hidden': False
        }
    )
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email, settings.EMAIL_HOST_USER]

    send_mail(subject, "", from_email, to_list, fail_silently=False, html_message=message)


def send_change_email(user, new_email, request=None):
    subject = 'Подтвердите изменение адреса электронной почты'
    user.email = new_email
    message = render_to_string(
        template_name='users/send_email.html',
        request=request,
        context={
            'user': user,
            'domain': 'http://127.0.0.1:8000/',
            'url': 'user/confirm-change-email/',
            'title': "Вы должны перейти на другую страницу, чтобы подтвердить изменения в вашей электронной почте",
            'btn_text': "Подтвердить",
            'is_email_hidden': True
        })

    from_email = settings.EMAIL_HOST_USER
    to_list = [new_email, settings.EMAIL_HOST_USER]

    send_mail(subject, "", from_email, to_list, fail_silently=False, html_message=message)