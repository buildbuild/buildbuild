from django.shortcuts import render
from django.http import HttpResponse
from dockerbuild.models import Build

def build(request, project_id):
    if "tag_name" in request.GET:
        tag_name = request.GET['tag_name']
        Build.objects.build_project(project_id=project_id, tag=tag_name)
    else:
        raise ValueError("You must type tag name")
    return HttpResponse("Hello")
