from django.conf import settings
from django.db import models


class Suggestion(models.Model):
    class Meta:
        verbose_name = 'Sugestão'
        verbose_name_plural = 'sugestões'

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='Usuário')
    comments = models.TextField(verbose_name='Comentários')

    def __str__(self):
        return 'Sugestão ' + str(self.id) + ' de ' + self.user.username
