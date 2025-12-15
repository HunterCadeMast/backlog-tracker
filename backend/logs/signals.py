from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from logs.models import Logs, LogSessions

@receiver([post_save, post_delete], sender = LogSessions)
def log_playtime(sender, instance, **kwargs):
    total_time = (instance.log_id.sessions.addregate(total_time = Sum('session_playtime'))['total'] or 0)
    Logs.objects.filter(id = instance.log_id.id).update(user_playtime = total_time)