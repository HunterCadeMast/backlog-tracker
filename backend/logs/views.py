from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from logs.models import Logs, LogTags
from logs.serializers import LogsSerialiser, LogTagsSerialiser

class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsSerialiser
    permission_classes = [AllowAny]

class LogTagsViewSet(viewsets.ModelViewSet):
    queryset = LogTags.objects.all()
    serializer_class = LogTagsSerialiser
    permission_classes = [AllowAny]