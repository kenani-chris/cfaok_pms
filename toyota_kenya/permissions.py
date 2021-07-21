from .apps import ToyotaKenyaConfig
from django.http import HttpResponseRedirect
from django.urls import reverse


def is_member_company(user):
    return user.groups.filter(name=ToyotaKenyaConfig.name).exists()


def is_admin(user):
    return user.is_superuser
