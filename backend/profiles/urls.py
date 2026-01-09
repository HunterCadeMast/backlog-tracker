from django.urls import path
from profiles.views import UsersViewSet

urlpatterns = [
    path('<username>/', UsersViewSet.as_view()),
]
