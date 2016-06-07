from django.contrib import admin
from . import models

admin.site.register(models.Car)
admin.site.register(models.OilChange)
admin.site.register(models.Refuel)