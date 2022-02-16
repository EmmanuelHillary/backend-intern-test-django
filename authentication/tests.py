from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

User = get_user_model()

class AuthTests(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create(
            first_name='john',
            last_name='snow',
            email='john@snow.com',
            password='johnpassword',
            phone_number='123456667'
            )

    def test_create_account(self):
        url = reverse('register')
        data = {
            'first_name': 'test_first',
            'last_name': 'test_last',
            'email': 'test_mail@mail.com',
            'phone_number': '123456789',
            'password': 'testpassword123',
            'password2': 'testpassword123',
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().first_name, 'test_first')
        self.assertEqual(User.objects.first().last_name, 'snow')
    
    def test_email_exists(self):
        url = reverse('register')
        data = {
            'first_name': 'test_first',
            'last_name': 'test_last',
            'email': 'john@snow.com',
            'phone_number': '123456789',
            'password': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().first_name, 'john')
    
    def test_login(self):
        login_url = reverse('login')
        register_url = reverse('register')
        data = {
            'first_name': 'test_first',
            'last_name': 'test_last',
            'email': 'test@user.com',
            'phone_number': '123456789',
            'password': 'testpassword123',
            'password2': 'testpassword123',
        }
        login_data = {
            'username': 'test@user.com',
            'password': 'testpassword123'
        }

        
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['access']
        self.assertEqual(login_response.status_code, 200)

        token_verify_url = reverse('token_verify')
        token_response = self.client.post(token_verify_url, {'token': token}, format='json')
        self.assertEqual(token_response.status_code, 200)

