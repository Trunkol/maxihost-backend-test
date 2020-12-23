from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from .models import Survivor, InfectedSurvivor

class SurvivorTest(APITestCase):
    fixtures = ['users.json', 'survivors.json']

    def setUp(self) -> None:
        token = Token.objects.get(user__username="survivor1")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_valid_survivor(self):
        username_payload = {"username": "survivor-tokyo",
                            "password": '123',
                            "email": 'a@email.com'}
        
        response = self.client.post('/api/v1/users/',
                                    data=username_payload,
                                    format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)        
        
        token = Token.objects.get(user__username="survivor-tokyo")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

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

    def test_user_update_valid_survivor_error(self):
        payload = {"name": "survivor-tokyo-1",
                    "gender": "M",
                    "latitude": 10.689,
                    "longitude": 10.692}
        
        token = Token.objects.get(user__username="survivor1")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        survivor = Survivor.objects.get(user__username='survivor1')

        response = self.client.put(f'/api/v1/survivor/{survivor.pk}/',
                                    data=payload,
                                    format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['name'], response.json()['name'])
        self.assertEqual(payload['gender'], response.json()['gender'])
    
    def test_infect_a_user(self):
        survivor = Survivor.objects.get(user__username='survivor1')
        self.assertEqual(survivor.infected, False)
        for username in ('survivor3', 'survivor2', 'survivor4'):
            token = Token.objects.get(user__username=username)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            response = self.client.post(f'/api/v1/survivor/{survivor.pk}/infect/',
                                        data={},
                                        format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        survivor = Survivor.objects.get(user__username='survivor1')
        self.assertEqual(survivor.infected, True)

    def test_infect_a_survivor_double_times_by_same(self):
        survivor = Survivor.objects.get(user__username='survivor1')
        self.assertEqual(survivor.infected, False)
        for username in ('survivor2', 'survivor2'):
            token = Token.objects.get(user__username=username)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            response = self.client.post(f'/api/v1/survivor/{survivor.pk}/infect/',
                                        data={},
                                        format='json')        
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_get_nearest_survivor(self):
        survivor = Survivor.objects.get(name='survivor-sp')
        response = self.client.get(f'/api/v1/survivor/{survivor.pk}/closest/',
                                    format='json')       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    