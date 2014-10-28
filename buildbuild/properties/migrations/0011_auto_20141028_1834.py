# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0010_auto_20141028_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dockertext',
            old_name='lang_docker_text',
            new_name='docker_text',
        ),
    ]
