from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAccountOwner
from logs.models import Logs, LogTags
from logs.serializers import LogsSerialiser, LogTagsSerialiser

class LogsViewSet(viewsets.ModelViewSet):
    serializer_class = LogsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return Logs.objects.filter(user = self.request.user)

class LogTagsViewSet(viewsets.ModelViewSet):
    serializer_class = LogTagsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return LogTags.objects.filter(user = self.request.user)