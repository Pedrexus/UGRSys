from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

from django.conf import settings


class Department(models.Model):
    department_name = models.CharField(max_length=100, null=True, blank=True,
                                       verbose_name='Nome do Departamento')

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.department_name


class Laboratory(models.Model):
    lab_name = models.CharField(max_length=100, null=True, blank=True,
                                verbose_name='Nome do Laboratório')

    class Meta:
        verbose_name = 'Laboratório'
        verbose_name_plural = 'Laboratórios'

    def __str__(self):
        return self.lab_name


class Waste(models.Model):
    generator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  verbose_name='Gerador')

    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Data de criação')
    last_modified_date = models.DateTimeField(auto_now=True,
                                              verbose_name='Data de modificação')

    amount = models.DecimalField(max_digits=10, decimal_places=3,
                                 verbose_name='Quantidade')
    status = models.BooleanField(verbose_name='Entregue', default=False)

    pH = models.DecimalField(max_digits=2, decimal_places=0, null=True,
                             blank=True, default=Decimal('7'))

    UNITS_CHOICES = (
        ('Kg', 'Kilogramas'),
        ('L', 'Litros')
    )
    unit = models.CharField(max_length=2, choices=UNITS_CHOICES, default='L',
                            verbose_name='unidade')

    # Composição química:
    chemical_makeup = models.CharField(max_length=200,
                                       verbose_name='Composição química')
    # TODO: mudar composição para varios campos

    halogen = models.BooleanField(default=False, verbose_name='Halogenados',
                                  name='halogen')
    acetonitrile = models.BooleanField(default=False,
                                       verbose_name='Acetonitrilas',
                                       name='acetonitrile')
    heavy_metals = models.BooleanField(default=False,
                                       verbose_name='Metais pesados',
                                       name='heavy_metals')
    sulfur = models.BooleanField(default=False, verbose_name='Sulfurados',
                                 name='sulfur')
    cyanide = models.BooleanField(default=False,
                                  verbose_name='Geradores de cianeto',
                                  name='cyanide')
    amine = models.BooleanField(default=False, verbose_name='Aminas',
                                name='amine')

    FEATURES_CHOICES = (
        ('SIM', 'Sim'),
        ('NÃO', 'Não'),
        ('NÃO SEI', 'Não Sei'),
    )

    # TODO: o default deve ser vazio e nao pode ser permitido ficar vazio.
    # TODO: checar informações redundantes
    explosive = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                 default='SIM', verbose_name='Explosivo')
    flammable = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                 default='SIM', verbose_name='Inflamável')
    oxidizing = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                 default='SIM', verbose_name='Oxidante')
    under_pressure = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                      default='SIM',
                                      verbose_name='Sob pressão')
    toxic = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                             default='SIM', verbose_name='Tóxico')
    corrosive = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                 default='SIM', verbose_name='Corrosivo')
    health_dangerous = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                        default='SIM',
                                        verbose_name='Dano à saúde')
    pollutant = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                 default='SIM', verbose_name='Poluente')
    can_agitate = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                   default='SIM', verbose_name='Agitável')

    comments = models.TextField(blank=True, verbose_name='Comentários')

    class Meta:
        verbose_name = 'Resíduo'
        verbose_name_plural = 'Resíduos'

    def __str__(self):
        return ': '.join([self.generator.full_name, self.chemical_makeup])

    def boolean_to_X(self):
        substance_properties = {'halogen': self.halogen,
                                'acetonitrile': self.acetonitrile,
                                'heavy_metals': self.heavy_metals,
                                'sulfur': self.sulfur,
                                'cyanide': self.cyanide,
                                'amine': self.amine}

        property_checks = {name: (lambda x: 'X' if x else ' ')(boolean) for
                         name, boolean in substance_properties.items()}

        return property_checks

    # TODO: adicionar localização no estoque e talvez data de produção.
    def inventory_label(self):
        # abstract
        return 'A1'
