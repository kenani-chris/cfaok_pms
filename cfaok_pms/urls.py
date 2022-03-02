from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name="main_home"),

    path('Site/', include('Site.urls'), name='Site'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/self_password_change/', views.self_change_password, name='change_user_password'),
    path('accounts/self_password_change/done/', views.self_password_change_done, name='self_change_user_password_done'),
]
