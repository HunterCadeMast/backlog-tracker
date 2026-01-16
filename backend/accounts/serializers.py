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

    def create(self, validated_data):
        password = validated_data.pop('password')
        accepted_terms = validated_data.pop('accepted_terms')
        accepted_privacy = validated_data.pop('accepted_privacy')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.accepted_terms = accepted_terms
        user.accepted_privacy = accepted_privacy
        if not accepted_terms or not accepted_privacy:
            raise serializers.ValidationError('You must accept the Terms and Privacy Policy to create an account!')
        if accepted_terms and accepted_privacy:
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