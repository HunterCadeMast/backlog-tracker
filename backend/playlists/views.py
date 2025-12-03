from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import F, Count
from accounts.permissions import IsAccountOwner
from playlists.models import Playlists, PlaylistLogs
from playlists.serializers import PlaylistsSerialiser, PlaylistLogsSerialiser
from logs.models import Logs

class PlaylistsViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        playlists = Playlists.objects.filter(user = self.request.user)
        if title := self.request.query_params.get('playlist_search'):
            playlists = playlists.filter(playlist_title__icontains = title)
        sort_decision = self.request.query_params.get('sort_playlist')
        if sort_decision == 'title_ascending':
            playlists = playlists.order_by('playlist_title')
        elif sort_decision == 'title_descending':
            playlists = playlists.order_by('-playlist_title')
        elif sort_decision == 'recent_ascending':
            playlists = playlists.order_by('updated_timestamp')
        elif sort_decision == 'recent_descending':
            playlists = playlists.order_by('-updated_timestamp')
        elif sort_decision == 'count_ascending':
            playlists = playlists.annotate(log_count = Count('playlistlogs')).order_by('log_count')
        elif sort_decision == 'count_descending':
            playlists = playlists.annotate(log_count = Count('playlistlogs')).order_by('-log_count')
        return playlists
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    @action(detail = True, methods = ['patch'])
    def rename(self, request, pk = None):
        current_playlist = self.get_object()
        new_playlist_title = request.data.get('playlist_title')
        if not new_playlist_title:
            return Response({'error': 'Playlist title needed!'}, status = 400)
        current_playlist.playlist_title = new_playlist_title
        current_playlist.update_time()
        current_playlist.save()
        return Response({'message': 'Edited title!'}, status = 200)

class PlaylistLogsViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistLogsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        playlist_logs = PlaylistLogs.objects.filter(user = self.request.user)
        if games := self.request.query_params.get('games'):
            playlist_logs = playlist_logs.filter(log_id__game_id__game_title__icontains = games)
        if developers := self.request.query_params.get('developers'):
            playlist_logs = playlist_logs.filter(log_id__game_id__gamespecificdevelopers__developer_id__label__icontains = developers).distinct()
        if publishers := self.request.query_params.get('publishers'):
            playlist_logs = playlist_logs.filter(log_id__game_id__gamespecificpublishers__publisher_id__label__icontains = publishers).distinct()
        if genres := self.request.query_params.get('genres'):
            playlist_logs = playlist_logs.filter(log_id__game_id__gamespecificgenres__genre_id__label__icontains = genres).distinct()
        if platforms := self.request.query_params.get('platforms'):
            playlist_logs = playlist_logs.filter(log_id__game_id__gamespecificplatforms__platform_id__label__icontains = platforms).distinct()
        if franchises := self.request.query_params.get('franchises'):
            playlist_logs = playlist_logs.filter(log_id__game_id__gamespecificfranchises__franchise_id__label__icontains = franchises).distinct()
        if series := self.request.query_params.get('series'):
            playlist_logs = playlist_logs.filter(log_id__game_id__gamespecificseries__series_id__label__icontains = series).distinct()
        if tag := self.request.query_params.get('log_tag'):
            playlist_logs = playlist_logs.filter(log_id__logtags__log_tag__icontains = tag).distinct()
        if tags := self.request.query_params.getlist('log_tags'):
            for tag in tags:
                playlist_logs = playlist_logs.filter(log_id__logtags__log_tag__icontains = tag)
            playlist_logs = playlist_logs.distinct()
        status_order = ['completed', 'playing', 'paused', 'backlog', 'dropped']
        sort_decision = self.request.query_params.get('sort_playlist_logs')
        if sort_decision == 'rating_ascending':
            playlist_logs = playlist_logs.order_by('log_id__user_rating')
        elif sort_decision == 'rating_descending':
            playlist_logs = playlist_logs.order_by('-log_id__user_rating')
        elif sort_decision == 'playtime_ascending':
            playlist_logs = playlist_logs.order_by('log_id__user_playtime')
        elif sort_decision == 'playtime_descending':
            playlist_logs = playlist_logs.order_by('-log_id__user_playtime')
        elif sort_decision == 'status_ascending':
            playlist_logs = list(playlist_logs)
            playlist_logs = sorted(playlist_logs, key = lambda x: status_order.index(x.log_id.user_status))
        elif sort_decision == 'status_descending':
            playlist_logs = list(playlist_logs)
            playlist_logs = sorted(playlist_logs, key = lambda x: status_order.index(x.log_id.user_status), reverse = True)
        elif sort_decision == 'position':
            playlist_logs = playlist_logs.order_by('current_position')
        return playlist_logs
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    @action(detail = True, methods = ['patch'])
    def reorder(self, request, pk = None):
        current_playlist = Playlists.objects.get(id = pk, user = request.user)
        # Log Order will be added with front-end.
        current_order = request.data.get('log_order')
        if not current_order or not isinstance(current_order, list):
            return Response({'error': 'Need list of ordered logs!'}, status = 400)
        for index, log_id in enumerate(current_order):
            PlaylistLogs.objects.filter(playlist_id = current_playlist, log_id = log_id).update(current_position = index)
        current_playlist.update_time()
        return Response({'message': 'Reordered log!'}, status = 200)
    
    @action(detail = True, methods = ['post'])
    def add(self, request, pk = None):
        try:
            current_playlist = Playlists.objects.get(id = pk, user = request.user)
        except Playlists.DoesNotExist:
            return Response({'error': 'Playlist not found!'}, status = 404)
        log_id = request.data.get('log_id')
        try:
            log = Logs.objects.get(id = log_id, user = request.user)
        except Logs.DoesNotExist:
            return Response({'error': 'Log not found!'}, status = 404)
        logs = PlaylistLogs.objects.filter(playlist_id = current_playlist).order_by('current_position')
        # Log Position will be added with front-end.
        new_position = int(request.data.get('log_position', -1))
        if new_position is None:
            new_position = -1
        if new_position < 0 or new_position > logs.count():
            new_position = logs.count()
        logs.filter(current_position__gte = new_position).update(current_position = F('current_position') + 1)
        PlaylistLogs.objects.create(user = request.user, playlist_id = current_playlist, log_id = log, current_position = new_position)
        current_playlist.update_time()
        return Response({'message': 'Added log!'}, status = 201)
    
    @action(detail = True, methods = ['delete'])
    def remove(self, request, pk = None):
        try:
            current_playlist = Playlists.objects.get(id = pk, user = request.user)
        except Playlists.DoesNotExist:
            return Response({'error': 'Playlist not found!'}, status = 404)
        log_id = request.data.get('log_id')
        try:
            log = PlaylistLogs.objects.get(playlist_id = current_playlist, log_id = log_id)
        except PlaylistLogs.DoesNotExist:
            return Response({'error': 'Log not found!'}, status = 404)
        previous_position = log.current_position
        log.delete()
        PlaylistLogs.objects.filter(playlist_id = current_playlist, current_position__gt = previous_position).update(current_position = F('current_position') - 1)
        current_playlist.update_time()
        return Response({'message': 'Removed log!'}, status = 201)