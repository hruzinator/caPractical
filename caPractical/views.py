# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django.contrib.auth.models import User
from reviewsApi.models import Company

def index(request):
    if request.user.is_authenticated:
        template = loader.get_template("index.html")
        return HttpResponse(template.render({}, request))
    else:
        return redirect("site_login")


def site_login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return HttpResponse("login failed")
    else:
        #render a login page template
        template = loader.get_template("login.html")
        return HttpResponse(template.render({}, request))

def site_logout(request):
    logout(request)
    return redirect("site_login")
