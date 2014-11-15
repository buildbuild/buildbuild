from django.shortcuts import render
from django.http import HttpResponse
from dockerbuild.models import Build
from projects.models import Project

def build_page(request, project_id):
    return render(
            request,
            "dockerbuild/build_page.html",
            { 
                "project" : Project.objects.get_project(id=project_id),
                "project_id" : project_id,
            }   
    )
def build_new(request, project_id):
    if "tag" in request.GET:
        tag = request.GET['tag']
        build = Build.objects.build_project(project_id=project_id, tag=tag)
        project = Project.objects.get_project(project_id)
    else:
        raise ValueError("You must type tag name")
    return render(
            request,
            "dockerbuild/build_new.html",
            {
                "project" : project,
                "build" : build,
            }
    ) 
