from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

from agape.signals import on

import json
from django.utils import timezone
from datetime import timedelta
import datetime

# Create your tests here.
from .models import Person
from .serializers import PersonSerializer
# from .settings import AUTHENTICATION
# 

MODEL = Person
SERIALIZER_CLASS = PersonSerializer
CREATE_DATA =  {   
        'first_name':'Elvis',
        'middle_name':'Aaron',
        'last_name':'Presley',
        'birthday': datetime.date(1935, 1, 8),
        'gender': 'm'
    }
EXPECT_DATA = {   
    'id':1,
    'first_name':'Elvis',
    'middle_name':'Aaron',
    'last_name':'Presley',
    'birthday': datetime.date(1935, 1, 8),
    'gender': 'm',
    'title': None
}

UPDATE_DATA = { 
    'title': 'Mr.'
}
UPDATE_EXPECT_DATA= {   
    'id':1,
    'first_name':'Elvis',
    'middle_name':'Aaron',
    'last_name':'Presley',
    'birthday': datetime.date(1935, 1, 8),
    'gender': 'm',
    'title': 'Mr.'
}

class PersonTestCase(TestCase):

    def setUp(self):
        self.model              = MODEL
        self.serializer_class   = SERIALIZER_CLASS
        self.create_data        = CREATE_DATA
        self.expect_data        = EXPECT_DATA
        self.update_data        = UPDATE_DATA
        self.update_expect_data = UPDATE_EXPECT_DATA

    def test_create(self):
        instance = self.model(**self.create_data)
        instance.save()

        # compare instance to expected data
        for key in self.expect_data.keys():
            instance_value = getattr(instance, key)
            expected_value = self.expect_data[key]
            self.assertEqual(instance_value, expected_value, "Comparing {} attribute".format(key) )

    def test_update(self):
        instance = self.model(**self.create_data)
        instance.save()

        # update the instance
        for key, value in self.update_data.items():
            instance_value = setattr(instance, key, value )
        
        # save the instance
        instance.save()

        # retrieve the instance
        instance_id = instance.id
        instance = None
        instance = self.model.objects.get(id=instance_id)

        # compare instance to expected data
        for key in self.update_expect_data.keys():
            instance_value = getattr(instance, key)
            expected_value = self.update_expect_data[key]
            self.assertEqual(instance_value, expected_value, "Comparing {} attribute".format(key) )



# class PersonSerializerTestCase(TestCase):

#     def setUp(self):
#         self.model              = MODEL
#         self.serializer_class   = SERIALIZER_CLASS
#         self.create_data        = CREATE_DATA
#         self.expect_data        = EXPECT_DATA
#         self.update_data        = UPDATE_DATA
#         self.update_expect_data = UPDATE_EXPECT_DATA

#     def test_serialize(self):
#         instance =self.model(**self.create_data)
#         instance.save()

#         serializer = self.serializer_class(instance)
#         self.assertDictEqual(self.expect_data, serializer.data)

#     def test_create(self):

#         # serializer data is valid
#         serializer = self.serializer_class(data=self.create_data)
#         self.assertTrue(serializer.is_valid(), 'Serializer data is valid')

#         # create an instance via the serializer
#         instance = serializer.create(serializer.validated_data)
#         self.assertTrue(instance, 'Created instance from serializer data')

#         # compare instance to expected data
#         for key in self.expect_data.keys():
#             instance_value = getattr(instance, key)
#             expected_value = self.expect_data[key]
#             self.assertEqual(instance_value, expected_value, "Comparing {} attribute".format(key) )

#     def test_update(self):
#         instance =self.model(**self.create_data)
#         instance.save()

#         serializer = self.serializer_class(data=self.update_data)
#         self.assertTrue(serializer.is_valid(), 'Serializer data is valid')

#         instance = serializer.update(instance, serializer.validated_data)

#         # compare instance to expected data
#         for key, expected_value in self.update_expect_data.items():
#             instance_value = getattr(instance, key)
#             self.assertEqual(instance_value, expected_value, "Comparing {} attribute".format(key) )



class APITestCase(TestCase):

    def setUp(self):
        self.model              = MODEL
        self.serializer_class   = SERIALIZER_CLASS
        self.create_data        = CREATE_DATA
        self.expect_data        = EXPECT_DATA
        self.update_data        = UPDATE_DATA
        self.update_expect_data = UPDATE_EXPECT_DATA

        self.client =  APIClient()
        self.entity = 'person'
        self.api_end_point = '/api/v1/people/'

    # def test_create(self):
    #     response = self.client.post(self.api_end_point, self.create_data)
    #     self.assertEqual(response.status_code, 201, "Created new instance")

    #     # compare response to expected data
    #     for key, expected_value in self.expect_data.items():
    #         instance_value = response.data.get(key)
    #         self.assertEqual(instance_value, expected_value, "Comparing {} attribute".format(key) )

    #     # verify actual database record was created
    #     instance = self.model.objects.get(id=response.data.get('id'))
    #     self.assertTrue(instance)

    # def test_retrieve(self):
    #     response = self.client.post(self.api_end_point, self.create_data)
    #     self.assertEqual(response.status_code, 201, "Created new instance")

    #     instance_id = response.data.get('id')
    #     uri = "{}{}/".format(self.api_end_point,instance_id)
    #     self.assertEqual(response.status_code, 201, "Retrieved")

    #     response = None
    #     response = self.client.get(uri)

    #     # compare response to expected data
    #     for key, expected_value in self.expect_data.items():
    #         instance_value = response.data.get(key)
    #         self.assertEqual(instance_value, expected_value, "Comparing {} attribute".format(key) )

    # def test_update(self):
    #     response = self.client.post(self.api_end_point, self.create_data)
    #     self.assertEqual(response.status_code, 201, "Created new instance")

    #     instance_id = response.data.get('id')
    #     uri = "{}{}/".format(self.api_end_point,instance_id)

    #     response = self.client.patch(uri, json.dumps(self.update_data), content_type='application/json')
    #     self.assertEqual(response.status_code, 200, "Updated instance")

    #     # validate response
    #     for key, expected_value in self.update_expect_data.items():
    #         instance_value = response.data.get(key)
    #         self.assertEqual(instance_value, expected_value, "Comparing {} attribute".format(key) )

    #     # perform get operation and validate
    #     instance_id = response.data.get('id')
    #     uri = "{}{}/".format(self.api_end_point,instance_id)

    #     response = None
    #     response = self.client.get(uri)

    #     # compare response to expected data
    #     for key, expected_value in self.update_expect_data.items():
    #         instance_value = response.data.get(key)
    #         self.assertEqual(instance_value, expected_value, "Comparing {} attribute".format(key) )

    # def test_delete(self):
    #     response = self.client.post(self.api_end_point, self.create_data)
    #     self.assertEqual(response.status_code, 201, "Created new instance")

    #     instance_id = response.data.get('id')
    #     uri = "{}{}/".format(self.api_end_point,instance_id)
    #     print(uri)

    #     response = self.client.delete( uri )    
    #     self.assertEqual(response.status_code, 204, "Deleted")

    #     query = self.model.objects.filter(id=instance_id)
    #     self.assertEqual(len(query),0, "Deleted")


    def test_signals(self):

        scope = {}

        def on_create_before(self,data):
            scope['on_create_before'] = True

        def on_create_success(self,instance):
            scope['on_create_success'] = True

        def on_retrieve_before(self,data):
            scope['on_retrieve_before'] = True

        def on_retrieve_success(self,instance):
            scope['on_retrieve_success'] = True

        def on_update_before(self,data):
            scope['on_update_before'] = True

        def on_update_success(self,instance):
            scope['on_update_success'] = True

        def on_delete_before(self,data):
            scope['on_delete_before'] = True

        def on_delete_success(self,instance):
            scope['on_delete_success'] = True

        on(self.entity + '.create:before',      on_create_before)
        on(self.entity + '.create:success',     on_create_success)
        on(self.entity + '.retrieve:before',    on_retrieve_before)
        on(self.entity + '.retrieve:success',   on_retrieve_success)
        on(self.entity + '.update:before',      on_update_before)
        on(self.entity + '.update:success',     on_update_success)
        on(self.entity + '.delete:before',      on_delete_before)
        on(self.entity + '.delete:success',     on_delete_success)

        # create new record
        response = self.client.post(self.api_end_point, self.create_data)
        self.assertEqual(response.status_code, 201, "Created new instance")

        self.assertTrue(scope['on_create_before'], '.create:before')
        self.assertTrue(scope['on_create_success'], '.create:before')

        # rerieve the record
        instance_id = response.data.get('id')
        uri = "{}{}/".format(self.api_end_point,instance_id)
        self.assertEqual(response.status_code, 201, "Retrieved")

#        self.assertTrue(scope['on_retrieve_before'], '.retrieve:before')
        self.assertTrue(scope['on_retrieve_success'], '.retrieve:before')


        # update a record
        response = self.client.patch(uri, json.dumps(self.update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200, "Updated instance")


        self.assertTrue(scope['on_update_before'], '.update:before')
        self.assertTrue(scope['on_update_success'], '.update:before')

        # delete
        response = self.client.delete( uri )    
        self.assertEqual(response.status_code, 204, "Deleted")

        self.assertTrue(scope['on_delete_before'], '.delete:before')
        self.assertTrue(scope['on_delete_success'], '.delete:before')
       

