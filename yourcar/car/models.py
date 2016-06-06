from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core import validators

class Car(models.Model):
    car_model = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    year = models.SmallIntegerField(
        help_text=_('Use year as YYYY.'),
        validators=[validators.RegexValidator(
            r'^[0-9]{4}$',
            _('Year in invalid format!'),
            'invalid'
        )]
    )
    mileage = models.IntegerField(
        default=0,
        validators=[validators.MinValueValidator(0)],
        help_text=_("Or your car is brand new or it have some mileage traveled")
    )

    def __str__(self):
        return self.car_model + "/" + self.year

class OilChange(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateTimeField('date changed')
    mileage = models.IntegerField(
        default=0,
        validators=[validators.MinValueValidator(0)]
    )

class Refuel(models.Model):
    REGULAR_GAS = _("Regular gas")
    FUEL_TYPES = (
        (REGULAR_GAS, _("Regular gas")),
        (_("Premium gas"), _("Premium gas")),
        (_("Alcohol"), _("Alcohol")),
        (_("Diesel"), _("Diesel")),
    )

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateTimeField('date refueled')
    liters = models.DecimalField(max_digits=7, decimal_places=3)
    fuel_price = models.DecimalField(max_digits=4, decimal_places=2)
    mileage = models.IntegerField(
        default=0,
        validators=[validators.MinValueValidator(0)]
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPES,
        default=REGULAR_GAS
    )