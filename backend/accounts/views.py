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
        elif not user.emailaddress_set.filter(verified = True).exists():
            return Response({'error', 'Email not verified!'}, status = 403)
        else:
            refresh_token = RefreshToken.for_user(user)
            response = Response({'message': 'User logged in!'}, status = 202)
            response.set_cookie(key = "access", value = str(refresh_token.access_token), httponly = True, secure = True, samesite = 'Lax', max_age = 60 * 15)
            response.set_cookie(key = "refresh", value = str(refresh_token), httponly = True, secure = True, samesite = 'Lax', max_age = 60 * 60 * 24 * 7)
            return response
    
class LogoutViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh")
            if refresh_token:
                RefreshToken(refresh_token).blacklist()
            response = Response({'message': 'User logged out!'}, status = 200)
            response.delete_cookie('access')
            response.delete_cookie('refresh')
            return response
        except:
            return Response({'error', 'Token invalid!'}, status = 400)
        
class RefreshViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response({'error', 'Token invalid!'}, status = 401)
        else:
            access_token = RefreshToken(refresh_token).access_token
            if not access_token:
                return Response({'error', 'Token invalid!'}, status = 401)
            response = Response({'message': 'Token refreshed!'}, status = 200)
            response.set_cookie(key = "access", value = str(access_token), httponly = True, secure = True, samesite = 'Lax', max_age = 60 * 15)
            return response
    
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
        refresh_token = RefreshToken.for_user(request.user)
        response = Response({'message': 'OAuthentication account created successfully!', 'user': user_info, 'profile_id': profile.id, 'providers': list(request.user.socialaccount_set.values_list('provider', flat = True))}, status = 202)
        response.set_cookie(key = "access", value = str(refresh_token.access_token), httponly = True, secure = True, samesite = 'Lax', max_age = 60 * 15)
        response.set_cookie(key = "refresh", value = str(refresh_token), httponly = True, secure = True, samesite = 'Lax', max_age = 60 * 60 * 24 * 7)
        return response
    
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