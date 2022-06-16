"""serializers for the web API view"""

from django.contrib.auth import get_user_model

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