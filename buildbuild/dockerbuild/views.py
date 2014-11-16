from django.shortcuts import render, redirect
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

def deploy(request, build_id):
    Build.objects.deploy_project(build_id = build_id)
    return render(
            request,
            'dockerbuild/deploy.html',
            {
                "project" : Build.objects.get(id = build_id).project, 
                "build" : Build.objects.get(id = build_id) 
            }
    )
def my_project(request, project_id):
    my_project_address = "http://192.168.59.103:"+ str( int(project_id)+int(10000) )  
    return redirect(my_project_address)
