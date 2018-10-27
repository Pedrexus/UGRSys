from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from labs.validators import phone_regex


class MyUser(AbstractUser):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', default=0)
    full_name = models.CharField(max_length=50)
    #department = models.ForeignKey('labs.Department', on_delete=models.CASCADE)
    #laboratory = models.ForeignKey('labs.Laboratory', on_delete=models.CASCADE)
    email = models.EmailField()
    email_confirmed = models.BooleanField(default=False)
    phone_number = models.CharField(validators=[phone_regex], max_length=17)

    class Meta:
        verbose_name = 'Gerador'
        verbose_name_plural = 'Geradores'

    def __str__(self):
        return self.full_name

"""
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        MyUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
"""
