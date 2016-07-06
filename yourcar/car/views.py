from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import View
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from car.forms import CreateCarForm, NewUserForm, NewRefuelForm
from car.models import Car, Refuel, OilChange, UserBotConversation
import requests
import json

def send_message(message):
    requests.post('https://api.telegram.org/bot%s/sendMessage' % settings.BOT_TOKEN, data=message)

class StartCommand:
    NUM_OF_ARGS = 1

    def handle(self, cmd_and_args, chat_id):
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

        message = {'chat_id': chat_id, 'text':  text}
        send_message(message)

class NewRefuelCommand:
    NUM_OF_ARGS = 6 # This command needs this much arguments

    def handle(self, cmd_and_args, chat_id):
        print("Chegou na classe NewRefuelCommand")
        message = {'chat_id': chat_id}
        if len(cmd_and_args) is self.NUM_OF_ARGS:
            print("Quantity of args ok!")
            try:
                user_conversation = UserBotConversation.objects.get(chat=chat_id)
                user_cars = Car.objects.filter(owner=user_conversation.user)
                car_to_refuel = cmd_and_args[1]

                exists, car = self.car_exists(user_cars, car_to_refuel)
                if exists:
                    refuel = Refuel(car=car, fuel_type=Refuel.REGULAR_GAS)
                    new_refuel = {
                        'mileage': cmd_and_args[2],
                        'date': cmd_and_args[3],
                        'liters': cmd_and_args[4],
                        'fuel_price': cmd_and_args[5],
                        'fuel_type': Refuel.REGULAR_GAS
                    }
                    form = NewRefuelForm(data=new_refuel, instance=refuel)
                    if form.is_valid():
                        form.save()
                        message['text'] = '%s refuel noted!' % car_to_refuel
                    else:
                        msg = 'Something went wrong. Check our data about it: \n'
                        for field, error in form.errors.items():
                            msg = msg + field + " - " + repr(error) + "/n"
                        message['text'] = msg
                else:
                    if not user_cars:
                        msg = 'You have no cars on your.car account. Register one there, is easy!'
                    else:
                        msg = 'This car does not exists on your account. Check your.cars: \n'
                        for car in user_cars:
                            msg = msg + ' - ' + str(car) + '\n'
                    message['text'] = msg
            except ObjectDoesNotExist:
                message['text'] = 'User not found. Tell us your your.car login on /start command first. Like: /start username .'
        else:
            print("Quantity of args not ok!")
            message['text'] = 'Use newrefuel command like this: /newrefuel car mileage date liters price'
        send_message(message)

    def car_exists(self, user_cars, car_to_check):
        there_is_car = False
        found_car = None
        for car in user_cars:
            if str(car) == car_to_check:
                there_is_car = True
                found_car = car
                break
        return there_is_car, found_car

class BotView(View):

    def handle(self, cmd, chat_id):
        cmd_and_args = cmd.split(' ')
        command = cmd_and_args[0]
        if command == '/start':
            StartCommand().handle(cmd_and_args, chat_id)
        elif command == '/newrefuel':
            print("arrive in new refuel in bot view")
            NewRefuelCommand().handle(cmd_and_args, chat_id)

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
