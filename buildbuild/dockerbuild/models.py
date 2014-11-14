from django.db import models
from projects.models import Project, ProjectManager
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from properties.models import DockerText

from docker import Client
from io import BytesIO

class BuildManager(models.Manager):
    def build_project(self, project_id, tag, **kwargs):
        build = self.model()
        self.validate_tag(tag)
    
        build.tag = "soma.buildbuild.io:4000/" + Project.objects.get(id = project_id).name + "-" + tag
        
        build.project = Project.objects.get_project(project_id)
    
        Dockerfile = self.optimize_docker_text(project_id = project_id)

        docker_client = Client(base_url='192.168.59.103:2375')

        response = [line for line in 
               docker_client.build(fileobj=open("/Users/Korniste/Developments/abc/Dockerfile"), tag=build.tag) ]

        build.save(using = self.db)
    
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
        if len(tag) >15:
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
    tag = models.CharField(max_length = 15, unique = True)
    objects = BuildManager()
    project = models.ForeignKey(Project)
    is_active = models.BooleanField(default=True)
    created_time = models.DateField(auto_now_add=True)
