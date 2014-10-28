# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_auto_20141028_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableLanguageAndVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('available_lang_ver', jsonfield.fields.JSONField(default={b'': b''}, help_text=b'This field informs available languages and  versions', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DockerTextForEachLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang_docker_text', jsonfield.fields.JSONField(default={b'': b''}, help_text=b'This field have docker texts for each language', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='AvailableLanguageVersions',
        ),
        migrations.DeleteModel(
            name='LanguageDockerText',
        ),
    ]
