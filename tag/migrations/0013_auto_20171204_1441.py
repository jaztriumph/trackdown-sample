# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0012_auto_20171204_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientinfo',
            name='client_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_time',
            field=models.DateTimeField(blank=True),
        ),
    ]
