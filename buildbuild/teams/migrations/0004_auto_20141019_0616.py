# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20141019_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name=b'member', through='teams.Membership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='wait_members',
            field=models.ManyToManyField(related_name=b'wait_member', through='teams.WaitList', to=settings.AUTH_USER_MODEL),
        ),
    ]
