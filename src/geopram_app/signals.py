import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=UserProfile)
def create_referral_code(sender, instance, created, **kwargs):
    if created and not instance.referral_code:
        instance.referral_code = f"GP{uuid.uuid4().hex[:8].upper()}"
        instance.save(update_fields=["referral_code"])
