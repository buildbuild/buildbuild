# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import __builtin__
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20141023_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='docker_text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='properties',
            field=jsonfield.fields.JSONField(default=__builtin__.dict),
        ),
    ]
