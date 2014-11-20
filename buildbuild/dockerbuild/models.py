from django.db import models
from projects.models import Project, ProjectManager
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from properties.models import DockerText
import os
import platform

from docker import Client
from docker.tls import TLSConfig

from io import BytesIO
import json

class BuildManager(models.Manager):
    def build_project(self, project_id, tag, **kwargs):
#       Darwin is OS X
        if platform.system() == 'Darwin':
            DOCKER_HOST = os.environ['DOCKER_HOST']
            DOCKER_HOST = DOCKER_HOST.replace('tcp', 'https')
            DOCKER_CERT_PATH = os.environ['DOCKER_CERT_PATH']
            cert_dir = os.environ['DOCKER_CERT_PATH'] + '/'
            tls_config = TLSConfig(
                 client_cert=(cert_dir + 'cert.pem', cert_dir + 'key.pem'), verify=False
            )
            docker_client = Client(base_url=DOCKER_HOST, tls = tls_config)
        if platform.system() == 'Linux':
            docker_client = Client(base_url='unix://var/run/docker.sock')

        build = self.model()
        self.validate_tag(tag)
        build.tag = tag
        image_name = "soma.buildbuild.io:4000/" + Project.objects.get(id = project_id).name + "-" + tag
        build.project = Project.objects.get_project(project_id)
        Dockerfile = self.optimize_docker_text(project_id = project_id)

        try:
            Build.objects.get(project = build.project, is_active = True)
        except ObjectDoesNotExist:
            pass
        else:  
            old_build = Build.objects.get(project = build.project, is_active = True)
            docker_client.stop(container = old_build.container)

#       build.response = "".join([json.loads(line)["stream"] for line in 
        build.response = ([ line for line in 
#          docker_client.build(fileobj=open("/Users/Korniste/Developments/abc/Dockerfile"), tag=tag) ])
           docker_client.build(fileobj=Dockerfile, rm=True, tag=image_name) ])
 
        try:
            Build.objects.get(project = build.project, is_active = True)
        except ObjectDoesNotExist:
            pass
        else:
            old_build = Build.objects.get(project = build.project, is_active = True)
            docker_client.start(container = old_build.container , port_bindings = { 8080: old_build.port })

        build.image_name = image_name
        docker_client.push(repository=image_name, insecure_registry=True)
        build.save(using = self.db)
        return build

    def deploy_project(self, build_id, **kwargs):
        build = Build.objects.get(id=build_id)
        team_name = build.project.project_teams.all()[0].name
#       Darwin is OS X
        if platform.system() == 'Darwin':
            DOCKER_HOST = os.environ['DOCKER_HOST']
            DOCKER_HOST = DOCKER_HOST.replace('tcp', 'https')
            DOCKER_CERT_PATH = os.environ['DOCKER_CERT_PATH']
            cert_dir = os.environ['DOCKER_CERT_PATH'] + '/'
            tls_config = TLSConfig(
                 client_cert=(cert_dir + 'cert.pem', cert_dir + 'key.pem'), verify=False
            )
            docker_client = Client(base_url=DOCKER_HOST, tls = tls_config)
        if platform.system() == 'Linux':
            docker_client = Client(base_url='unix://var/run/docker.sock')
        image_name = build.image_name
        docker_client.pull(repository=image_name, insecure_registry=True)

        try:
            Build.objects.get(project = build.project, is_active = True)
        except ObjectDoesNotExist:
            pass
        else:  
            old_build = Build.objects.get(project = build.project, is_active = True)
            old_build.is_active = False
            old_build.save()
            docker_client.remove_container(container = old_build.container, force=True)
        if build.container == "empty":
            container = docker_client.create_container(
                image=image_name,
                name = team_name+"_"+build.project.name+"_"+build.tag,
                detach=True,
                ports = [ 8080 ]
            )
            build.container = container.get('Id')

        build.port = 10000 + build.project.id

        response = docker_client.start(container = build.container, port_bindings = { 8080 : build.port }) 
        build.is_active = True
        build.save()
        return response

    def optimize_docker_text(self, project_id):
        project = Project.objects.get_project(id = project_id)
        language = project.properties['language']
        version = project.properties['version']
        git_url = project.properties['git_url']
        branch_name = project.properties['branch_name']
        project_name = project.name
        docker_text = DockerText.objects.get(lang = language).docker_text
        docker_text = docker_text.replace("<x.y>", version[:3])
        docker_text = docker_text.replace("<x.y.z>", version)
        docker_text = docker_text.replace("<git_url>", git_url)
        docker_text = docker_text.replace("<branch_name>", branch_name)
        docker_text = docker_text.replace("<project_name>", project_name)
        return BytesIO(docker_text.encode('utf-8'))

    def validate_tag(self, tag):
        if len(tag) < 1:
            raise ValidationError("project tag length should be at most 15", )
        if len(tag) > 15:
            raise ValidationError("project tag max length is 15" , )

    def get_build(self, id):
        try:
            build = Build.objects.get(id = id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist
        else:
            return build

    def delete_build(self, id): 
        build = Build.objects.get_build(id)
        build.delete()
        if build.id is None:
            return True
        else:
            raise OperationalError("delete build failed")

class Build(models.Model):
    tag = models.CharField(max_length = 15)
    image_name = models.CharField(default = "", max_length = 200, unique = True)
    objects = BuildManager()
    project = models.ForeignKey(Project)
    is_active = models.BooleanField(default=True)
    created_time = models.DateField(auto_now_add=True)
    response = models.TextField(default="")
    container = models.CharField(default="empty", max_length = 50)
    port = models.IntegerField(default=10000)
    is_active = models.BooleanField(default=False)
