from django.db import models


class Evaluation(models.Model):
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    EVALUATION_1 = '1'
    EVALUATION_2 = '2'
    EVALUATION_3 = '3'
    EVALUATION_4 = '4'
    EVALUATION_5 = '5'

    EVALUATION_CHOICES = (
        (EVALUATION_1, 'Péssimo'),
        (EVALUATION_2, 'Ruim'),
        (EVALUATION_3, 'Satisfatório'),
        (EVALUATION_4, 'Bom'),
        (EVALUATION_5, 'Excelente'),
    )

    waste = models.OneToOneField('labs.Waste', on_delete=models.CASCADE,
                                 primary_key=True, verbose_name='Resíduo')

    in_accordance_with_description = models.CharField(
        max_length=15,
        choices=EVALUATION_CHOICES,
        # default=EVALUATION_3,
        verbose_name='De acordo com a descrição'
    )
    flask_conditions = models.CharField(
        max_length=15,
        choices=EVALUATION_CHOICES,
        # default=EVALUATION_3,
        verbose_name='Condições da bomba'
    )
    storage_conditions = models.CharField(
        max_length=15,
        choices=EVALUATION_CHOICES,
        # default=EVALUATION_3,
        verbose_name='Situação da armazenagem'
    )
    tag_conditions = models.CharField(
        max_length=15,
        choices=EVALUATION_CHOICES,
        # default=EVALUATION_3,
        verbose_name='Situação da etiqueta'
    )
    help_from_generator = models.CharField(
        max_length=15,
        choices=EVALUATION_CHOICES,
        # default=EVALUATION_3,
        verbose_name='Atendimento do gerador'
    )
    extra_comments = models.TextField(
        blank=True,
        verbose_name='Comentários Adicionais'
    )

    def __str__(self):
        return self.waste.__str__()