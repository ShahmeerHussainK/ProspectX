from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from .models import UserProfile

from user.tokens import account_activation_token


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        get_profile = UserProfile.objects.get(user=user)
        get_profile.email_verified = True
        get_profile.save()
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')
