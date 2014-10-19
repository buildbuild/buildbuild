# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20141019_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name=b'belonged_team', through='teams.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
