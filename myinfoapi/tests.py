from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
class MyModelAPITestCase(APITestCase):
    def setUp(self):
        self.singpass_auth_url = '/singpass-auth/'
        self.singpass_auth_url_callback = '/singpass-auth/callback'

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Generate JWT token for the test user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Set the credentials for the test client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_get_singpass_auth(self):
        response = self.client.get(self.singpass_auth_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_singpass_auth_callback_empty_code(self):
        response = self.client.get(self.singpass_auth_url_callback)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_singpass_auth_unauthenticated(self):
        # Remove authentication headers
        self.client.credentials()

        response = self.client.get(self.singpass_auth_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_singpass_auth_callback_unauthenticated(self):
        # Remove authentication headers
        self.client.credentials()

        response = self.client.get(self.singpass_auth_url_callback)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
