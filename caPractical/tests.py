# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client

from django.contrib.auth.models import User
from reviewsApi.models import ApiKey

#view tests
class viewsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.user_logged_out = Client()
        self.user_logged_in = Client()
        api_key = ApiKey.objects.create(user_id=user)
        self.userApiKey = api_key.key
        #log in
        self.user_logged_in.post('/login/', {'username': 'temporary', 'password': 'temporary'})

    def testBadUrl(self):
        response = self.user_logged_out.get('/failure')
        self.assertEqual(response.status_code, 404)
        response = self.user_logged_in.get('/failure')
        self.assertEqual(response.status_code, 404)

    def testUnauthenticatedNavigation(self):
        response = self.user_logged_out.get('/')
        self.assertRedirects(response, '/login/')

        response = self.user_logged_out.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def testAuthenticatedNavigation(self):
        response = self.user_logged_in.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

        response = self.user_logged_in.get('/login/')
        self.assertRedirects(response, '/')

    def testBadLogin(self):
        response = self.user_logged_out.post('/login/', {'username': 'temporary', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'login failed')
        self.assertEqual(len(self.user_logged_out.cookies), 0)
        self.user_logged_out.logout()

    def testGoodLogin(self):
        user2 = User.objects.create_user('temporary2', 'temporary2@gmail.com', 'temporary2')
        c = Client()
        c.logout()
        response = c.post('/login/', {'username': 'temporary2', 'password': 'temporary2'})
        self.assertRedirects(response, '/')
        self.assertEqual(user2.is_authenticated, True)

    def testLogout(self):
        response = self.user_logged_in.get('/logout/')
        self.assertRedirects(response, '/login/')
        #assert we can no longer reach parts of the site
        response = self.user_logged_in.get('/')
        self.assertRedirects(response, '/login/')
