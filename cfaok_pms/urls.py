"""cfaok_pms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include
from . import views
from .views import PasswordChangeDone

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="main_home"),
    path('cfao_kenya/', include('cfao_kenya.urls'), name='cfao_kenya'),
    path('cfao_agri/', include('cfao_agri.urls'), name='cfao_agri'),
    path('tamk/', include('tamk.urls'), name='tamk'),
    path('tydia/', include('tydia.urls'), name='tydia'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name="registration/change-password.html"), name='change_user_password'),
    path('accounts/password_change/done/', PasswordChangeDone.as_view(), name='change_user_password_done'),
]
