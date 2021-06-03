from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

def staff_path(url, view, login_url, name):
    return path(url, staff_member_required(view(), login_url=login_url), name=name)