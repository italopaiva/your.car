from django.db.models.signals import post_save

def notify_in_telegram(sender, instance, created, **kwargs):
    if created:
        pass