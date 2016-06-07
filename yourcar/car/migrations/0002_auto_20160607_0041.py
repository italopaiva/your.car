# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 00:41
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_model',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9\\s+]+$', 'Car model must have only alphanumeric characters')], verbose_name='Car model'),
        ),
        migrations.AlterField(
            model_name='car',
            name='color',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^[a-zA-Z\\s+]+$', 'Car color must have only alphabetical characters')], verbose_name='Car color'),
        ),
        migrations.AlterField(
            model_name='car',
            name='mileage',
            field=models.IntegerField(default=0, help_text='Set here your car mileage at the moment.', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Car mileage'),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.SmallIntegerField(help_text='Use year as YYYY.', validators=[django.core.validators.RegexValidator('^[0-9]{4}$', 'Year in invalid format!')], verbose_name='Car year'),
        ),
    ]
