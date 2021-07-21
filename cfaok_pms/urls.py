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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="main_home"),

    path('cfao_agri/', include('cfao_agri.urls'), name='cfao_agri'),
    path('cfao_kenya/', include('cfao_kenya.urls'), name='cfao_kenya'),
    path('tamk/', include('tamk.urls'), name='tamk'),
    path('tydia/', include('tydia.urls'), name='tydia'),
    path('toyota_kenya/', include('toyota_kenya.urls'), name='toyota_kenya'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/self_password_change/', views.self_change_password, name='change_user_password'),
    path('accounts/self_password_change/done/', views.self_password_change_done, name='self_change_user_password_done'),
]
