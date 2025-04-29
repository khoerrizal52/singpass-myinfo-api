from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class UserAuthenticationTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "username": "johndoe",
            "email": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "TestPassword123!",
            "password2": "TestPassword123!"
        }

    def test_user_registration(self):
        """
        Ensure we can register a new user.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_user_login(self):
        """
        Ensure registered user can log in and receive JWT tokens.
        """
        # First register
        self.client.post(self.register_url, self.user_data, format='json')

        # Now login
        login_data = {
            "username": "johndoe",
            "password": "TestPassword123!"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        """
        Ensure login fails with incorrect credentials.
        """
        # First register
        self.client.post(self.register_url, self.user_data, format='json')

        # Attempt login with wrong password
        login_data = {
            "username": "johndoe",
            "password": "WrongPassword"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
