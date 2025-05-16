from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string

from django.core.mail import EmailMessage
from django.utils.timezone import now


# Send verification mail to user

def verification_email_send(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))

    current_site = get_current_site(request)

    verification_link = f"http://{current_site.domain}/users/verify/{uid}/{token}"
    email_sub = "Verify your email"
    context =  {
            "user": user, 
            "verification_link": verification_link,
            "email_type": "verification",
            "now": now()
    }


    email_body = render_to_string("users/email_verification.html", context)

    email = EmailMessage(
        subject = email_sub,
        body = email_body,
        from_email= settings.EMAIL_HOST_USER,
        to=[user.email]
    )

    email.content_subtype ="html"
    email.send()


# Send mail to reset user's password

def password_reset_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))

    current_site = get_current_site(request)

    verification_link = f"http://{current_site.domain}/users/confirm-password-reset/{uid}/{token}"

    email_sub = "Reset your password"
    context =  {
            "user": user,
            "verification_link": verification_link,
            "email_type": "password-reset",
            "now": now()
    }
    email_body = render_to_string("users/email_verification.html", context)

    email = EmailMessage(
        subject = email_sub,
        body = email_body,
        from_email= settings.EMAIL_HOST_USER,
        to=[user.email]
    )

    email.content_subtype ="html"
    email.send()