from django.urls import path
from profiles.views import UsersViewSet

urlpatterns = [
    path('user/<str:username>/', UsersViewSet.as_view(), name = 'user_profile'),
]