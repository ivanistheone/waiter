# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 23:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('runs', '0003_auto_20170612_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentchannel',
            name='followers',
            field=models.ManyToManyField(related_name='saved_channels', to=settings.AUTH_USER_MODEL),
        ),
    ]
