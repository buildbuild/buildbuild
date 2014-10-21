# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20141020_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmembership',
            name='project_team',
            field=models.ForeignKey(related_name=b'membership_project_team', default=None, to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='projectwaitlist',
            name='project_wait_team',
            field=models.ForeignKey(related_name=b'wait_list_project_team', default=None, to='teams.Team'),
        ),
    ]
