# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-10 18:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0016_remove_clientinfo_client_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientinfo',
            name='user_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_info', to='tag.UserInfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_info', to=settings.AUTH_USER_MODEL),
        ),
    ]
