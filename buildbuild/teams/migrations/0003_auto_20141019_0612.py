# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20141017_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name=b'belonged_team', through='teams.Membership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='wait_members',
            field=models.ManyToManyField(related_name=b'requested_team', through='teams.WaitList', to=settings.AUTH_USER_MODEL),
        ),
    ]
