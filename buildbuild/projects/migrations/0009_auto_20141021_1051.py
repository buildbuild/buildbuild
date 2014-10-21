# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20141021_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_teams',
            field=models.ManyToManyField(related_name=b'project_teams', through='projects.ProjectMembership', to=b'teams.Team'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_wait_teams',
            field=models.ManyToManyField(related_name=b'project_wait_teams', through='projects.ProjectWaitList', to=b'teams.Team'),
        ),
        migrations.AlterField(
            model_name='projectwaitlist',
            name='project',
            field=models.ForeignKey(related_name=b'wait_list_project', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='projectwaitlist',
            name='project_wait_team',
            field=models.ForeignKey(related_name=b'wait_list_project_team', default=None, to='teams.Team'),
        ),
    ]
