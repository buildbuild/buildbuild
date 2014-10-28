# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import __builtin__
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_auto_20141028_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomDockerText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('custom_docker_text', models.TextField(help_text=b'This field have docker text for each languages', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='availablelanguageversions',
            name='available_pyver',
        ),
        migrations.AddField(
            model_name='availablelanguageversions',
            name='available_lang_ver',
            field=jsonfield.fields.JSONField(default=__builtin__.dict, help_text=b'This field informs available language versions', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availablelanguages',
            name='available_lang',
            field=models.CharField(help_text=b'This field informs available languages', unique=True, max_length=30),
        ),
    ]
