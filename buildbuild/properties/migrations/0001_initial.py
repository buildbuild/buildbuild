# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableLanguages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('available_lang', models.TextField(default=b'ruby python', help_text=b'This text informs available languages')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
