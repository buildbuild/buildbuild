# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'users/index.html')

def login(request):
    return HttpResponse('Login Page')

def signin(request):
    return HttpResponse('회원가입 페이지')
