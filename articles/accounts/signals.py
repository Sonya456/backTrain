from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Topic

@receiver(m2m_changed, sender=Topic.subscribers.through)
def delete_topic_if_no_subscribers(sender, instance, action, **kwargs):
    """
    Удаляет тему, если у нее не осталось подписчиков.
    """
    if action == "post_remove" or action == "post_clear":
        if instance.subscribers.count() == 0:
            instance.delete()
