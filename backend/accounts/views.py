from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.db import transaction
from django.conf import settings
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from profiles.models import Profiles

class RegisterViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        token = token_generator.make_token(user)
        verification_url = f'{settings.FRONTEND_URL}/email/verification/{user.id}/{token}'
        send_mail(subject = 'Verify your Email - Gaming Logjam', message = f'Verify your email using this link:\n{verification_url}', from_email = settings.DEFAULT_FROM_EMAIL, recipient_list = [user.email],)
        return Response({'message': 'Account created!'}, status = 201)

class LoginViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'non_field_errors': ['Email and password are required!']}, status = 400)
        user = authenticate(email = email, password = password)
        if not user:
            return Response({'non_field_errors': ['Invalid email or password!']}, status = 401)
        else:
            refresh_token = RefreshToken.for_user(user)
            return Response({'message': 'User logged in!', 'access': str(refresh_token.access_token), 'refresh': str(refresh_token), 'user': CustomUserSerializer(user).data,}, status = 200)

class LogoutViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception:
                Response({'message': 'Cannot log out!'}, status = 403)
        return Response({'message': 'Logged out!'}, status = 200)

class RefreshViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        old_token = request.data.get('refresh')
        if not old_token:
            return Response({'error', 'Token needed!'}, status = 400)
        else:
            try:
                refresh_token = RefreshToken(old_token)
                access_token = refresh_token.access_token
                new_token = str(old_token)
            except Exception:
                return Response({'error', 'Token invalid!'}, status = 401)
            return Response({'message': 'Token refreshed!', 'access': str(access_token), 'refresh': str(new_token),}, status = 200)
    
class PersonalViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = CustomUserSerializer(request.user, context = {'request': request}, data = request.data, partial = True)
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
            return Response({'current_password': 'Current password is incorrect!'}, status = 400)
        elif new_password != new_password_confirm:
            return Response({'confirm_password': 'Passwords do not match!'}, status = 400)
        else:
            request.user.set_password(new_password)
            request.user.save()
            return Response({'message': 'Password changed!'}, status = 202)
    
class PasswordChangeCompleteViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'message': 'Password changed!', 'status': 'password_changed'}, status = 200)
    
class EmailChangeViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_email = request.data.get('email')
        current_password = request.data.get('current_password')
        user = request.user
        if not new_email or not current_password:
            return Response({'error': 'Need both password and email!'}, status = 400)
        if not user.check_password(current_password):
            return Response({'current_password': 'Incorrect password!'}, status = 400)
        if CustomUser.objects.filter(email = new_email).exclude(id = user.id).exists():
            return Response({'email': 'Already using that email address!'}, status = 400)
        user.email = new_email
        user.is_email_verified = False
        user.save(update_fields = ['email', 'is_email_verified'])
        token = token_generator.make_token(user)
        verification_url = f'{settings.FRONTEND_URL}/email/verification/{user.id}/{token}'
        send_mail(subject = 'Verify your Email - Gaming Logjam', message = f'Verify your email using this link:\n{verification_url}', from_email = settings.DEFAULT_FROM_EMAIL, recipient_list = [user.email],)
        return Response({'message': 'Email updated successfully!'}, status = 200)
    
class PasswordResetViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email required!'}, status = 400)
        user = CustomUser.objects.filter(email = email).first()
        if not user:
            return Response({'error': 'User not found!'}, status = 404)
        token = token_generator.make_token(user)
        password_reset_url = f'{settings.FRONTEND_URL}/password/reset/{user.id}/{token}'
        send_mail(
            subject = 'Reset Password - Gaming Logjam',
            message = f'Reset your password using this link:\n{password_reset_url}',
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [user.email],
        )
        return Response({'message': 'If the email exists, password reset email sent!'}, status = 200)
    

class PasswordResetConfirmationViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, id, token):
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        if not new_password or not new_password_confirm:
            return Response({'error': 'Password fields are required!'}, status = 400)
        if new_password != new_password_confirm:
            return Response({'error': 'New password does not match!'}, status = 400)
        try:
            user = CustomUser.objects.get(id = id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Password reset link invalid!'}, status = 400)
        if not token_generator.check_token(user, token):
            return Response(
                {'error': 'Token invalid or expired!'}, status = 400)
        validate_password(new_password, user)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successfully!'}, status = 200)
    
class EmailVerificationViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, id, token):
        try:
            user = CustomUser.objects.get(id = id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User invalid!'}, status = 400)
        if not token_generator.check_token(user, token):
            return Response({'error': 'Tokens invalid!'}, status = 400)
        if user.is_email_verified:
            return Response({'message': 'Email already verified!'}, status = 200)
        user.is_email_verified = True
        user.save(update_fields = ['is_email_verified'])
        return Response({'message': 'Email verified!'}, status = 200)
    

class AccountDeletionViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        with transaction.atomic():
            RefreshToken.for_user(user).blacklist()
            user.delete()
        return Response({'message': 'Account deleted successfully!',}, status = 204)
    
class OAuthenticationViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        profile = Profiles.objects.get_or_create(user = request.user)
        user_info = CustomUserSerializer(request.user).data
        refresh_token = RefreshToken.for_user(request.user)
        return Response({'message': 'OAuthentication account created successfully!', 'user': user_info, 'profile_id': profile.id, 'providers': list(request.user.socialaccount_set.values_list('provider', flat = True)), 'access': str(refresh_token.access_token), 'refresh': str(refresh_token),}, status = 200,)
    
class UnlinkAccountViewSet(APIView):
    authentication_classes = []
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