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
        template = loader.get_template("login.html")
        return HttpResponse(template.render({}, request))


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

def signup(request):
    if request.user.is_authenticated:
        return redirect("settings")
    if request.method == 'GET':
        template = loader.get_template("signUp.html")
        return HttpResponse(template.render({}, request))
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_name = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['passwordConfirmation']

        #TODO data validation checks
        if password != confirm_password:
            return HttpResponse("Passwords do not match!")

        newUser = User.objects.create_user(username, email_name, password)
        newUser.first_name = first_name
        newUser.last_name = last_name
        newUser.save()
        return redirect("index")

def settings(request):
    if request.user.is_authenticated is False:
        return redirect("signup")
    if request.method == 'GET':
        template = loader.get_template("userSettings.html")
        return HttpResponse(template.render({}, request))
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_name = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['passwordConfirmation']

        #TODO update the user

        return redirect("index")


def submitReview(request):
    if request.user.is_authenticated is False:
        return redirect("signup")
    c_list = Company.objects.all()
    template = loader.get_template("postReview.html")
    return HttpResponse(template.render({"companies":c_list}, request))

#TODO
def getReviews(request):
    return HttpResponse("placeholder")
