# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 22:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0009_auto_20160705_0500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbotconversation',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserBotConversation',
        ),
    ]