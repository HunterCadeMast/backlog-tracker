from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_api_key.models import APIKey
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.permissions import IsAccountOwner
from profiles.models import Profiles, APIKeys
from profiles.serializers import ProfilesSerializer, APIKeysSerializer

class ProfilesViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        return Profiles.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    @action(detail = True, methods = ['patch'])
    def update_profile_photo(self, request, pk = None):
        profile = self.get_object()
        profile_photo = request.FILES.get('profile_photo')
        if not profile_photo:
            return Response({'error': 'No profile photo found!'}, status = 400)
        profile.profile_photo = profile_photo
        profile.save()
        return Response({'message': 'Profile photo updated!'})
    
    @action(detail = True, methods = ['patch'])
    def toggle_visibility(self, request, pk = None):
        profile = self.get_object()
        profile.private_profile = not profile.private_profile
        profile.save()
        return Response({'message': 'Profile visibility inverted!'}, status = 200)
    
    @action(detail = True, methods = ['patch'])
    def change_profile_info(self, request, pk = None):
        profile = self.get_object()
        profile_serializer = self.get_serializer(profile, data = request.data, partial = True)
        profile_serializer.is_valid(raise_exception = True)
        profile_serializer.save()
        return Response({'message': 'Updated profile!'}, status = 200)
    
class APIKeysViewSet(viewsets.ModelViewSet):
    serializer_class = APIKeysSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return APIKeys.objects.filter(user = self.request.user)
    
    @action(detail = False, methods = ['post'])
    def create_key(self, request):
        api_key, key = APIKey.objects.create_key(name = request.user.username)
        api_key_model = APIKeys.objects.create(user = request.user, profile_id = request.user.profiles, api_token = api_key.prefix)
        return Response({'message': 'API key successfully created!', 'api_key': key, 'id': api_key_model.id, 'creation_timestamp': api_key_model.creation_timestamp}, status = 201)
    
    @action(detail = True, methods = ['delete'])
    def delete_key(self, request, pk = None):
        try:
            api_key = APIKey.objects.get(pk = pk, user = request.user)
            APIKey.objects.filter(prefix = api_key.api_token).delete()
            api_key.delete()
            return Response({'message': 'API key successfully deleted!'}, status = 200)
        except APIKey.DoesNotExist:
            return Response({'error': 'API key not found!'}, status = 404)
    
    