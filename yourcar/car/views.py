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
from car.models import Car, Refuel, OilChange, UserBotConversation
from django.core.exceptions import ObjectDoesNotExist
import requests
import json


class BotView(View):

    bot_token = '257906616:AAF5IAAm65BtHGK8RHYXw0qSXNnKartFFeQ'

    def handle(self, cmd, chat_id):
        cmd_and_args = cmd.split(' ')
        command = cmd_and_args[0]
        post_data = {}
        post_data['chat_id'] = chat_id
        if command == '/start':
            try:
                username = cmd_and_args[1]
                try:
                    user = User.objects.get(username=username)
                    UserBotConversation.objects.update_or_create(user=user, chat=chat_id) # Save the user chat_id
                    text = 'Hello %s, welcome to your.car Bot!' % username
                except ObjectDoesNotExist:
                    text = 'This user is not registered in Your.car'
            except IndexError:
                text = 'It seems that you forgot to tell us your username...'

            post_data['text'] = text
            self.__send_message(post_data)
        elif command == '/newrefuel':
            NUM_OF_ARGS = 7 # This command needs 7 arguments
            if len(cmd_and_args) is NUM_OF_ARGS:
                try:

                    user_conversation = UserBotConversation.objects.get(chat=chat_id)
                    user_cars = Car.objects.filter(owner=user_conversation.user)
                    car_to_refuel = cmd_and_args[1]

                    if(self.car_exists(user_cars, car_to_refuel)):
                        post_data['text'] = 'Car refueled!'
                    else:
                        msg = 'This car does not exists on your account. Check your.cars: \n'
                        for car in user_cars:
                            msg = msg + ' - ' + str(car) + '\n'
                        post_data['text'] = msg
                except ObjectDoesNotExist:
                    post_data['text'] = 'User not found. Tell us your your.car login on /start command first. Like: /start username .'
            else:
                post_data['text'] = 'Use newrefuel command like this: /newrefuel car date liters price mileage fuel_type'
            self.__send_message(post_data)

    def car_exists(self, user_cars, car_to_check):
        there_is_car = False
        for car in user_cars:
            if str(car) == car_to_check:
                there_is_car = True
                break
        return there_is_car

    def __send_message(self, message):
      requests.post('https://api.telegram.org/bot%s/sendMessage' % self.bot_token, data=message)

    def post(self, request):
       msg = json.loads((request.body).decode('UTF-8'))
       print(msg)
       msg = msg['message']
       chat_id = msg['chat']['id']
       command = msg['text']
       self.handle(command, chat_id)
       return HttpResponse('OK')

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

            first_contact = request.POST.get('first_contact')
            if not first_contact:
                template = "car/car_list.html"
            else:
                template = "car/new_car_get_started.html"

            msg_level = messages.ERROR
            msg = _('You have some problems on your car info. Please, correct these trying to create it again.')
            messages.add_message(request, msg_level, msg)
            response = TemplateResponse(request, template, context)

        return response

class NewRefuelView(View):

    form = NewRefuelForm

    @method_decorator(login_required)
    def get(self, request, car_id):
        car = Car.objects.get(pk=car_id)
        context = {'form': self.form(), 'car': car}
        return TemplateResponse(request, "refuel/new_refuel.html", context)

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
            response = TemplateResponse(request, "refuel/new_refuel.html", context)
            msg_level = messages.ERROR
            msg = _('Something is wrong. Please, check the data you\'ve informed.')

        messages.add_message(request, msg_level, msg)
        return response


class DeleteRefuelView(View):
    http_method_names = [u'post']

    @method_decorator(login_required)
    def post(self, request, refuel_id):
        refuel = Refuel.objects.get(pk=refuel_id)
        if refuel.car.owner == request.user:
            refuel_car = refuel.car
            refuel.delete()
            messages.add_message(request, messages.SUCCESS, _("Refuel deleted successfuly!"))
            response = HttpResponseRedirect(reverse('car_refuels',
                                            kwargs={'car_id': refuel_car.pk}))
            return response
        else:
            raise Http404

class UpdateRefuelView(View):

    form = NewRefuelForm

    @method_decorator(login_required)
    def get(self, request, refuel_id):
        refuel = Refuel.objects.get(pk=refuel_id)
        if refuel.car.owner == request.user:
            form = self.form(instance=refuel)
            context = {'form': form, 'refuel': refuel, 'car': refuel.car}
            return TemplateResponse(request, "refuel/edit_refuel.html", context)
        else:
            raise Http404

    @method_decorator(login_required)
    def post(self, request, refuel_id):
        refuel = Refuel.objects.get(pk=refuel_id)
        if refuel.car.owner == request.user:
            form = self.form(data=request.POST, instance=refuel)
            if form.is_valid():
                form.save()
                response = HttpResponseRedirect(reverse('car_refuels', kwargs={'car_id': refuel.car.pk}))
                msg_level = messages.SUCCESS
                msg = _('Refuel updated with success!')
            else:
                msg_level = messages.ERROR
                msg = _('Something is wrong. Please, check the data you\'ve informed.')
                context = {'form': form, 'refuel': refuel, 'car': refuel.car}
                response = TemplateResponse(request, "refuel/edit_refuel.html", context)
            messages.add_message(request, msg_level, msg)
            return response
        else:
            raise Http404

@login_required
def cars(request):
    cars = Car.objects.filter(owner=request.user)
    context = {'cars': cars, 'form': CreateCarForm()}
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
