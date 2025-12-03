from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.permissions import IsAccountOwner
from logs.models import Logs, LogTags
from logs.serializers import LogsSerialiser, LogTagsSerialiser

class LogsViewSet(viewsets.ModelViewSet):
    serializer_class = LogsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        user_logs = Logs.objects.filter(user = self.request.user)
        if games := self.request.query_params.get('games'):
            user_logs = user_logs.filter(game_id__game_title__icontains = games)
        if developers := self.request.query_params.get('developers'):
            user_logs = user_logs.filter(game_id__gamespecificdevelopers__developer_id__label__icontains = developers).distinct()
        if publishers := self.request.query_params.get('publishers'):
            user_logs = user_logs.filter(game_id__gamespecificpublishers__publisher_id__label__icontains = publishers).distinct()
        if genres := self.request.query_params.get('genres'):
            user_logs = user_logs.filter(game_id__gamespecificgenres__genre_id__label__icontains = genres).distinct()
        if platforms := self.request.query_params.get('platforms'):
            user_logs = user_logs.filter(game_id__gamespecificplatforms__platform_id__label__icontains = platforms).distinct()
        if franchises := self.request.query_params.get('franchises'):
            user_logs = user_logs.filter(game_id__gamespecificfranchises__franchise_id__label__icontains = franchises).distinct()
        if series := self.request.query_params.get('series'):
            user_logs = user_logs.filter(game_id__gamespecificseries__series_id__label__icontains = series).distinct()
        if tag := self.request.query_params.get('log_tag'):
            user_logs = user_logs.filter(logtags__log_tag__icontains = tag).distinct()
        if tags := self.request.query_params.getlist('log_tags'):
            for tag in tags:
                user_logs = user_logs.filter(logtags__log_tag__icontains = tag)
            user_logs = user_logs.distinct()
        status_order = ['completed', 'playing', 'paused', 'backlog', 'dropped']
        sort_decision = self.request.query_params.get('sort_user_logs')
        if sort_decision == 'rating_ascending':
            user_logs = user_logs.order_by('user_rating')
        elif sort_decision == 'rating_descending':
            user_logs = user_logs.order_by('-user_rating')
        elif sort_decision == 'playtime_ascending':
            user_logs = user_logs.order_by('user_playtime')
        elif sort_decision == 'playtime_descending':
            user_logs = user_logs.order_by('-user_playtime')
        elif sort_decision == 'status_ascending':
            user_logs = list(user_logs)
            user_logs = sorted(user_logs, key = lambda x: status_order.index(x.user_status))
        elif sort_decision == 'status_descending':
            user_logs = list(user_logs)
            user_logs = sorted(user_logs, key = lambda x: status_order.index(x.user_status), reverse = True)
        return user_logs
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
class LogTagsViewSet(viewsets.ModelViewSet):
    serializer_class = LogTagsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        return LogTags.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user, profile_id = self.request.user.profiles)

    @action(detail = True, methods = ['patch'])
    def rename(self, request, pk = None):
        current_tag = self.get_object()
        new_tag = request.data.get('tag')
        if not new_tag:
            return Response({'error': 'Tag needed!'}, status = 400)
        current_tag.log_tag = new_tag
        current_tag.save()
        return Response({'message': 'Edited tag!'}, status = 200)
    
    @action(detail = True, methods = ['post'])
    def add(self, request,  pk = None):
        current_tag = self.get_object()
        log_id = request.data.get('log_id')
        try:
            log = Logs.objects.get(id = log_id, user = request.user)
        except Logs.DoesNotExist:
            return Response({'error': 'Log not found!'}, status = 404)
        current_tag.log_id = log
        current_tag.save()
        return Response({'message': 'Added tag!'}, status = 200)
    
    @action(detail = True, methods = ['delete'])
    def remove(self, request,  pk = None):
        current_tag = self.get_object()
        current_tag.log_id = None
        current_tag.save()
        return Response({'message': 'Removed tag!'}, status = 200)