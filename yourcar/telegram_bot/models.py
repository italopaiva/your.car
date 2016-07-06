from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class UserBotConversation(models.Model):
    user = models.ForeignKey(User)
    chat = models.BigIntegerField(unique=True)