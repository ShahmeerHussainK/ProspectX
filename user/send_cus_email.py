from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token

from django.utils.encoding import force_bytes, force_text


def sendEmail(user, ran_password, type, email_verification, current_site, role, sub_user):
    print("in my fun")
    if type == 'update':
        if role == 'Admin User':
            content = "You have changed password for your sub-user {} . Your new password is:".format(sub_user.first_name)
        else:
            content = "Your ProspectX password has been changed. Your new password is:"

    else:
        if role == 'Admin User':
            content = "ProspectX account for sub-user {} is created and password is:".format(sub_user.first_name)
        else:
            content = "Your ProspectX account is created. Your password is:"

    if email_verification:
        if role == 'Admin User':
            email_verification = 'None'
        else:
            email_verification = 'Please click on the email verification link below to confirm your Prospectx account registration,'
    else:
        email_verification = 'None'

    ctx = {
        'password': ran_password,
        'content': content,
        'email_verification': email_verification,
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }
    print(current_site.domain)
    print(ctx['token'])
    to_email_list = [user.email]
    subject = "Prospectx"
    html_message = render_to_string('user/CustomAlert.html', ctx)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, plain_message, from_email, to_email_list, html_message=html_message,
              fail_silently=False)
