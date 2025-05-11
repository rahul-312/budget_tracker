from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.

    Handles validation and creation of a new User instance, including password
    strength enforcement.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Password must have at least 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 special character.'
    )

    class Meta:
        model = User
        fields = [
            'email', 'phone_number', 'first_name', 'last_name',
            'gender', 'profile_picture', 'password'
        ]

    def validate_password(self, value):
        """
        Validates that the password meets the required complexity rules.
        """
        password_regex = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$'
        )
        if not password_regex.match(value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and include an uppercase letter, "
                "a lowercase letter, a number, and a special character."
            )
        return value

    def create(self, validated_data):
        """
        Creates and returns a new User instance after setting the hashed password.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for authenticating a user using email and password.

    Returns JWT access and refresh tokens upon successful authentication.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        """
        Validates the user's email and password.

        Ensures the user exists and is active.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid login credentials.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """
        Generates JWT tokens (access and refresh) for the authenticated user.
        """
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
