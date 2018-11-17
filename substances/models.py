from django.db import models


class SubstanceName(models.Model):
    class Meta:
        verbose_name = 'Nome'
        verbose_name_plural = 'Nomes'

    # Nome do composto químico:
    name = models.CharField(max_length=200,
                            verbose_name='Nome', unique=True)

    def __str__(self):
        return self.name


class Substance(models.Model):
    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'

    # Nome do composto químico:
    name = models.OneToOneField(
        SubstanceName,
        on_delete=models.CASCADE,
        verbose_name='Nome da substância'
    )

    halogen = models.BooleanField(default=False, verbose_name='Halogenado',
                                  name='halogen')
    acetonitrile = models.BooleanField(default=False,
                                       verbose_name='Acetonitrila',
                                       name='acetonitrile')
    heavy_metals = models.BooleanField(default=False,
                                       verbose_name='Metal pesado',
                                       name='heavy_metals')
    sulfur = models.BooleanField(default=False, verbose_name='Sulfurado',
                                 name='sulfur')
    cyanide = models.BooleanField(default=False,
                                  verbose_name='Gerador de cianeto',
                                  name='cyanide')
    amine = models.BooleanField(default=False, verbose_name='Amina',
                                name='amine')
    explosive = models.BooleanField(default=False, verbose_name='Explosivo',
                                    name='explosive')
    flammable = models.BooleanField(default=False, verbose_name='Inflamável',
                                    name='flammable')
    oxidizing = models.BooleanField(default=False, verbose_name='Oxidante',
                                    name='oxidizing')
    under_pressure = models.BooleanField(default=False,
                                         verbose_name='Sob pressão',
                                         name='under_pressure')
    toxic = models.BooleanField(default=False, verbose_name='Tóxico',
                                name='toxic')
    corrosive = models.BooleanField(default=False, verbose_name='Corrosivo',
                                    name='corrosive')
    health_dangerous = models.BooleanField(default=False,
                                           verbose_name='Danoso à saúde',
                                           name='health_dangerous')
    pollutant = models.BooleanField(default=False, verbose_name='Poluente',
                                    name='pollutant')
    cannot_agitate = models.BooleanField(default=False,
                                         verbose_name='Não pode ser agitado',
                                         name='cannot_agitate')

    def __str__(self):
        return str(self.name)


class Properties(models.Model):
    class Meta:
        verbose_name = 'Característica'
        verbose_name_plural = 'Características'

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
    explosive = models.BooleanField(default=False, verbose_name='Explosivo',
                                    name='explosive')
    flammable = models.BooleanField(default=False, verbose_name='Inflamável',
                                    name='flammable')
    oxidizing = models.BooleanField(default=False, verbose_name='Oxidante',
                                    name='oxidizing')
    under_pressure = models.BooleanField(default=False,
                                         verbose_name='Sob pressão',
                                         name='under_pressure')
    toxic = models.BooleanField(default=False, verbose_name='Tóxico',
                                name='toxic')
    corrosive = models.BooleanField(default=False, verbose_name='Corrosivo',
                                    name='corrosive')
    health_dangerous = models.BooleanField(default=False,
                                           verbose_name='Dano à saúde',
                                           name='health_dangerous')
    pollutant = models.BooleanField(default=False, verbose_name='Poluente',
                                    name='pollutant')
    cannot_agitate = models.BooleanField(default=False,
                                         verbose_name='Não pode ser agitado',
                                         name='cannot_agitate')

    @property
    def my_substance_properties(self):
        return self.substance_properties(self)

    @staticmethod
    def substance_properties(self):
        return {
            'halogen': self.halogen,
            'acetonitrile': self.acetonitrile,
            'heavy_metals': self.heavy_metals,
            'sulfur': self.sulfur,
            'cyanide': self.cyanide,
            'amine': self.amine,
            'explosive': self.explosive,
            'flammable': self.flammable,
            'oxidizing': self.oxidizing,
            'under_pressure': self.under_pressure,
            'toxic': self.toxic,
            'corrosive': self.corrosive,
            'health_dangerous': self.health_dangerous,
            'pollutant': self.pollutant,
            'cannot_agitate': self.cannot_agitate
        }

    def my_boolean_to_x(self):
        return self.boolean_to_x(
            substance_properties=self.my_substance_properties
        )

    @staticmethod
    def boolean_to_x(substance_properties):

        property_checks = {name: (lambda x: 'X' if x else ' ')(boolean) for
                           name, boolean in substance_properties.items()}

        return property_checks
