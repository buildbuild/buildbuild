from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect,request

from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic import DetailView

from django.contrib.auth import authenticate

from django.contrib import messages

from django.core.urlresolvers import reverse

from django.db import IntegrityError
from django.db import OperationalError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from projects.forms import MakeProjectForm
from projects.models import Project, ProjectMembership
from teams.models import Team
from properties.models import AvailableLanguage, VersionList, DockerText
from buildbuild import custom_msg
from django.core.validators import URLValidator

from influxdb import client as influxdb

import json
import pprint
from elasticsearch import Elasticsearch
from copy import deepcopy

import re


# when User click a project in team page,
# team_page.html links to project_page url denoted in projects' urlconf
# and project_page method in view render project_page.html
# with the fields of project
def project_page(request, team_id, project_id):
    project_name = Project.objects.get_project(id=project_id).name
    team_name = Team.objects.get_team(id=team_id).name

    container_name = "'/docker/"+team_name + "_" + project_name + "'"

    # Get Client IP
    client_ip = request.META["REMOTE_ADDR"]

    # Access influxdb
    # internal ( 172.xxx.xxx.xxx ) to 172.16.100.169
    # external                     to  61.43.139.143

    is_internal = re.match( "172.*", client_ip, re.I,)

    if is_internal:
        influxdb_host = "soma.buildbuild.io"
    else:
        influxdb_host = "buildbuild.io"

    db = influxdb.InfluxDBClient(
        host=influxdb_host,
        database='cadvisor',
        timeout=2,
    )

    cpu_index = 0
    memory_index = 0
    rx_index = 0
    tx_index = 0
    try:
        query = db.query("select * from /.*/ where container_name =  '" + "/docker/registry" + "'limit 2")
        for index, item in enumerate(query[0]['columns']):
            if item == 'cpu_cumulative_usage':
                cpu_index = index
            elif item == 'memory_usage':
                memory_index = index
            elif item == 'tx_bytes':
                tx_index = index
            elif item == 'rx_bytes':
                rx_index = index
        memory_usage = query[0]['points'][0][memory_index]
        rx_used = query[0]['points'][0][rx_index]
        tx_used = (query[0]['points'][0][tx_index])
        cpu_usage = (query[0]['points'][0][cpu_index] - query[0]['points'][1][cpu_index])
    except:
        memory_usage = 0
        rx_used = 0
        tx_used = 0
        cpu_usage = 0

    # Calculate Values
    cpu_usage_in_Ghz = cpu_usage * 1.0 / (10**6)
    cpu_usage_percent = cpu_usage_in_Ghz / 2.8 * 100

    memory_usage_in_GB = memory_usage * 1.0 / (10**9)
    memory_usage_percent = memory_usage_in_GB / 1.0 * 100

    rx_used_in_GB = rx_used * 1.0 / (10**9)
    rx_used_percent = rx_used_in_GB / 1.0 * 100

    tx_used_in_GB = tx_used * 1.0 / (10**9)
    tx_used_percent = tx_used_in_GB / 1.0 * 100

    project = Project.objects.get_project(project_id)
    team = Team.objects.get_team(team_id)

    return render(
               request,
               "projects/project_page.html",
               {
                   "team" : team,
                   "project" : project,
                   "language" : project.properties['language'],
                   "version" : project.properties['version'],
                   "git_url" : project.properties['git_url'],
                   "branch_name" : project.properties['branch_name'],
                   "memory_usage" : memory_usage,
                   "memory_usage_percent" : memory_usage_percent,
                   "memory_usage_in_GB" : memory_usage_in_GB,
                   "requested_bytes" : rx_used,
                   "requested_bytes_percent" : rx_used_percent,
                   "requested_bytes_in_GB" : rx_used_in_GB,
                   "transferred_bytes" : tx_used,
                   "transferred_bytes_percent" : tx_used_percent,
                   "transferred_bytes_in_GB" : tx_used_in_GB,
                   "cpu_usage" : cpu_usage,
                   "cpu_usage_percent" : cpu_usage_percent,
                   "cpu_usage_in_Ghz" : cpu_usage_in_Ghz,
               },
           )


class MakeProjectView(FormView):
    template_name = "projects/makeproject.html"
    form_class = MakeProjectForm

    def get_queryset(self):
        return self.kwargs['team_id']

    # context['var'] in views -> {{var}} in html
    def get_context_data(self, **kwargs):
        context = super(MakeProjectView, self).get_context_data(**kwargs)
        user = self.request.user
        team_id = self.get_queryset()
        team = Team.objects.get_team(team_id)

        # user who doesn't belong the team cannot access makeproject page
        try:
            team.members.get_member(user.id)
        except ObjectDoesNotExist:
            context['is_team_member'] = False
        else:
            context['is_team_member'] = True

        return context

    def form_valid(self, form):
        project = Project()
        project_name = self.request.POST["projects_project_name"]
        team_id = self.get_queryset()

        team = Team.objects.get_team(team_id)

        # empty space value, for simple short name
        language = ""
        version = ""
        git_url = ""
        branch_name = ""
        properties = dict()

        # Check the team is in <teams DB>
        try:
            team = Team.objects.get_team(team_id)
        except ObjectDoesNotExist:
            messages.error(self.request, custom_msg.project_make_project_error)
            messages.info(self.request, custom_msg.project_non_exist_team)
            return HttpResponseRedirect(reverse("home"))

        # Check valid project name
        try:
            Project.objects.validate_name(project_name)
        except ValidationError:
            messages.error(self.request, custom_msg.project_make_project_error)
            messages.info(self.request, custom_msg.project_invalid)
            return HttpResponseRedirect(reverse("home"))

        # Check unique project name
        # Notice : project name must be unique in one team, not all teams
        try:
            Project.objects.check_uniqueness_project_name(
                project_name = project_name,
                team_name = team.name,
            )
        except IntegrityError:
            messages.error(self.request, custom_msg.project_make_project_error)
            messages.info(self.request, custom_msg.project_already_exist)
            return HttpResponseRedirect(reverse("home"))

        # Check valid team name
        try:
            Team.objects.validate_name(team.name)
        except ValidationError:
            messages.error(self.request, custom_msg.project_make_project_error)
            messages.info(self.request, custom_msg.project_invalid_team_name)
            return HttpResponseRedirect(reverse("home"))

        # Login check is programmed in buildbuild/urls.py
        # Check login user belong to the team
        user = self.request.user
        try:
            team.members.get_member(id = user.id)
        except ObjectDoesNotExist:
            messages.error(self.request, custom_msg.project_make_project_error)
            messages.info(self.request, custom_msg.project_user_does_not_belong_team)
            return HttpResponseRedirect(reverse("home"))

        # Both Language & Version form is needed
        if ("language" in self.request.POST) and ("version" in self.request.POST):
            language = self.request.POST["language"]
            version = self.request.POST["version"]

            try:
                VersionList.objects.validate_lang(language)
            except ObjectDoesNotExist:
                messages.error(self.request, custom_msg.project_make_project_error)
                messages.info(self.request, custom_msg.project_lang_invalid)
                return HttpResponseRedirect(reverse("home"))

            try:
                Project.objects.validate_version_of_language(language, version)
            except ObjectDoesNotExist:
                messages.error(self.request, custom_msg.project_make_project_error)
                messages.info(self.request, custom_msg.project_ver_invalid)
                return HttpResponseRedirect(reverse("home"))

        elif ("language" in self.request.POST) or ("version" in self.request.POST):
            messages.error(self.request, custom_msg.project_make_project_error)
            messages.info(self.request, custom_msg.project_both_lang_and_ver_is_needed)
            return HttpResponseRedirect(reverse("home"))

        # Both Git & Branch name form is needed
        if ("git_url" in self.request.POST) and ("branch_name" in self.request.POST):
            git_url = self.request.POST["git_url"]
            branch_name = self.request.POST["branch_name"]

            try:
                validate_git_url = URLValidator()
                validate_git_url(git_url)
            except ValidationError:
                messages.error(self.request, custom_msg.project_make_project_error)
                messages.info(self.request, custom_msg.url_invalid)
                return HttpResponseRedirect(reverse("home"))
            except UnicodeError:
                messages.error(self.request, custom_msg.project_make_project_error)
                messages.info(self.request, custom_msg.url_unicode_invalid)
                return HttpResponseRedirect(reverse("home"))

            # it's empty validator for branch name, needed to more test for this.
            try:
                Project.objects.validate_git_url(branch_name)
            except:
                pass

        elif ("git_url" in self.request.POST) or ("branch_name" in self.request.POST):
            messages.error(self.request, custom_msg.project_both_git_url_and_branch_name_is_needed)
            return HttpResponseRedirect(reverse("home"))

        properties = {
                         'language' : language,
                         'version' : version,
                         'git_url' : git_url,
                         'branch_name' : branch_name,
                     }

        project = Project.objects.create_project(
                      name = project_name,
                      team_name = team.name,
                      properties = properties,
                  )

        # Create Elastic Search for grafana
        es = Elasticsearch([{'host' : 'soma.buildbuild.io'}])

        # Get templates as a docker - project
        doc = es.get(index='docker-grafana-dash', doc_type='dashboard', id = 'dockerproject')

        pr = team.name + "_" + project_name
        name = '/docker/' + pr # As a query language
        project_name = "container_name = '" + name + "'"
        uni_name = unicode(project_name, 'unicode-escape')
        _doc = deepcopy(doc)

        _doc['_id'] = pr
        loads = json.loads(_doc['_source']['dashboard'])

        loads['title'] = pr
        loads['originalTitle'] = pr
        loads['rows'][0]['panels'][0]['targets'][0]['condition'] = uni_name
        loads['rows'][0]['panels'][0]['targets'][0]['query'] = loads['rows'][0]['panels'][0]['targets'][0]['query'].replace('/docker/registry',name)

        loads['rows'][1]['panels'][0]['targets'][0]['condition'] = uni_name
        loads['rows'][1]['panels'][0]['targets'][0]['query'] = loads['rows'][0]['panels'][0]['targets'][0]['query'].replace('/docker/registry',name)

        loads['rows'][2]['panels'][0]['targets'][0]['condition'] = uni_name
        loads['rows'][2]['panels'][0]['targets'][0]['query'] = loads['rows'][0]['panels'][0]['targets'][0]['query'].replace('/docker/registry',name)

        loads['rows'][2]['panels'][0]['targets'][1]['condition'] = uni_name
        loads['rows'][2]['panels'][0]['targets'][1]['query'] = loads['rows'][0]['panels'][0]['targets'][1]['query'].replace('/docker/registry',name)

        dumps = json.dumps(loads)

        _doc['_source']['dashboard'] = dumps
        _doc['_source']['title'] = pr
        _doc['_version'] = 0

        es.index(index = 'docker-grafana-dash', doc_type='dashboard', id=pr, body = _doc['_source'])

        messages.success(self.request, custom_msg.project_make_project_success)
        messages.info(self.request, custom_msg.project_make_success)

        # redirect url should be changed later
        return HttpResponseRedirect(reverse("home"))

