"""views for the user API"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer
from user.serializers import AuthTokenSerializer

class CreateUserView(generics.CreateAPIView):
    """create a new user in the system"""
    
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """create an new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES # optional
    
class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    # user the same serialize as before
    serializer_class = UserSerializer
    # to verify user is who we think they are
    authentication_classes = [authentication.TokenAuthentication,]
    # what the user is allowed to do
    permission_classes = [permissions.IsAuthenticated,]

    # overwrite the get object.
    def get_object(self):
        """retrieve and return the auth user"""
        return self.request.user