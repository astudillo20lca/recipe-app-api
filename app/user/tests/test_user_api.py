"""test for the user API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """create and return a new user"""

    return get_user_model().objects.create_user(**params)

# we separate tests for public features of the API
class PublicUserAPITest(TestCase):
    """test the public features of the user API"""

    def setUP(self):
        self.client = APIClient()

    def test_create_user_successs(self):
        """test creating a user is successful"""

        payload = {
            'email':'test@example.com',
            'password': 'testpass123',
            'name':'Test Name'
        }

        res = self.client.post(CREATE_USER_URL,payload)
        # test successful code
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # validate the user registed correctly
        user = get_user_model().objects.get(email=payload['email'])
        
        self.assertTrue(user.check_password(payload['password']))

        # make sure the password does not come back in the response
        self.assertnotIn('password',res.data)

    def test_user_with_email_exists_error(self):
        """test error returned if user with email exists"""
        
        payload = {
            'email':'test@example.com',
            'password': 'testpass123',
            'name':'Test Name'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """test an error is returned if password less than 4 chars"""


        payload = {
            'email':'test@example.com',
            'password': 'pili',
            'name':'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # returns true if user exists
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)
