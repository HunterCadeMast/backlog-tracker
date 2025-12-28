from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class Home(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        content = {'message', 'Hello World!'}
        return Response(content)