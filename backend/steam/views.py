from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core import cache
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from urllib.parse import urlencode
from games.models import Games
from steam.models import SteamProfiles
from backend.steam.manual_sync import fetch_steam_player, fetch_steam_games
    
class SteamLinkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail = False, methods = ['get'])
    def link(self, request):
        parameters = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'checkid_setup',
            'openid.return_to': request.build_absolute_uri('/api/steam/callback'),
            'openid.realm': request.build_absolute_uri('/'),
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
        }
        return redirect(f'{settings.STEAM_OPENID_URL}?{urlencode(parameters)}')
    
class SteamUnlinkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail = False, methods = ['post'])
    def unlink(self, request):
        profile = SteamProfiles.objects.get(user = request.user)
        if profile.auto_sync_games or profile.auto_sync_playtime:
            return Response({'error': 'Auto-sync should be disabled before unlinking Steam account!'}, status = 409)
        profile.delete()
        return Response({'message': 'Steam account unlinked!'}, status = 200)

class SteamCallbackViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail = False, methods = ['get'])
    def callback(self, request):
        claimed_id = request.query_params.get('openid.claimed_id')
        if not claimed_id:
            return Response({'error': 'Cannot authenticate Steam!'}, status = 400)
        steam_id = claimed_id.rsplit('/', 1)[-1]
        profile, created = SteamProfiles.objects.get_or_create(steam_id = steam_id, defaults = {'user': request.user})
        if profile.user != request.user and not created:
            return Response({'error': 'Steam account already linked!'}, status = 409)
        data = fetch_steam_player(steam_id)
        profile.steam_username = data['personaname']
        profile.steam_avatar_link = data['avatarfull']
        profile.steam_public_profile = (data['communityvisibilitystate'] == 3)
        profile.last_fetched = timezone.now()
        profile.save()
        return Response({'message': 'Steam account linked!'}, status = 201)
    
class SteamSyncViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail = False, methods = ['post'])
    def sync(self, request):
        profile = SteamProfiles.objects.get(user = request.user)
        key = f'steam_sync:{profile.steam_id}'
        if cache.get(key):
            return Response({'error': 'Too many responses!'}, status = 429)
        owned_games = fetch_steam_games(profile.steam_id)
        for game in owned_games:
            # UPDATE WITH IGDB
            Games.objects.update_or_create()
        profile.last_fetched = timezone.now()
        profile.save()
        cache.set(key, True, timeout = 60)
        return Response({'message': 'Steam account synced!'}, status = 200)