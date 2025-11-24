from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from recommendations.models import Recommendations
from recommendations.serializers import RecommendationsSerialiser

class RecommendationsViewSet(viewsets.ModelViewSet):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationsSerialiser
    permission_classes = [AllowAny]