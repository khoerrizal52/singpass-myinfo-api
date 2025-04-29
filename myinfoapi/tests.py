from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.
class MyModelAPITestCase(APITestCase):
    def setUp(self):
        self.singpass_auth_url = '/singpass-auth/'
        self.singpass_auth_url_callback = '/singpass-auth/callback'

    def test_get_singpass_auth(self):
        response = self.client.get(self.singpass_auth_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_singpass_auth_callback_empty_code(self):
        response = self.client.get(self.singpass_auth_url_callback)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
