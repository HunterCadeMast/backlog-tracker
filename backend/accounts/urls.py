from django.urls import path
from .views import RegisterViewSet, LoginViewSet, LogoutViewSet, ProfileViewSet, PasswordChangeViewSet, PasswordChangeCompleteViewSet, PasswordResetViewSet, PasswordResetCompleteViewSet, PasswordResetConfirmatonViewSet, PasswordResetConfirmationCompleteViewSet, EmailVerificationViewSet, EmailVerificationConfirmationViewSet

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
    path('email/verification/', EmailVerificationViewSet.as_view(), name = 'email_verification'),
    path('email/verification/confirmation/<uuid:id>/<token>/', EmailVerificationConfirmationViewSet.as_view(), name = 'email_verification_confirmation'),
]