from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from car.models import Car, Refuel

class CreateCarForm(forms.ModelForm):
    
    class Meta:
        model = Car
        fields = '__all__'
        exclude = ['owner']


class NewUserForm(forms.ModelForm):

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        help_text=_('For your safety, use a minimum of 6 and maximum of 10 digits password.'),
        validators=[validators.MinLengthValidator(6), validators.MaxLengthValidator(10)],

    )

    class Meta:
        model = User
        fields = ['username']


class NewRefuelForm(forms.ModelForm):
    
    from functools import partial
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})

    date = forms.DateField(widget=DateInput())

    class Meta:
        model = Refuel
        fields = '__all__'
        exclude = ['car']