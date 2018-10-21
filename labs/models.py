from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from labs.validators import phone_regex


# O usuário é uma foreign key para acessar a base de resíduos
# TODO: o departamento deve ser uma categoria fixa (foreign key)
class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile', default=0)
    full_name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17)

    class Meta:
        verbose_name = 'Gerador'
        verbose_name_plural = 'Geradores'

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        MyUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Waste(models.Model):
    generator = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    amount = models.DecimalField(max_digits=10, decimal_places=3, null=True,
                                 blank=True)

    UNITS_CHOICES = (
        ('Kg', 'Kilogramas'),
        ('L', 'Litros')
    )
    unit = models.CharField(max_length=2, choices=UNITS_CHOICES, default='L')

    # Composição química:
    chemical_makeup = models.CharField(max_length=200)

    # TODO: adicionar localização no estoque e talvez data de produção.

    FEATURES_CHOICES = (
        ('SIM', 'Sim'),
        ('NÃO', 'Não'),
        ('NÃO SEI', 'Não Sei'),
    )

    # TODO: o default deve ser vazio e nao pode ser permitido ficar vazio.
    explosive = models.CharField(max_length=7, choices=FEATURES_CHOICES, default='SIM')
    flammable = models.CharField(max_length=7, choices=FEATURES_CHOICES, default='SIM')
    oxidizing = models.CharField(max_length=7, choices=FEATURES_CHOICES, default='SIM')
    under_pressure = models.CharField(max_length=7, choices=FEATURES_CHOICES, default='SIM')
    toxic = models.CharField(max_length=7, choices=FEATURES_CHOICES, default='SIM')
    corrosive = models.CharField(max_length=7, choices=FEATURES_CHOICES, default='SIM')
    health_dangerous = models.CharField(max_length=7, choices=FEATURES_CHOICES, default='SIM')
    pollutant = models.CharField(max_length=7, choices=FEATURES_CHOICES, default='SIM')
    can_agitate = models.CharField(max_length=7, choices=FEATURES_CHOICES, default='SIM')

    comments = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Resíduo'
        verbose_name_plural = 'Resíduos'

    def __str__(self):
        return ': '.join([self.generator.full_name, self.chemical_makeup])
