from user.models import UserProfile
from django.core.exceptions import PermissionDenied
from skiptrace.models import *
from django.shortcuts import render, redirect


def user_has_list_management_Permission(function):
    def wrap(request, *args, **kwargs):
        permissions = UserProfile.objects.get(user=request.user).permissions
        if permissions.list_management:
            print("here")
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_has_marketing_plan_Permission(function):
    def wrap(request, *args, **kwargs):
        permissions = UserProfile.objects.get(user=request.user).permissions
        if permissions.marketing_plan:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_has_skip_trace_Permission(function):
    def wrap(request, *args, **kwargs):
        permissions = UserProfile.objects.get(user=request.user).permissions
        if permissions.skip_trace:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_has_single_skip_trace_Balance(function):
    def wrap(request, *args, **kwargs):
        permissions = PrepaidBalance.objects.filter(user=request.user)
        price_data = UserProfile.objects.filter(user=request.user)
        if permissions:
            if permissions[0].amount >= price_data[0].skiptrace_price:
                return function(request, *args, **kwargs)
            else:
                return redirect('/skiptrace/skip_trace/single/')
        else:
            return redirect('/skiptrace/skip_trace/single/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_has_skip_history_Permission(function):
    def wrap(request, *args, **kwargs):
        permissions = UserProfile.objects.get(user=request.user).permissions
        if permissions.access_import_log:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_has_report_history_Permission(function):
    def wrap(request, *args, **kwargs):
        permissions = UserProfile.objects.get(user=request.user).permissions
        if permissions.access_export_log or permissions.access_import_log:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def is_admin_user(function):
    def wrap(request, *args, **kwargs):
        user = UserProfile.objects.get(user=request.user).role.role_name
        if user == 'Admin User':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
# def user_has_access_tag_log_Permission(function):
#     def wrap(request, *args, **kwargs):
#         permissions = UserProfile.objects.get(user=request.user).permissions
#         if permissions.access_tag_log:
#             return function(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap
