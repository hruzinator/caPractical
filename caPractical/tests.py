# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client

# from .models import Review, Company, ReviewerMetadata

from django.contrib.auth.models import User

#view tests
class viewsTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def testBadUrl(self):
        response = self.c.get('/failure')
        self.assertEqual(response.status_code, 404)

    def testUnauthenticatedNavigation(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def testUserCreation(self):
        pass
    def testAuthenticatedNavigation(self):
        pass
    def testChangeSettings(self):
        pass
    def testChangePassword(self):
        pass
    def testLogout(self):
        pass
