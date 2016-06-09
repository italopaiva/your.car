from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
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
        else:
            context = {'form': form}
            response = TemplateResponse(request, "signup.html", context)
        return response

class NewCarView(View):
    
    form = CreateCarForm

    def post(self, request):
        form = self.form(data=request.POST)
        if form.is_valid():
            form.save()
            response = HttpResponseRedirect(reverse('cars'))
        else:
            context = {'form': form}
            response = TemplateResponse(request, "car/new_car_get_started.html", context)
        return response

def cars(request):
    cars = Car.objects.all()
    context = {'cars': cars}
    return TemplateResponse(request, "car/car_list.html", context)
