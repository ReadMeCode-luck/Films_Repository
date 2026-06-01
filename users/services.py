from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


def send_password_reset_email(request, user):
    """
    Формирует и отправляет письмо со ссылкой для сброса пароля.

    Вызывается из users/views.py в forgot_password_view.
    Вся логика отправки живёт здесь, во views.py только вызов функции.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    protocol = 'https' if request.is_secure() else 'http'

    html_message = render_to_string(
        'emails/password_reset_email.html',
        {
            'user': user,
            'uid': uid,
            'token': token,
            'domain': domain,
            'protocol': protocol,
        }
    )

    message = EmailMultiAlternatives(
        subject='Сброс пароля — Синема Сити',
        body=(
            f'Здравствуйте, {user.username}!\n\n'
            f'Для сброса пароля перейдите по ссылке:\n'
            f'{protocol}://{domain}/accounts/reset/{uid}/{token}/\n\n'
            f'Ссылка действительна 24 часа.\n'
            f'Если вы не запрашивали сброс — просто проигнорируйте письмо.'
        ),
        from_email=None,   # берётся из DEFAULT_FROM_EMAIL в settings.py
        to=[user.email],
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()