from django.test import TestCase
from agape import viewsets

from agape.authentication.models import User
from agape.authentication.serializers import UserSerializer


from rest_framework.test import APIRequestFactory

class TestViewSet(viewsets.ModelViewSet):
    """ Viewset that provides CRUD operations for user accounts
    
    Extends:
        viewsets.ModelViewSet

    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    context = 'user'



class ViewSetTestCase(TestCase):

    def setUp(self):
        self.viewset = TestViewSet()
        pass

    def test_sanity(self):
        self.assertTrue(True, "Sane")

    def test_create(self):
        # Using the standard RequestFactory API to create a form POST request
        factory = APIRequestFactory()
        request = factory.post('/notes/', {'title': 'new idea'})
        print(request)
        
        self.viewset.create(request)