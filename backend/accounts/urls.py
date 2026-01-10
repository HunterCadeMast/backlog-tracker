from django.urls import path
from .views import RegisterViewSet, LoginViewSet, LogoutViewSet, RefreshViewSet, PersonalViewSet, PasswordChangeViewSet, EmailChangeViewSet, PasswordResetViewSet, PasswordResetConfirmatonViewSet, EmailVerificationViewSet, OAuthenticationViewSet, UnlinkAccountViewSet

urlpatterns = [
    path('register/', RegisterViewSet.as_view(), name = 'register'),
    path('login/', LoginViewSet.as_view(), name = 'login'),
    path('logout/', LogoutViewSet.as_view(), name = 'logout'),
    path('refresh/', RefreshViewSet.as_view(), name = 'refresh'),
    path('profile/', PersonalViewSet.as_view(), name = 'profile'),
    path('password/change/', PasswordChangeViewSet.as_view(), name = 'password_change'),
    path('email/change/', EmailChangeViewSet.as_view(), name = 'email_change'),
    path('password/reset/', PasswordResetViewSet.as_view(), name = 'password_reset'),
    path('password/reset/<int:id>/<str:token>/', PasswordResetConfirmatonViewSet.as_view(), name = 'password_reset_confirmation'),
    path('email/verification/<int:id>/<str:token>/', EmailVerificationViewSet.as_view(), name = 'email_verification'),
    path('oauthentication/completed/', OAuthenticationViewSet.as_view(), name = 'oauthentication_complete'),
    path('oauthentication/unlinked/', UnlinkAccountViewSet.as_view(), name = 'unlinked_account'),
]