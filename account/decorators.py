from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect


def check_role_admin(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied