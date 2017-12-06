# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0014_clientinfo_client_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientinfo',
            name='client_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
