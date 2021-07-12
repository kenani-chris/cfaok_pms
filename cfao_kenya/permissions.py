from .apps import CfaoKenyaConfig
from django.http import HttpResponseRedirect
from django.urls import reverse


def is_member_company(user):
    return user.groups.filter(name=CfaoKenyaConfig.name).exists()


def is_admin(user):
    return user.is_superuser
