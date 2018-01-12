# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

import uuid

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=64)
    company = models.ForeignKey('Company', on_delete=models.PROTECT)
    rating = models.PositiveSmallIntegerField() #range is 1-5
    summary = models.CharField(max_length=10000)
    ip_address = models.GenericIPAddressField(protocol='both')
    submission_date = models.DateField(auto_now=True) #timestamp review
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    reviewer_metadata = models.ForeignKey(
        'ReviewerMetadata',
        on_delete=models.CASCADE
    )

class Company(models.Model):
    name = models.CharField(max_length=254)
    industry = models.CharField(max_length=254)

class ReviewerMetadata(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
