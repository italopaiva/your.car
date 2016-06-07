from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.template.response import TemplateResponse
from car.forms import CreateCarForm
from car.models import Car

def home(request):
    context = {
        'form': CreateCarForm()
    }
    return TemplateResponse(request, "home.html", context)

class NewCarView(View):
    
    form = CreateCarForm

    def post(self, request):
        form = self.form(data=request.POST)
        if form.is_valid():
            form.save()
            response = HttpResponse('Salvou o carro')
        else:
            context = {'form': form}
            response = TemplateResponse(request, "car/new_car_get_started.html", context)
        return response
