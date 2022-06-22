"""serializers for the web API view"""

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.forms import PasswordInput
from django.utils.translation import gettext as _

from rest_framework import serializers

# serializers converts objects to and from python objects (or a model in the db)

# we use base clase to create model serializers
class UserSerializer(serializers.ModelSerializer):
    """serializer for the user object"""

    # the model and the fields to be passed to the serializer
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password':{
        'write_only': True, # can't be read 
        'min_length': 5}
        }

        # overwrite the create method. Called after the validation
        def create(self,validated_data):
            """create and return a user with encrypted password"""

            return get_user_model().objects.create_user(**validated_data)

        def udpate(self, instance, validated_data):
            """update and return user"""
            # overwrite the update method

            # validated_data has been gone trough the serializer validation
            password = validated_data.pop('password', None) # retrieve and remove
            
            # existing update method does most of the work. 
            user = super().update(instance, validated_data) 
            
            if password:
                user.set_password(password)
                user.save()

            return user



class AuthTokenSerializer(serializers.Serializer):
    """serializer for the user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,)

    def validate(self, attrs):
        """validate and authenticate the user"""

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('unable to authenticate with provided credentials.')
            # standard way to raise errors with serializers
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

