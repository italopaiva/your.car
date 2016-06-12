from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View
from django.template.response import TemplateResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from car.forms import CreateCarForm, NewUserForm, NewRefuelForm
from car.models import Car, Refuel, OilChange

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

class NewRefuelView(View):
    
    form = NewRefuelForm

    @method_decorator(login_required)
    def get(self, request, car_id):
        car = Car.objects.get(pk=car_id)
        context = {'form': self.form(), 'car': car}
        return TemplateResponse(request, "car/new_refuel.html", context)

    @method_decorator(login_required)
    def post(self, request, car_id):
        car = Car.objects.get(pk=car_id)
        refuel = Refuel(car=car)
        form = self.form(data=request.POST, instance=refuel)
        if form.is_valid():
            form.save()
            response = HttpResponseRedirect(reverse('car_refuels', kwargs={'car_id': car_id}))
            msg_level = messages.SUCCESS
            msg = _('Your refuel was successfuly saved!')
        else:
            context = {'form': form, 'car': car}
            response = TemplateResponse(request, "car/new_refuel.html", context)
            msg_level = messages.ERROR
            msg = _('Something is wrong. Please, check the data you\'ve informed.')

        messages.add_message(request, msg_level, msg)
        return response


class DeleteRefuelView(View):
    http_method_names = [u'post']

    def post(self, request, refuel_id):
        refuel = Refuel.objects.get(pk=refuel_id)
        refuel_car = refuel.car
        if refuel.car.owner == request.user:
            refuel.delete()
            messages.add_message(request, messages.SUCCESS, _("Refuel delete successfuly!"))
            response = HttpResponseRedirect(reverse('car_refuels', 
                                            kwargs={'car_id': refuel_car.pk}))
            return response
        else:
            raise Http404


@login_required
def cars(request):
    cars = Car.objects.all()
    context = {'cars': cars}
    return TemplateResponse(request, "car/car_list.html", context)

@login_required
def refuels(request, car_id):
    car = Car.objects.get(pk=car_id)
    refuels = Refuel.objects.filter(car=car_id)
    context = {'refuels': refuels, 'car': car}
    return TemplateResponse(request, "car/car_refuels.html", context)

@login_required
def oil_changes(request, car_id):
    pass