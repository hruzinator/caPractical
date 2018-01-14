# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate, login
from .models import Review, Company, ReviewerMetadata, ApiKey
from django.template import loader
from django.core import serializers
import json
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def postReview(request):
    if request.user.is_authenticated == False:
        return HttpResponse("Please log in.")

    #get values from request
    try:
        title = request.POST["title"]
        rating = request.POST["rating"]
        company_id = request.POST["company"]
        summary = request.POST["summary"]
    except MultiValueDictKeyError:
        return HttpResponse("Missing required field")

    #special error message for API key
    try:
        api_key = request.POST["api_key"]
    except:
        return HttpResponse("API key required to acess this part of the API")
    if validApiKey(request.user, api_key) == False:
        return HttpResponse("Api Key could not be validated")

    try:
        r = int(rating)
    except ValueError:
        return HttpResponse("rating needs to be a whole number from 1 to 5 inclusive")

    if r < 1 or r > 5:
        return HttpResponse("rating needs to be a whole number from 1 to 5 inclusive")

    if len(title) > 64:
        return HttpResponse("Title can be no longer than 64 characters")

    if len(summary) > 10000:
        return HttpResponse("Summary can be no longer than 10,000 characters")

    try:
        company_id = int(company_id)
    except ValueError:
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
        title = title,
        rating = r,
        summary = summary,
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

    #TODO check that the method type is POST?

    #note: does not error out since django returns 404 for non-existant review id
    review = Review.objects.get(pk=reviewId)
    if request.user != review.user_id:
        return HttpResponse("Access Denied")

    try:
        api_key = request.POST["api_key"]
    except:
        return HttpResponse("API key required to acess this part of the API")
    if validApiKey(request.user, api_key) == False:
        return HttpResponse("Api Key could not be validated")

    data = serializers.serialize('json', [review,])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, content_type='application/json')

def getOwnReviews(request):
    if request.user.is_authenticated == False:
        return HttpResponse("Please log in.")

    try:
        api_key = request.POST["api_key"]
    except:
        return HttpResponse("API key required to acess this part of the API")
    if validApiKey(request.user, api_key) == False:
        return HttpResponse("Api Key could not be validated")

    reviewSet = Review.objects.filter(user_id=request.user)
    data = serializers.serialize('json', reviewSet)
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type='application/json')


#helper method
def validApiKey(user, apiKey):
    matched_keys = ApiKey.objects.filter(user_id=user)
    for entry in matched_keys:
        keyStr = entry.key.urn[9:] #gets urn value. Strips away `urn:uuid:`
        if keyStr == apiKey:
            return True
    return False
