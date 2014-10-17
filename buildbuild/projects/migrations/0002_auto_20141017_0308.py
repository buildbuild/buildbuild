# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import __builtin__
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='docker_text',
            field=models.TextField(default=b'none'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='properties',
            field=jsonfield.fields.JSONField(default=__builtin__.dict),
            preserve_default=True,
        ),
    ]
