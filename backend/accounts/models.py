from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from accounts.managers import CustomUserManager
import uuid

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, null = False, blank = False)
    username = models.CharField(max_length = 35, unique = True, null = True, blank = True)
    email = models.CharField(max_length = 255, unique = True, null = False, blank = False)
    password = models.TextField(null = True, blank = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    creation_timestamp = models.DateTimeField(default = timezone.now, null = False, blank = False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()