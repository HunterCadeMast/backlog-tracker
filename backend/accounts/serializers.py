from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'creation_timestamp']
        read_only_fields = ['id', 'creation_timestamp']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        validate_password(password)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        if password is not None:
            validate_password(password)
            instance.set_password(password)
        instance.save()
        return instance