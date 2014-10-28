# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import __builtin__
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_auto_20141028_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableLanguageVersions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('available_pyver', jsonfield.fields.JSONField(default=__builtin__.dict, help_text=b'This field informs available python versions')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='availablelanguages',
            name='available_lang',
            field=models.CharField(help_text=b'This field informs available languages', max_length=30),
        ),
    ]
