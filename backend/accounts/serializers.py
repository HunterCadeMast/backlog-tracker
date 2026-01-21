from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    accepted_privacy = serializers.BooleanField(required = True)
    accepted_terms = serializers.BooleanField(required = True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'accepted_privacy', 'accepted_terms', 'accepted_terms_and_privacy_timestamp', 'creation_timestamp']
        read_only_fields = ['id', 'accepted_terms_and_privacy_timestamp', 'creation_timestamp']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if not data.get('accepted_terms') or not data.get('accepted_privacy'):
            raise serializers.ValidationError('You must accept the Terms and Privacy Policy to create an account.')
        return data
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username = value).exists():
            raise serializers.ValidationError("This username is already in use!")
        return value
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email = value).exists():
            raise serializers.ValidationError("This email is already in use!")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.get('username')
        email = validated_data.get('email')
        if CustomUser.objects.filter(username__iexact = username).exists():
            raise serializers.ValidationError({'username': ['This username is already in use!']})
        if CustomUser.objects.filter(email__iexact = email).exists():
            raise serializers.ValidationError({'email': ['This email is already in use!']})
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.accepted_terms_and_privacy_timestamp = timezone.now()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        if password:
            validate_password(password)
            instance.set_password(password)
        if validated_data.get('accepted_terms') and validated_data.get('accepted_privacy'):
            instance.accepted_terms_and_privacy_timestamp = timezone.now()
        instance.save()
        return instance