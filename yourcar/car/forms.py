from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from car.models import Car

class CreateCarForm(forms.ModelForm):
    
    class Meta:
        model = Car
        fields = '__all__'



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