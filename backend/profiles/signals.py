from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from profiles.models import Profiles

@receiver(post_save, sender = get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(user = instance)