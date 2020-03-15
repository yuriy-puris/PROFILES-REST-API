from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

class TestApiView(APIView):

  serializer_class = serializers.TestSerializer

  def get(self, request, format=None):
    return Response({'message': 'Test message'})

  def post(self, request):
    serializer = self.serializer_class(data=request.data)

    if serializer.is_valid():
      name = serializer.validated_data.get('name')
      message = f'Hello {name}!'
      return Response({'message': message})
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk=None):
    return Response({'method': 'PUT'})

  def patch(self, request, pk=None):
    return Response({'method': 'PATCH'})

  def delete(self, request, pk=None):
    return Response({'method': 'DELETE'})


class TestViewSet(viewsets.ViewSet):

    serializer_class = serializers.TestSerializer

    def list(self, request):
      viewset = [ 'TEST1', 'TEST2', 'TEST3' ]
      return Response({"message": 'Test view set', 'viewset': viewset})


    def create(self, request):
      serializer = self.serializer_class(data=request.data)

      if serializer.is_valid():
        name = serializer.validated_data.get('name')
        return Response({'message': f'create message by {name}'})
      else:
        return Response(
          serializer.errors,
          status=status.HTTP_400_BAD_REQUEST
        )


    def retrieve(self, request, pk=None):
      """get object by id"""
      return Response({'message': 'HTTP method - GET'})


    def update(self, request, pk=None):
      """handle updating an object"""
      return Response({'message': 'HTTP method - PUT'})


    def partial_update(self, request, pk=None):
      """handle updating part of an object"""
      return Response({'message': 'HTTP method - PATCH'})


    def destroy(self, request, pk=None):
      """handle removing an object"""
      return Response({'message': 'HTTP method - DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
  serializer_class = serializers.UserProfileSerializer
  queryset = models.UserProfile.objects.all()
  authentication_classes = (TokenAuthentication,)
  permission_classes = (permissions.UpdateOwnProfile,)
  filter_backends = (filters.SearchFilter,)
  search_fields = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
  renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

 
class UserProfileFeedItemViewSet(viewsets.ModelViewSet):
  authentication_classes = (TokenAuthentication,)
  serializer_class = serializers.ProfileFeedItemSerializer
  queryset = models.ProfileFeedItem.objects.all()
  permission_classes = (
    permissions.UpdateOwnStatus,
    IsAuthenticated
  )

  def perform_create(self, serializer):
    serializer.save(user_profile=self.request.user)