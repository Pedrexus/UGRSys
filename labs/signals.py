from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from registration.models import MyUser


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        MyUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()