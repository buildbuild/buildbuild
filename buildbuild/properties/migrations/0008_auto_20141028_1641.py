# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0007_auto_20141028_1356'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AvailableLanguageAndVersion',
        ),
        migrations.DeleteModel(
            name='DockerTextForEachLanguage',
        ),
    ]
