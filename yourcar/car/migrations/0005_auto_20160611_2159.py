# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-11 21:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car', '0004_car_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='user',
        ),
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
            preserve_default=False,
        ),
    ]
