from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^new$', views.NewCarView.as_view(), name='new_car'),
    url(r'^cars$', views.cars, name='cars'),
    url(r'^refuels/(?P<car_id>[0-9]+)$', views.refuels, name='car_refuels'),
    url(r'^refuels/new/(?P<car_id>[0-9]+)$', views.NewRefuelView.as_view(), name='new_refuel'),
    url(r'^oil_changes/(?P<car_id>[0-9]+)$', views.oil_changes, name='car_oil_changes'),
]