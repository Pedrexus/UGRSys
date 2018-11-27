from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from labs.validators import phone_regex


class User(AbstractUser):
    pass


class MyUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                verbose_name='Nome de Usuário')
    full_name = models.CharField(max_length=50, verbose_name='Nome completo')
    department = models.ForeignKey('labs.Department', on_delete=models.CASCADE,
                                   verbose_name='Departamento')
    laboratory = models.ForeignKey('labs.Laboratory', on_delete=models.CASCADE,
                                   verbose_name='Laboratório')
    email = models.EmailField(verbose_name='e-mail', unique=True,
                              error_messages={
                                  'unique': _("Esse e-mail já foi registrado. "
                                              "Tente criar a sua conta com "
                                              "outro e-mail.")})
    email_confirmed = models.BooleanField(default=False,
                                          verbose_name='e-mail verificado?')
    phone_number = models.CharField(validators=[phone_regex], max_length=17,
                                    verbose_name='Contato telefônico',
                                    unique=True,
                                    error_messages={
                                        'unique': _(
                                            "Esse número de telefone já foi "
                                            "registrado. Tente criar a sua "
                                            "conta com outro número.")})

    class Meta:
        verbose_name = 'Gerador'
        verbose_name_plural = 'Geradores'

    def __str__(self):
        return self.full_name
