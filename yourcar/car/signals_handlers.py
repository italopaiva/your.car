from django.db.models.signals import post_save
from telegram_bot.models import UserBotConversation
from django.core.exceptions import ObjectDoesNotExist
from telegram_bot.views import send_message

def notify_in_telegram(sender, instance, created, **kwargs):
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

