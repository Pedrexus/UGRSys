from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

from django.conf import settings


class Department(models.Model):
    department_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.department_name


class Laboratory(models.Model):
    lab_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Laboratório'
        verbose_name_plural = 'Laboratórios'

    def __str__(self):
        return self.lab_name


class Waste(models.Model):
    status = 'user_inventory'
    generator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    amount = models.DecimalField(max_digits=10, decimal_places=3, null=True,
                                 blank=True)

    pH = models.DecimalField(max_digits=2, decimal_places=0, null=True,
                             blank=True, default=Decimal('7'))

    UNITS_CHOICES = (
        ('Kg', 'Kilogramas'),
        ('L', 'Litros')
    )
    unit = models.CharField(max_length=2, choices=UNITS_CHOICES, default='L')

    # Composição química:
    chemical_makeup = models.CharField(max_length=200)
    # TODO: mudar composição para varios campos

    halogen = models.BooleanField(default=False)
    acetonitrile = models.BooleanField(default=False)
    heavy_metals = models.BooleanField(default=False)
    sulfur = models.BooleanField(default=False)
    cyanide = models.BooleanField(default=False)
    amine = models.BooleanField(default=False)

    FEATURES_CHOICES = (
        ('SIM', 'Sim'),
        ('NÃO', 'Não'),
        ('NÃO SEI', 'Não Sei'),
    )

    # TODO: o default deve ser vazio e nao pode ser permitido ficar vazio.
    # TODO: checar informações redundantes
    explosive = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                 default='SIM')
    flammable = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                 default='SIM')
    oxidizing = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                 default='SIM')
    under_pressure = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                      default='SIM')
    toxic = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                             default='SIM')
    corrosive = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                 default='SIM')
    health_dangerous = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                        default='SIM')
    pollutant = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                 default='SIM')
    can_agitate = models.CharField(max_length=7, choices=FEATURES_CHOICES,
                                   default='SIM')

    comments = models.TextField(blank=True)

    def boolean_to_X(self):
        if self.halogen:
            self.halogen_check = 'X'
        else:
            self.halogen_check = ' '

        if self.acetonitrile:
            self.acetonitrile_check = 'X'
        else:
            self.acetonitrile_check = ' '

        if self.heavy_metals:
            self.heavy_metals_check = 'X'
        else:
            self.heavy_metals_check = ' '

        if self.sulfur:
            self.sulfur_check = 'X'
        else:
            self.sulfur_check = ' '

        if self.cyanide:
            self.cyanide_check = 'X'
        else:
            self.cyanide_check = ' '

        if self.amine:
            self.amine_check = 'X'
        else:
            self.amine_check = ' '

    # TODO: adicionar localização no estoque e talvez data de produção.
    # abstract
    def inventory_label(self):
        return 'A1'

    class Meta:
        verbose_name = 'Resíduo'
        verbose_name_plural = 'Resíduos'

    def __str__(self):
        return ': '.join([self.generator.full_name, self.chemical_makeup])
