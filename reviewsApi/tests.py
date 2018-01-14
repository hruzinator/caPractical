# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client

from .models import Review, Company, ReviewerMetadata, ApiKey

from django.contrib.auth.models import User
import uuid

#API tests
class APITestCase(TestCase):
    def setUp(self):
        self.c = Client()
        #create a user
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        #create an API key for the user
        api_key = ApiKey.objects.create(user_id=user)
        self.userApiKey = api_key.key

        #log in
        self.c.post('/login/', {'username': 'temporary', 'password': 'temporary'})
        #create a company
        c = Company.objects.create(name="Jack in the Box", industry="Fast Food")
        #create a sample review metadata object
        rm = ReviewerMetadata.objects.create(name="Temporary User", email="temporary@gmail.com")
        #create a sample review (will get id 1, since it is the first created)
        Review.objects.create(
            title="I can tolerate Jack in the Box",
            company = c,
            rating = 3,
            summary = "Jack in the box makes sub-par burgers, but I didn't get sick from eating them",
            ip_address = '127.0.0.1',
            user_id = user,
            reviewer_metadata = rm
        )

        #create another sample review
        rm2 = ReviewerMetadata.objects.create(name="Temporary User", email="temporary@gmail.com")
        #create a sample review (will get id 1, since it is the first created)
        Review.objects.create(
            title="I actually find Jack in the box good for some reason",
            company = c,
            rating = 5,
            summary = "I enjoy jack in the box",
            ip_address = '127.0.0.1',
            user_id = user,
            reviewer_metadata = rm2
        )

        #create a final review that should not be accessible to our test user

        user2 = User.objects.create_user('someoneElse', 'otherPerson@gmail.com', 'cantTouchThis')
        rm3 = ReviewerMetadata.objects.create(name="Someone Else", email="otherPerson@gmail.com")
        #create a sample review (will get id 1, since it is the first created)
        Review.objects.create(
            title="Jack in the Box burnt my burger",
            company = c,
            rating = 1,
            summary = "This is actually a true story. I went to a Jack in the box and it took them 5 minuites in an empty line to procure a burger, after which, it was burnt.",
            ip_address = '127.0.0.1',
            user_id = user2,
            reviewer_metadata = rm3
        )

    def testPostReview(self):
        data = {
          "title": "Got sick from eating Jack in the Box",
          "rating": 1,
          "summary": "I ordered a burger from Jack in the Box one night. I awoke the next morning with food poisioning.",
          "company": 1,
          "api_key": self.userApiKey
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'Submission successful')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="Got sick from eating Jack in the Box")
        self.assertEqual(len(reviewObj), 1)

    def testSendBadApiKeyPostReview(self):
        data = {
          "title": "Sending bad API key",
          "rating": 1,
          "summary": "I ordered a burger from Jack in the Box one night. I awoke the next morning with food poisioning.",
          "company": 1,
          "api_key": uuid.uuid4() #generate a different uuid
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'Api Key could not be validated')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="Sending bad API key")
        self.assertEqual(len(reviewObj), 0)

    def testSendNoApiKeyPostReview(self):
        data = {
          "title": "Not sending an api key",
          "rating": 1,
          "summary": "I ordered a burger from Jack in the Box one night. I awoke the next morning with food poisioning.",
          "company": 1,
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'API key required to acess this part of the API')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="Not sending an api key")
        self.assertEqual(len(reviewObj), 0)

    def testSendBadCompanyIDPostReview(self):
        data = {
          "title": "testing bad id",
          "rating": 1,
          "summary": "I ordered a burger from Jack in the Box one night. I awoke the next morning with food poisioning.",
          "company": 50,
          "api_key": self.userApiKey
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'Company id not found')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="testing bad id")
        self.assertEqual(len(reviewObj), 0)

        data["company"] = "a string"
        data["title"] = "testing another bad id"
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'invalid company id format')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="testing another bad id")
        self.assertEqual(len(reviewObj), 0)

    def testMissingTitlePostReview(self):
        data = {
          "rating": 1,
          "summary": "I think titles are stupid",
          "company": 1,
          "api_key": self.userApiKey
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'Missing required field')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(summary="I think titles are stupid")
        self.assertEqual(len(reviewObj), 0)

    def testMissingSummaryPostReview(self):
        data = {
          "title": "This title is so good I dont need a summary!",
          "rating": 1,
          "company": 1,
          "api_key": self.userApiKey
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'Missing required field')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="This title is so good I dont need a summary!")
        self.assertEqual(len(reviewObj), 0)

    def testMissingRatingPostReview(self):
        data = {
          "title": "This title is so good I dont need a rating!",
          "summary": "test",
          "company": 1,
          "api_key": self.userApiKey
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'Missing required field')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="This title is so good I dont need a rating!")
        self.assertEqual(len(reviewObj), 0)

    def testMissingCompanyIDPostReview(self):
        data = {
          "title": "This title is so good I don\'t need a company id!",
          "summary": "test",
          "rating": 1,
          "api_key": self.userApiKey
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'Missing required field')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="This title is so good I don\'t need a company id!")
        self.assertEqual(len(reviewObj), 0)

    def testBadRatingPostReview(self):
        data = {
          "title": "testing bad rating",
          "rating": -7,
          "summary": "I ordered a burger from Jack in the Box one night. I awoke the next morning with food poisioning.",
          "company": 50,
          "api_key": self.userApiKey
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'rating needs to be a whole number from 1 to 5 inclusive')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="testing bad rating")
        self.assertEqual(len(reviewObj), 0)

        data['title'] = "another bad rating"
        data['rating']= 10
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'rating needs to be a whole number from 1 to 5 inclusive')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="another bad rating")
        self.assertEqual(len(reviewObj), 0)

        data['title'] = "non-whole number bad rating"
        data['rating'] = 1.5
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'rating needs to be a whole number from 1 to 5 inclusive')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="non-whole number bad rating")
        self.assertEqual(len(reviewObj), 0)

    def testSendLongTitlePostReview(self):
        data = {
          "title": 'A'*65,
          "rating": 1,
          "summary": "I ordered a burger from Jack in the Box one night. I awoke the next morning with food poisioning.",
          "company": 1,
          "api_key": self.userApiKey
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'Title can be no longer than 64 characters')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title='A'*65)
        self.assertEqual(len(reviewObj), 0)

    def testSendLongSummaryPostReview(self):
        data = {
          "title": "The summary should be too long to post",
          "rating": 1,
          "summary": 'A'*10001,
          "company": 1,
          "api_key": self.userApiKey
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'Summary can be no longer than 10,000 characters')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="The summary should be too long to post")
        self.assertEqual(len(reviewObj), 0)

    def testGetReview(self):
        response = self.c.post('/api/getReview/1/', {"api_key" : self.userApiKey})
        self.assertEqual(response.status_code, 200)
        j = response.json()["fields"]
        self.assertEqual(j["title"], "I can tolerate Jack in the Box")
        self.assertEqual(j["rating"], 3)
        self.assertEqual(j["summary"], "Jack in the box makes sub-par burgers, but I didn't get sick from eating them")

    def testBadApiKeyGetReview(self):
        response = self.c.post('/api/getReview/1/', {"api_key" : uuid.uuid4()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Api Key could not be validated')

    def testNoApiKeyGetReview(self):
        response = self.c.post('/api/getReview/1/', {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'API key required to acess this part of the API')

    def testGetNonExistantReview(self):
        response = self.c.post('api/getReview/100/', {"api_key" : self.userApiKey})
        self.assertEqual(response.status_code, 404)

    def testGetMyReviews(self):
        response = self.c.post('/api/getOwnReviews/', {"api_key" : self.userApiKey})
        j = response.json()
        j0 = j[0]["fields"]
        j1 = j[1]["fields"]
        self.assertEqual(j0['title'], 'I can tolerate Jack in the Box')
        self.assertEqual(j1['title'], 'I actually find Jack in the box good for some reason')

    def testBadApiKeyGetMyReviews(self):
        response = self.c.post('/api/getOwnReviews/', {"api_key" : uuid.uuid4()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Api Key could not be validated')

    def testNoApiKeyGetMyReviews(self):
        response = self.c.post('/api/getOwnReviews/', {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'API key required to acess this part of the API')

    def testGetUnauthorizedReview(self):
        response = self.c.post('/api/getReview/3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Access Denied')
        self.c.get('/logout/')
        response = self.c.post('/api/getReview/1/', {"api_key" : self.userApiKey})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Please log in.')

    def testPostUnauthorized(self):
        self.c.get('/logout/')
        data = {
          "title": "test posting a review while logged out",
          "rating": 1,
          "summary": "I ordered a burger from Jack in the Box one night. I awoke the next morning with food poisioning.",
          "company": 1
        }
        response = self.c.post("/api/postReview/", data)
        self.assertEqual(response.content, b'Please log in.')
        self.assertEqual(response.status_code, 200)
        reviewObj = Review.objects.filter(title="test posting a review while logged out")
        self.assertEqual(len(reviewObj), 0)

    def testGetMyReviewsLogout(self):
        self.c.get('/logout/')
        response = self.c.post('/api/getOwnReviews/', {"api_key" : self.userApiKey})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Please log in.')
