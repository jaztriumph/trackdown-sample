# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-03 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0005_auto_20171203_0534'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='time',
            field=models.DateTimeField(default=b'2006-10-25 14:30:59', max_length=100),
        ),
    ]
