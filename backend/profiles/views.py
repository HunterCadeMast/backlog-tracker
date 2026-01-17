from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_api_key.models import APIKey
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from accounts.permissions import APIKeyAuthenticated, APIKeyThrottle
from profiles.models import Profiles, APIKeys
from profiles.serializers import ProfilesSerializer, UsersSerializer, APIKeysSerializer

class ProfilesViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profiles.objects.filter(user = self.request.user)

    @action(detail = False, methods = ['get', 'patch'])
    def personal(self, request):
        profile, _ = Profiles.objects.get_or_create(user = request.user)
        if request.method == 'GET':
            return Response(self.get_serializer(profile, context = {'request': request}).data)
        else:
            serializer = self.get_serializer(profile, data = request.data, context = {'request': request}, partial = True)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)

class UsersViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, username):
        profile = get_object_or_404(Profiles, user__username = username, private_profile = False)
        serializer = UsersSerializer(profile, context = {'request': request})
        return Response(serializer.data)
    
class APIKeysViewSet(viewsets.ModelViewSet):
    serializer_class = APIKeysSerializer
    permission_classes = [APIKeyAuthenticated]
    throttle_classes = [APIKeyThrottle]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return APIKeys.objects.filter(user = self.request.user)
    
    @action(detail = False, methods = ['post'])
    def create_key(self, request):
        if not request.user.emailaddress_set.filter(verified = True).exists():
            return Response({'error', 'Email not verified!'}, status = 403)
        elif APIKeys.objects.filter(user = request.user, expired = False).count() >= 5:
            return Response({'error', 'Too many API keys!'}, status = 403)
        api_key, raw_api_key = APIKey.objects.create_key(name = request.user.username)
        api_key_model = APIKeys.objects.create(user = request.user, api_key_prefix = api_key.prefix)
        return Response({'message': 'API key successfully created!', 'api_key': raw_api_key, 'id': api_key_model.id, 'creation_timestamp': api_key_model.creation_timestamp}, status = 201)
    
    @action(detail = True, methods = ['delete'])
    def delete_key(self, request, pk = None):
        try:
            api_key = APIKey.objects.get(pk = pk, user = request.user)
            APIKey.objects.filter(prefix = api_key.api_key_prefix).delete()
            api_key.expired = True
            api_key.save(update_fields = ['expired'])
            return Response({'message': 'API key successfully deleted!'}, status = 200)
        except APIKey.DoesNotExist:
            return Response({'error': 'API key not found!'}, status = 404)

    @action(detail = True, methods = ['post'])
    def rotate_key(self, request, pk = None):
        try:
            old_api_key = APIKeys.objects.get(pk = pk, user = request.user, expired = False)
        except APIKeys.DoesNotExist:
            return Response({'error': 'API key not found!'}, status = 404)
        if old_api_key.rotate.exists():
            return Response({'error': 'Already rotated key!'}, status = 409)
        api_key, raw_api_key = APIKey.objects.create_key(name = f'rotate-{request.user.username}')
        new_api_key = APIKeys.objects.create(user = request.user, api_key_prefix = api_key.prefix, rotate = old_api_key)
        old_api_key.expiration_date = timezone.now() + timedelta(hours = 24)
        old_api_key.save(update_fields = ['expiration_date'])
        return Response({'message': 'Rotated key!', 'new_api_key': raw_api_key, 'new_api_key_id': new_api_key.id, 'old_key_expiration_date': old_api_key.expiration_date}, status = 201)