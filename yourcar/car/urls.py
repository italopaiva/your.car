from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^new$', views.NewCarView.as_view(), name='new_car'),
    url(r'^cars$', views.cars, name='cars'),
]