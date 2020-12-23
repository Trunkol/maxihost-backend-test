from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token

class SurvivorTest(APITestCase):
    fixtures = ['users.json', 'survivors.json']

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

    def test_create_and_update_valid_survivor(self):
        payload = {"name": "survivor-tokyo",                         
                    "gender": "M",
                    "latitude": 21.689,
                    "longitude": 139.692}
        
        response = self.client.post('/api/v1/survivor/',
                                    data=payload,
                                    format='json')

        self.assertEqual(21.689, float(response.json()['latitude']))
        self.assertEqual(139.692, float(response.json()['longitude']))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = response.json()
        payload['latitude'] = 10.123
        payload['longitude'] = 130.123
        
        response = self.client.put(f'/api/v1/survivor/{response["id"]}/',
                                    data=payload,
                                    format='json')
        
        self.assertEqual(10.123, float(response.json()['latitude']))
        self.assertEqual(130.123, float(response.json()['longitude']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_and_with_another_user_update_valid_survivor_error(self):
        payload = {"name": "survivor-tokyo",                         
                    "gender": "M",
                    "latitude": 21.689,
                    "longitude": 139.692}
        
        response = self.client.post('/api/v1/survivor/',
                                    data=payload,
                                    format='json')

        self.assertEqual(21.689, float(response.json()['latitude']))
        self.assertEqual(139.692, float(response.json()['longitude']))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = response.json()
        payload['latitude'] = 10.123
        payload['longitude'] = 130.123
        token = Token.objects.get(user__username="survivor2")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.put(f'/api/v1/survivor/{response["id"]}/',
                                    data=payload,
                                    format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_infect_a_user(self):
        token = Token.objects.get(user__username="survivor1")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post('/api/v1/survivor/1/infect/',
                                    data={},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)