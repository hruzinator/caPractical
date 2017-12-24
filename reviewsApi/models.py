# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=64)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField() #range is 1-5
    summary = models.CharField(max_length=10000)
    ip_address = models.GenericIPAddressField(protocol='both')
    submission_date = models.DateField(auto_now=True) #timestamp review
    reviewer_metadata = models.ForeignKey(
        'ReviewerMetadata',
        on_delete=models.CASCADE
    )

class Company(models.Model):
    company_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=254)
    industry = models.CharField(max_length=254)

class ReviewerMetadata(models.Model):
    reviewer_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    # user_id = models.ForeignKey (actual user)
