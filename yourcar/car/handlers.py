from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from telegram_bot.models import UserBotConversation
from telegram_bot.views import send_message
from car.models import Car, Refuel
from car.forms import NewRefuelForm

class StartCommand:

    NUM_OF_ARGS = 1

    def handle(self, cmd_and_args, chat_id):
        print(chat_id)
        print('Chegou no comando start')
        print(cmd_and_args)
        print(chat_id)
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

class HelpCommand:

    NUM_OF_ARGS = 0

    def handle(self, cmd_and_args, chat_id):
        help_text = 'Welcome to Your.Car Bot! This is what you can do by now with me: \n\n'
        help_text += '/newrefuel - Register a new refuel for one of your.cars. Use it like this:\n'
        help_text += '\t/newrefuel car mileage date liters price'
        message = {'chat_id': chat_id, 'text': help_text}
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
                            msg = msg + field + " - " + repr(error) + "\n"
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

# Beyond the commons /help and /start
SUPPORTED_COMMANDS = {
    '/newrefuel': NewRefuelCommand
}
