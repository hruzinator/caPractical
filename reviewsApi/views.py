# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate, login
from .models import Review, Company, ReviewerMetadata
from django.template import loader
from django.core import serializers
import json

# Create your views here.
def postReview(request):
    if request.user.is_authenticated == False:
        return HttpResponse("Please log in.")

    try:
        r = int(request.POST["rating"])
    except:
        return HttpResponse("rating needs to be a whole number from 1 to 5 inclusive")

    if r < 1 or r > 5:
        return HttpResponse("rating needs to be a whole number from 1 to 5 inclusive")

    try:
        company_id = int(request.POST["company"])
    except:
        return HttpResponse("invalid company id format")

    c_query = Company.objects.filter(id=company_id)
    if len(c_query) == 0:
        return HttpResponse("Company id not found")

    company_obj = c_query[0]

    rm = ReviewerMetadata(
        name=request.user.first_name+" "+request.user.last_name,
        email=request.user.email
    )
    rm.save()

    review = Review(
        title = request.POST["title"],
        rating = r,
        summary = request.POST["summary"],
        ip_address = request.get_host(),
        company = company_obj,
        user_id = request.user,
        reviewer_metadata = rm
    )
    review.save()

    return HttpResponse("Submission successful")

def getReview(request, reviewId):
    if request.user.is_authenticated == False:
        return HttpResponse("Please log in.")

    #note: does not error out since django returns 404 for non-existant review id
    review = Review.objects.get(pk=reviewId)
    if request.user != review.user_id:
        return HttpResponse("Access Denied")
    #TODO api tokens
    data = serializers.serialize('json', [review,])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, content_type='application/json')

def getOwnReviews(request):
    if request.user.is_authenticated == False:
        return HttpResponse("Please log in.")
    reviewSet = Review.objects.filter(user_id=request.user)
    data = serializers.serialize('json', reviewSet)
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type='application/json')
