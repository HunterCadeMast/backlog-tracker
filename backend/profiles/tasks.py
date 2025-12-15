from django.utils import timezone
from celery import shared_task
from datetime import timedelta
from profiles.models import APIKeys

@shared_task
def api_key_expiration():
    APIKeys.objects.filter(expired = False, expiration_date__isnull = False, expiration_date__lte = timezone.now()).update(expired = True)

@shared_task
def api_key_rotation():
    expiration_date = timezone.now() - timedelta(days = 90)
    api_keys = APIKeys.objects.filter(expired = False, creation_timestamp__lte = expiration_date)
    for previous_key in api_keys:
        next_key, raw_key = APIKeys.objects.create_key(name = f'auto_rotate_{previous_key.user_id}')
        APIKeys.objects.create(user = previous_key.user, api_key_prefix = next_key.prefix, rotate = previous_key, expiration_date = timezone.now() + timedelta(days = 90))
        previous_key.expiration_date = timezone.now() + timedelta(hours = 24)
        previous_key.save(update_fields = ['expiration_date'])