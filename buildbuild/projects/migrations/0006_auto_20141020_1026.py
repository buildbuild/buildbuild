# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_auto_20141020_1026'),
        ('projects', '0005_auto_20141017_0701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='team_list',
        ),
        migrations.RemoveField(
            model_name='project',
            name='team_wait_list',
        ),
        migrations.RemoveField(
            model_name='projectmembership',
            name='team',
        ),
        migrations.RemoveField(
            model_name='projectwaitlist',
            name='wait_team',
        ),
        migrations.AddField(
            model_name='project',
            name='project_teams',
            field=models.ManyToManyField(related_name=b'project_teams', through='projects.ProjectMembership', to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='project_wait_teams',
            field=models.ManyToManyField(related_name=b'project_wait_teams', through='projects.ProjectWaitList', to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectmembership',
            name='project_team',
            field=models.ForeignKey(related_name=b'membership_project_team', default=b'', to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectwaitlist',
            name='project_wait_team',
            field=models.ForeignKey(related_name=b'wait_list_project_team', default=b'', to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectmembership',
            name='project',
            field=models.ForeignKey(related_name=b'membership_project', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='projectwaitlist',
            name='project',
            field=models.ForeignKey(related_name=b'wait_list_project', to='projects.Project'),
        ),
    ]
