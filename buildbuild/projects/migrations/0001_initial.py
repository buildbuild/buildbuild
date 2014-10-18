# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('project', models.ForeignKey(related_name=b'project_membership_project', to='projects.Project')),
                ('team', models.ForeignKey(related_name=b'project_membership_team', to='teams.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectWaitList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(related_name=b'project_wait_list_project', to='projects.Project')),
                ('wait_team', models.ForeignKey(related_name=b'project_wait_list_team', to='teams.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='team_list',
            field=models.ManyToManyField(related_name=b'project_membership', through='projects.ProjectMembership', to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='team_wait_list',
            field=models.ManyToManyField(related_name=b'project_wait_list', through='projects.ProjectWaitList', to='teams.Team'),
            preserve_default=True,
        ),
    ]
