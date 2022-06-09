from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import Home, password_expire, PasswordResetConfirmViewExtend, self_change_password, \
    self_password_change_done

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name="main_home"),

    path('Site/', include('Site.urls'), name='Site'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/password_expire/', password_expire, name='password_expire'),
    path('accounts/self_password_change/', self_change_password, name='self_change_user_password'),
    path('accounts/self_password_change/done/', self_password_change_done, name='self_change_user_password_done'),
    path('accounts/password_reset/<uidb64>/<token>/', PasswordResetConfirmViewExtend.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/password_reset/complete', TemplateView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),)
]
