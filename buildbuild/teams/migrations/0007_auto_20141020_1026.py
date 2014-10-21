# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_auto_20141019_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitlist',
            name='wait_member',
            field=models.ForeignKey(related_name=b'wait_list_wait_member', to=settings.AUTH_USER_MODEL),
        ),
    ]
