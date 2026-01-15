from django.urls import path
from .views import RegisterViewSet, LoginViewSet, LogoutViewSet, RefreshViewSet, PersonalViewSet, PasswordChangeViewSet, EmailChangeViewSet, PasswordResetViewSet, PasswordResetConfirmationViewSet, EmailVerificationViewSet, AccountDeletionViewSet, OAuthenticationViewSet, UnlinkAccountViewSet

urlpatterns = [
    path('register/', RegisterViewSet.as_view(), name = 'register'),
    path('login/', LoginViewSet.as_view(), name = 'login'),
    path('logout/', LogoutViewSet.as_view(), name = 'logout'),
    path('refresh/', RefreshViewSet.as_view(), name = 'refresh'),
    path('profile/', PersonalViewSet.as_view(), name = 'profile'),
    path('password/change/', PasswordChangeViewSet.as_view(), name = 'password_change'),
    path('email/change/', EmailChangeViewSet.as_view(), name = 'email_change'),
    path('password/reset/', PasswordResetViewSet.as_view(), name = 'password_reset'),
    path('password/reset/<uuid:id>/<str:token>/', PasswordResetConfirmationViewSet.as_view(), name = 'password_reset_confirmation'),
    path('email/verification/<uuid:id>/<str:token>/', EmailVerificationViewSet.as_view(), name = 'email_verification'),
    path('delete-account/', AccountDeletionViewSet.as_view(), name = 'delete_account'),
    path('oauthentication/', OAuthenticationViewSet.as_view(), name = 'oauthentication'),
    path('oauthentication/unlinked/', UnlinkAccountViewSet.as_view(), name = 'unlinked_account'),
]