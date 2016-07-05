"""yourcar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from car import views as car_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=settings.YOUR_CAR_HOME), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login', auth_views.login, {'template_name': 'login.html'}, "login"),
    url(r'^logout', auth_views.logout, {'next_page': 'home'}, "logout"),
    url(r'^signup', car_views.SignUpView.as_view(), name="signup"),
    url(r'^car/', include('car.urls')),
    url(r'^bot$', car_views.BotView.as_view()),
]
