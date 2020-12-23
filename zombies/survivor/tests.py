from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token

class SurvivorTest(APITestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        token = Token.objects.get(user__username="survivor1")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_valid_survivor(self):
        payload = {"name": "survivor-tokyo",                         
                    "gender": "M",
                    "latitude": 35.689,
                    "longitude": 139.692}
        
        response = self.client.post('/api/v1/survivor/',
                                    data=payload,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_survivor(self):
        payloads = ({'name':''}, {'name': 'valid', 'gender': 'M'}, 
                        {}, {'latitude': 'string'})
        for payload in payloads:
            response = self.client.post('/api/v1/survivor/',
                                        data=payload,
                                        format='json')
            self.assertRaises(ValidationError)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
