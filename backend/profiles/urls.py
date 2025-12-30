from django.urls import path
from profiles.views import UsersViewSet

urlpatterns = [
    path('users/<username>/', UsersViewSet.as_view()),
]
