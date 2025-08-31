from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    Requires: email, username, first_name, last_name, password
    Optional: middle_name
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    # Make first_name and last_name required
    first_name = serializers.CharField(
        required=True,
        max_length=30,
        help_text='Required field'
    )
    last_name = serializers.CharField(
        required=True,
        max_length=150,
        help_text='Required field'
    )
    
    # Middle name is optional
    middle_name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=30,
        help_text='Optional middle name'
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'middle_name', 'last_name', 
            'password', 'password_confirm', 'create_time'
        )
        read_only_fields = ('id', 'create_time')

    def validate(self, attrs):
        """
        Validate password confirmation matches password
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Password confirmation does not match password.'
            })
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                'email': 'Email already exists.'
            })
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({
                'username': 'Username already exists.'
            })
        return attrs

    def create(self, validated_data):
        """
        Create user with encrypted password
        """
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """
        Validate user credentials
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Authenticate using email instead of username
            user = authenticate(
                request=self.context.get('request'),
                username=email,  # AbstractUser uses username field for authentication
                password=password
            )
            
            if not user:
                # Try to find user by email and check if they exist
                try:
                    User.objects.get(email=email)
                    raise serializers.ValidationError('Incorrect password.')
                except User.DoesNotExist:
                    raise serializers.ValidationError('User with this email does not exist.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include "email" and "password".')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile operations (read/update)
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)  # Complete name with middle
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'middle_name', 'last_name', 
            'full_name', 'create_time', 'update_time'
        )
        read_only_fields = ('id', 'create_time', 'update_time')

    def update(self, instance, validated_data):
        """
        Update user profile
        """
        # Don't allow email changes through this serializer for security
        validated_data.pop('email', None)
        return super().update(instance, validated_data)


class UserPasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate_old_password(self, value):
        """
        Validate old password is correct
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

    def validate(self, attrs):
        """
        Validate new password confirmation matches new password
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'New password confirmation does not match new password.'
            })
        return attrs

    def save(self, **kwargs):
        """
        Save the new password
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for user list (admin purposes)
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)  # Complete name with middle
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'full_name', 'create_time', 
            'update_time'
        )
        read_only_fields = ('id', 'create_time', 'update_time')
