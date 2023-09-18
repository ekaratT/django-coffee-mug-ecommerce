from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


# Use this function to send and email once...
# 1.User account(both vendor and customer) is created and need user to activate account.
# 2.The reset password form is submited.
def send_email_notification(request, user, mail_subject, template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site,
        # Generate a unique reset token
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string(template, context)
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()