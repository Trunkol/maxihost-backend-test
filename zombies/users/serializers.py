from users.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        """
            Create and return a new `User` instance, given the validated data.
        """
        username = validated_data.get('username', None)
        password = validated_data.get('password', None)
        email = validated_data.get('email', None)

        user = User.objects.create_user(username, email, password)
        #Token.objects.create(user=user)

        return user
