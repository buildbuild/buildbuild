# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availablelanguages',
            name='available_lang',
            field=models.TextField(help_text=b'This text informs available languages'),
        ),
    ]
