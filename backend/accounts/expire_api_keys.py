from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from profiles.models import APIKeys

class Expire(BaseCommand):
    help = 'Expire API keys.'

    def handle(self, *args, **kwargs):
        expiration_date = timezone.now() - timedelta(days = 90)
        expired = APIKeys.objects.filter(last_fetched__lt = expiration_date, expired = False).update(expired = True)
        self.stdout.write(
            self.style.SUCCESS(f'API Keys Expired: {expired}!')
        )