# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0009_availablelanguageandversion_dockertextforeachlanguage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(help_text=b'This field informs available languages', unique=True, max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='DockerTextForEachLanguage',
            new_name='DockerText',
        ),
        migrations.RenameModel(
            old_name='AvailableLanguageAndVersion',
            new_name='Version',
        ),
        migrations.RenameField(
            model_name='version',
            old_name='available_lang_ver',
            new_name='lang_ver',
        ),
    ]
