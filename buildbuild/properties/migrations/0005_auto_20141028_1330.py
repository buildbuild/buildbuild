# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_auto_20141028_1322'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AvailableLanguages',
        ),
        migrations.AlterField(
            model_name='availablelanguageversions',
            name='available_lang_ver',
            field=jsonfield.fields.JSONField(default={b'': b''}, help_text=b'This field informs available language versions', unique=True),
        ),
    ]
