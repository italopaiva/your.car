from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.template.response import TemplateResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from car.forms import CreateCarForm, NewUserForm
from car.models import Car

def home(request):
    context = {
        'form': CreateCarForm()
    }
    return TemplateResponse(request, "home.html", context)

class SignUpView(View):

    form = NewUserForm

    def get(self, request):
        context = {'form': self.form()}
        return TemplateResponse(request, "signup.html", context)

    def post(self, request):

        form = self.form(data=request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            response = HttpResponseRedirect(reverse('login'))
            msg_level = messages.SUCCESS
            msg = _('Registered with success!')
            messages.add_message(request, msg_level, msg)
        else:
            context = {'form': form}
            response = TemplateResponse(request, "signup.html", context)

        return response

class NewCarView(View):
    
    form = CreateCarForm

    @method_decorator(login_required)
    def post(self, request):
        car = Car(owner=request.user)
        form = self.form(data=request.POST, instance=car)
        if form.is_valid():
            form.save()
            response = HttpResponseRedirect(reverse('cars'))
            msg_level = messages.SUCCESS
            msg = _('Congrats! Now we are keeping your.car! Add some data about it.')
            messages.add_message(request, msg_level, msg)
        else:
            context = {'form': form}
            response = TemplateResponse(request, "car/new_car_get_started.html", context)

        return response

@login_required
def cars(request):
    cars = Car.objects.all()
    context = {'cars': cars}
    return TemplateResponse(request, "car/car_list.html", context)
