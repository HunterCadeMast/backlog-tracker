from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator as token_generator
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from profiles.models import Profiles

class RegisterViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({'message': 'Account created!', 'user': serializer.data}, status = status.HTTP_201_CREATED)
    
class LoginViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(email = request.data.get('email'), password = request.data.get('password'))
        if not user:
            return Response({'error': 'Invalid credentials!'}, status = 401)
        elif not user.has_usable_password():
            return Response({'error': 'OAuthentication users cannot login with password!'}, status = 403) 
        elif not request.user.emailaddress_set.filter(verified = True).exists():
            return Response({'error', 'Email not verified!'}, status = 403)
        else:
            refresh_token = RefreshToken.for_user(user)
            serializer = CustomUserSerializer(user)
            return Response({'message': 'User logged in!', 'refresh': str(refresh_token), 'access': str(refresh_token.access_token), 'user': serializer.data}, status = 202)
    
class LogoutViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            RefreshToken(refresh_token).blacklist()
            return Response({'message': 'User logged out!'}, status = 202)
        except:
            return Response({'error', 'Token invalid!'}, status = 400)
    
class ProfileViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = CustomUserSerializer(request.user, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
    
class PasswordChangeViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        if not current_password or not new_password or not new_password_confirm:
            return Response({'error': 'All fields need filled out!'}, status = 400)
        elif not request.user.check_password(current_password):
            return Response({'error': 'Current password is incorrect!'}, status = 400)
        elif new_password != new_password_confirm:
            return Response({'error': 'New password does not match!'}, status = 400)
        else:
            request.user.set_password(new_password)
            request.user.save()
            return Response({'message': 'Password changed!'}, status = 202)
    
class PasswordChangeCompleteViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'message': 'Password changed!', 'status': 'password_changed'}, status = 200)
    
class PasswordResetViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email = email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Could not find user!'}, status = 404)
        token = token_generator.make_token(user)
        # Add confirmation email after front-end
        password_reset_url = f"http://127.0.0.1:8000/password/reset/{user.id}/{token}"
        return Response({'message': 'Password reset email sent!', 'password_reset_url': password_reset_url}, status = 200)
    
class PasswordResetCompleteViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'message': 'Password reset link sent!', 'status': 'email_sent'}, status = 200)
    
class PasswordResetConfirmatonViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request, id, token):
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        if new_password != new_password_confirm:
            return Response({'error': 'New password does not match!'}, status = 400)
        else:
            try:
                user = CustomUser.objects.get(id = id)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Password reset link invalid!'}, status = 400)
            if not token_generator.check_token(user, token):
                return Response({'error': 'Token invalid!'})
            else:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset!'}, status = 202)
    
class PasswordResetConfirmationCompleteViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'message': 'Password reset!', 'status': 'password_reset'}, status = 200)
    
class OAuthenticationViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profiles.objects.get(user = request.user)
        user_info = CustomUserSerializer(request.user).data
        return Response({'message': 'OAuthentication account created successfully!', 'refresh_token': str(RefreshToken.for_user(request.user)), 'access_token': str(RefreshToken.for_user(request.user).access_token), 'user': user_info, 'profile_id': profile.id, 'providers': list(request.user.socialaccount_set.values_list('provider', flat = True))}, status = 201)
    
class UnlinkAccountViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        account_provider = request.data.get('provider')
        if not account_provider:
            return Response({'error': 'No account provider!'}, status = 400)
        elif not request.user.has_usable_password() and request.user.socialaccount_set.count() == 1:
            return Response({'error': 'Cannot unlink accounts!'}, status = 400)
        else:
            deleted_account, _ = SocialAccount.objects.filter(user = request.user, provider = account_provider).delete()
            if not deleted_account:
                return Response({'error': 'No linked provider!'}, status = 404)
            else:
                return Response({'message': 'Unlinked accounts successfully!'}, status = 200)  