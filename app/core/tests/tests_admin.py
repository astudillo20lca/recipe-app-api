"""tests for django admin notifications"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    """Tests for django admin"""

    def setUp(self):
        """create user and client"""

        self.client = Client()
        # create superuser
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
        email = 'user@example.com',
        password = 'testpass123',
        name = 'test user'
        )

    def test_users_list(self):
        """tests that users are listed on pange"""
        # page with the list of users
        url = reverse('admin:core_user_changelist')
        
        # response object
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

