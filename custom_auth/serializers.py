from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    # Hide password from response and make it write-only
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """
        Create and save a new user instance with a hashed password.
        """
        user = self.Meta.model(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
