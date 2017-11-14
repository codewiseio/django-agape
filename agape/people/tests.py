from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

import json
from django.utils import timezone
from datetime import timedelta

# Create your tests here.
from .models import Person
from .serializers import PersonSerializer
# from .settings import AUTHENTICATION

class PersonTestCase(TestCase):
    def setUp(self):
        pass

    def test_sanity(self):
        self.assertTrue(True, "Sane")

    def test_create(self):
        instance = Person(first_name="Elvis",middle_name="Aaron",last_name="Presley", birthday="1935-01-08", gender="m")
        instance.save()

        self.assertEqual(instance.id, 1, 'Person assigned new ID')
        self.assertEqual(instance.first_name, "Elvis")
        self.assertEqual(instance.middle_name, "Aaron")
        self.assertEqual(instance.middle_name, "Aaron")
        self.assertEqual(instance.last_name, "Presley")
        self.assertEqual(instance.birthday, "1935-01-08")
        self.assertEqual(instance.gender, "m")



class PersonSerializerTestCase(TestCase):

    def setUp(self):
        pass

    def test_serialize(self):
        instance = Person(first_name="Elvis",middle_name="Aaron",last_name="Presley", birthday="1935-01-08", gender="m")
        instance.save()

        serializer = PersonSerializer(instance)

        expect = {
            'id':1,
            'first_name':'Elvis',
            'middle_name':'Aaron',
            'last_name':'Presley',
            'birthday': "1935-01-08",
            'gender': 'm',
            'title': None
        }

        self.assertDictEqual(expect, serializer.data)

    def test_inflate(self):

        data = {
            'first_name':'Elvis',
            'middle_name':'Aaron',
            'last_name':'Presley',
            'birthday': "1935-01-08",
            'gender': 'm',
            'title': None
        }

        # serializer data is valid
        serializer = PersonSerializer(data=data)
        self.assertTrue(serializer.is_valid(), 'Serializer data is valid')

        # create an instance via the serializer
        instance = serializer.create(serializer.validated_data)
        self.assertTrue(instance, 'Created instance from serializer data')

        # verify instance values
        self.assertEqual(instance.id, 1, 'Person assigned new ID')
        self.assertEqual(instance.first_name, "Elvis")
        self.assertEqual(instance.middle_name, "Aaron")
        self.assertEqual(instance.middle_name, "Aaron")
        self.assertEqual(instance.last_name, "Presley")
        self.assertEqual(instance.birthday.strftime('%Y-%m-%d'), "1935-01-08" )
        self.assertEqual(instance.gender, "m")
        self.assertEqual(instance.title, None)

        # verify partial modification
        data = {
            'id': instance.id,
            'title': 'Mr.'
        }
        serializer = PersonSerializer(data=data,partial=True)
        self.assertTrue(serializer.is_valid(), 'Serializer data is valid')

        # update the instance
        serializer.update(instance,data)
        self.assertEqual(instance.title, 'Mr.')

class APITestCase(TestCase):

    def setup(self):
        self.client =  APIClient()

    def test_create_person(self):

        data = {
            'first_name':'Elvis',
            'middle_name':'Aaron',
            'last_name':'Presley',
            'birthday': "1935-01-08",
            'gender': 'm'
        }        
        response = self.client.post('/api/v1/people/', data)
        self.assertEqual(response.status_code, 201, "Created new person")
        
        self.assertEqual(response.data.get('id'), 1, 'Person assigned new ID')
        self.assertEqual(response.data.get('first_name'), "Elvis")
        self.assertEqual(response.data.get('middle_name'), "Aaron")
        self.assertEqual(response.data.get('last_name'), "Presley")
        self.assertEqual(response.data.get('birthday'), "1935-01-08" )
        self.assertEqual(response.data.get('gender'), "m")
        self.assertEqual(response.data.get('title'), None)

        # verify actual database record was created
        instance = Person.objects.get(id=response.data.get('id'))
        self.assertTrue(instance)

    def test_retrieve(self):
        data = {
            'first_name':'Elvis',
            'middle_name':'Aaron',
            'last_name':'Presley',
            'birthday': "1935-01-08",
            'gender': 'm'
        }      
        response = self.client.post('/api/v1/people/', data)
        self.assertEqual(response.status_code, 201, "Created new person")
        
        response = None
        response = self.client.get('/api/v1/people/1/')
        self.assertEqual(response.data.get('id'),1,"Retrieved")
        self.assertEqual(response.data.get('first_name'), "Elvis")
        self.assertEqual(response.data.get('middle_name'), "Aaron")
        self.assertEqual(response.data.get('last_name'), "Presley")
        self.assertEqual(response.data.get('birthday'), "1935-01-08" )
        self.assertEqual(response.data.get('gender'), "m")
        self.assertEqual(response.data.get('title'), None)

    def test_update_person(self):

        data = {
            'first_name':'Elvis',
            'middle_name':'Aaron',
            'last_name':'Presley',
            'birthday': "1935-01-08",
            'gender': 'm'
        }      
        response = self.client.post('/api/v1/people/', data)
        self.assertEqual(response.status_code, 201, "Created new person")
        self.assertEqual(response.data.get('title'), None)

        data = { 'title':'Mr.' } 
        response = self.client.patch( 
            '/api/v1/people/{}/'.format(response.data.get('id')),
             json.dumps(data),
              content_type='application/json')
        self.assertEqual(response.data.get('title'), 'Mr.')

        # verify actual database record
        instance = Person.objects.get(id=response.data.get('id'))
        self.assertTrue(instance)
        self.assertEqual(instance.title,'Mr.')

    def test_delete_person(self):
        data = {
            'first_name':'Elvis',
            'middle_name':'Aaron',
            'last_name':'Presley',
            'birthday': "1935-01-08",
            'gender': 'm'
        }  
        response = self.client.post('/api/v1/people/', data)
        self.assertEqual(response.status_code, 201, "Created new person")
        id = response.data.get('id')

        uri = '/api/v1/people/{}/'.format(response.data.get('id'))
        response = self.client.delete( uri )    
        self.assertEqual(response.status_code, 204, "Deleted")

        query = Person.objects.filter(id=id)
        self.assertEqual(len(query),0, "Deleted")





