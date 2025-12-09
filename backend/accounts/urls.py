from django.urls import path
from .views import RegisterViewSet, LoginViewSet, LogoutViewSet, ProfileViewSet, PasswordChangeViewSet, PasswordChangeCompleteViewSet, PasswordResetViewSet, PasswordResetCompleteViewSet, PasswordResetConfirmatonViewSet, PasswordResetConfirmationCompleteViewSet, OAuthenticationViewSet, UnlinkAccountViewSet

# Include /accounts/[PROVIDER NAME]/login/?process=connect as endpoint in front-end for linking.

urlpatterns = [
    path('register/', RegisterViewSet.as_view(), name = 'register'),
    path('login/', LoginViewSet.as_view(), name = 'login'),
    path('logout/', LogoutViewSet.as_view(), name = 'logout'),
    path('profile/', ProfileViewSet.as_view(), name = 'profile'),
    path('password/change/', PasswordChangeViewSet.as_view(), name = 'password_change'),
    path('password/change/complete/', PasswordChangeCompleteViewSet.as_view(), name = 'password_change_complete'),
    path('password/reset/', PasswordResetViewSet.as_view(), name = 'password_reset'),
    path('password/reset/complete/', PasswordResetCompleteViewSet.as_view(), name = 'password_reset_complete'),
    path('password/reset/confirmation/<uuid:id>/<token>', PasswordResetConfirmatonViewSet.as_view(), name = 'password_reset_confirmation'),
    path('password/reset/confirmation/complete/', PasswordResetConfirmationCompleteViewSet.as_view(), name = 'password_reset_confirmation_complete'),
    path('oauthentication/completed/', OAuthenticationViewSet.as_view(), name = 'oauthentication_complete'),
    path('oauthentication/unlinked/', UnlinkAccountViewSet.as_view(), name = 'unlinked_account'),
]