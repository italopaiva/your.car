from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from telegram_bot.models import UserBotConversation
from telegram_bot.views import send_message
from car.models import Refuel
from car.signals import car_refuel_expense

@receiver(post_save, sender=Refuel)
def notify_new_refuel_in_telegram(sender, instance, created, **kwargs):
    if created:
        # Getting user from refuel
        user = instance.car.owner
        try:
            conversation = UserBotConversation.objects.get(user=user)
        except ObjectDoesNotExist:
            # If the refuel car owner was not found, it is not in touch with the Bot
            # So, no need to notify
            pass
        else:
            car = instance.car
            msg = 'New refuel (%s) for %s registered!' % (str(instance), str(car))
            chat_id = conversation.chat
            message = {'chat_id': chat_id, 'text': msg}
            send_message(message)

@receiver(car_refuel_expense)
def notify_expense_in_telegram(sender, car, **kwargs):
    expense = car.refuel_expense

    user = car.owner
    try:
        conversation = UserBotConversation.objects.get(user=user)
    except ObjectDoesNotExist:
        # If the refuel car owner was not found, it is not in touch with the Bot
        # So, no need to notify
        pass
    else:
        msg = 'You already spent $%s with refuels in %s, keep your eyes open and your wallet closed!' % (str(expense), str(car))
        chat_id = conversation.chat
        message = {'chat_id': chat_id, 'text': msg}
        send_message(message)
