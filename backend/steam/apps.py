from django.apps import AppConfig

class SteamConfig(AppConfig):
    name = 'steam'

    def auto(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        schedule, _ = IntervalSchedule.objects.get_or_create(every = 1, period = IntervalSchedule.HOURS)
        PeriodicTask.objects.get_or_create(name = 'steam_auto_sync', interval = schedule, task = 'steam.tasks.auto_sync_steam')