# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_auto_20141028_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageDockerText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang_docker_text', jsonfield.fields.JSONField(default={b'': b''}, help_text=b'This field have a docker text for each languages', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='CustomDockerText',
        ),
    ]
