from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core import validators
from django.contrib.auth.models import User

class Car(models.Model):
    owner = models.ForeignKey(User, verbose_name=_('Owner'))
    car_model = models.CharField(
        _("Car model"),
        max_length=20,
        validators=[
            validators.RegexValidator(
                r'^[a-zA-Z0-9\s+]+$',
                _('Car model must have only alphanumeric characters')
            )
        ]
    )
    color = models.CharField(
        _("Car color"),
        max_length=20,
        validators=[
            validators.RegexValidator(
                r'^[a-zA-Z\s+]+$',
                _('Car color must have only alphabetical characters')
            )
        ]
    )
    year = models.SmallIntegerField(
        _("Car year"),
        help_text=_('Use year as YYYY.'),
        validators=[validators.RegexValidator(
            r'^[0-9]{4}$',
            _('Year in invalid format!')
        )]
    )
    mileage = models.IntegerField(
        _("Car mileage"),
        default=0,
        validators=[validators.MinValueValidator(0)],
        help_text=_("Set here your car mileage at the moment.")
    )
    name = models.CharField(
        _("Car name"),
        max_length=20,
        validators=[
            validators.RegexValidator(
                r'^[a-zA-Z0-9\s+]+$',
                _('Car name must have only alphanumeric characters')
            )
        ],
        help_text=_("Do you name your car? We like it! Tell us the name of your.car."),
        blank=True
    )

    def __str__(self):
        if not self.name:
            car_name = self.car_model + "/" + str(self.year)
        else:
            car_name = self.name
        return car_name

class OilChange(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField('date changed')
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
    date = models.DateField('date refueled')
    liters = models.DecimalField(max_digits=7, decimal_places=3, validators=[validators.MinValueValidator(0)])
    fuel_price = models.DecimalField(max_digits=4, decimal_places=2, validators=[validators.MinValueValidator(0)])
    mileage = models.IntegerField(
        default=0,
        validators=[validators.MinValueValidator(0)]
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPES,
        default=REGULAR_GAS
    )

    def __str__(self):
        return _("Refuel") + " " + str(self.date) + " - " + str(self.mileage) + " Km"