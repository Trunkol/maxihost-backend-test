
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token

class UserTest(APITestCase):
    
    def setUp(self) -> None:
        pass

    def test_create_valid_user(self):
        payload = {"username": "survivor-tokyo",                         
                    "password": "123",
                    "email": 'a@mail.com'}
        
        response = self.client.post('/api/v1/users/',
                                    data=payload,
                                    format='json')
        token = Token.objects.get(user__username="survivor-tokyo")
        
        print(token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_survivor(self):
        payloads = ({'username':''}, {'username': 'valid', 'password': 'M'}, {}, {'email': 'string'})
        for payload in payloads:
            response = self.client.post('/api/v1/users/',
                                        data=payload,
                                        format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
