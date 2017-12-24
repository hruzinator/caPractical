# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Review, Company, ReviewerMetadata

admin.site.register(Review)
admin.site.register(Company)
admin.site.register(ReviewerMetadata)
