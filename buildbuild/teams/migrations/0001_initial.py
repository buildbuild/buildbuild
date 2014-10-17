# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('member', models.ForeignKey(related_name=b'membership_member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('contact_number', models.CharField(max_length=20)),
                ('website_url', models.URLField(max_length=255)),
                ('members', models.ManyToManyField(related_name=b'membership', through='teams.Membership', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WaitList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(related_name=b'wait_list_team', to='teams.Team')),
                ('wait_member', models.ForeignKey(related_name=b'wait_list_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='team',
            name='wait_members',
            field=models.ManyToManyField(related_name=b'wait_list', through='teams.WaitList', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='team',
            field=models.ForeignKey(related_name=b'membership_team', to='teams.Team'),
            preserve_default=True,
        ),
    ]
