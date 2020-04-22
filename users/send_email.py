from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail


def send_email_confirm_url(user):
    subject = 'Thank you for registering'
    message = render_to_string('users/confirm_user_email.html', {
        'user': user,
        'domain': 'http://127.0.0.1:8000/',
        'url': 'user/confirm/',
        'uid': user.pk
    })

    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email, settings.EMAIL_HOST_USER]

    send_mail(subject, message, from_email, to_list, fail_silently=False)


def send_reset_password_url(user, request=None):
    subject = 'Diploma.kz Reset Password'
    message = render_to_string(
        template_name='users/reset_password_email.html',
        request=request,
        context={
        'user': user,
        'domain': 'http://127.0.0.1:8000/',
        'url': 'user/reset-password-confirm/',
        'uid': user.pk
        }
    )
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email, settings.EMAIL_HOST_USER]

    send_mail(subject, "message", from_email, to_list, fail_silently=False, html_message=message)