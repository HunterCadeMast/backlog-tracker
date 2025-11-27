from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAccountOwner
from recommendations.models import Recommendations
from recommendations.serializers import RecommendationsSerialiser

class RecommendationsViewSet(viewsets.ModelViewSet):
    serializer_class = RecommendationsSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return Recommendations.objects.filter(user = self.request.user)