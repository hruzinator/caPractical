# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate, login
from .models import Review, Company, ReviewerMetadata
from django.template import loader

# Create your views here.
def postReview(request):
    if request.user.is_authenticated == False:
        return HttpResponse("Please log in.")
    title = request.POST["title"]
    rating = request.POST["rating"]
    summary = request.POST["summary"]
    ip_addr = request.get_host()
    company = request.POST["company"]
    reviewer_metadata = ReviewerMetadata(
        name=request.user.first_name+" "+request.user.last_name,
        email=request.user.email
    )
    return HttpResponse("placeholder")

def getReview(request):
    if request.user.is_authenticated == False:
        return HttpResponse("Please log in.")
    else:
        return JsonResponse({'test': 'placehoder'})
