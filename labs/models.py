from decimal import Decimal

from django.conf import settings
from django.db import models

from labs.functions import p2f
from labs.validators import percentages_regex
from registration.models import MyUser
from substances.models import SubstanceName, Properties


class Department(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True,
                            verbose_name='Nome do Departamento', unique=True)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.name


class Laboratory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True,
                            verbose_name='Nome do Laboratório', unique=True)

    class Meta:
        verbose_name = 'Laboratório'
        verbose_name_plural = 'Laboratórios'

    def __str__(self):
        return self.name


class Waste(models.Model):
    class Meta:
        verbose_name = 'Resíduo'
        verbose_name_plural = 'Resíduos'

    generator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  verbose_name='Gerador')
    # Composição química do banco de dados:
    chemical_makeup = models.ManyToManyField('substances.SubstanceName',
                                             verbose_name='Composição química',
                                             blank=True)
    chemical_makeup_pct = models.CharField(max_length=300,
                                           verbose_name='Concentrações',
                                           validators=[percentages_regex],
                                           default='0%')

    # Composição química exclusiva:
    chemical_makeup_text = models.CharField(max_length=200,
                                            verbose_name='Composição química extra',
                                            default='', blank=True)
    chemical_makeup_text_pct = models.CharField(max_length=300,
                                                verbose_name='Concentrações',
                                                validators=[percentages_regex],
                                                default='0%')
    STATUS_1 = 'User inventory'
    STATUS_2 = 'Waiting removal'
    STATUS_3 = 'DeGR inventory'
    STATUS_4 = 'Neutralized'
    STATUS_BOOKMARK = 'Bookmarked'

    STATUS_CHOICES = (
        (STATUS_1, 'Com usuário'),
        (STATUS_2, 'Aguardando retirada'),
        (STATUS_3, 'Inventório DeGR'),
        (STATUS_4, 'Neutralizado'),
        (STATUS_BOOKMARK, 'Favorito'),
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,
                              default=STATUS_1, verbose_name='Status')

    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Data de criação')
    last_modified_date = models.DateTimeField(auto_now=True,
                                              verbose_name='Data de modificação')

    amount = models.DecimalField(max_digits=10, decimal_places=3,
                                 verbose_name='Quantidade')

    UNITS_CHOICES = (
        ('Kg', 'Kilogramas'),
        ('L', 'Litros')
    )
    unit = models.CharField(max_length=2, choices=UNITS_CHOICES, default='L',
                            verbose_name='unidade')

    pH = models.DecimalField(max_digits=2, decimal_places=0, null=True,
                             blank=True, default=Decimal('7'))

    # TODO: tamanho da embalagem

    STATE = (
        ('L', 'Líquido'),
        ('S', 'Sólido')
    )

    is_liquid = models.CharField(max_length=7, choices=STATE, default='L',
                                 verbose_name='Estado do resíduo:')

    SOLVENT = (
        ('A', 'Solução Aquosa'),
        ('O', 'Solvente Orgânico')
    )

    solvent_type = models.CharField(max_length=7, choices=SOLVENT, default='A',
                                    verbose_name='Solvente principal',
                                    name='solvent_type')

    halogen = models.NullBooleanField(default=False,
                                      verbose_name='Halogenados',
                                      name='halogen')
    acetonitrile = models.NullBooleanField(default=False,
                                           verbose_name='Acetonitrilas',
                                           name='acetonitrile')
    heavy_metals = models.NullBooleanField(default=False,
                                           verbose_name='Metais pesados',
                                           name='heavy_metals')
    sulfur = models.NullBooleanField(default=False, verbose_name='Sulfurados',
                                     name='sulfur')
    cyanide = models.NullBooleanField(default=False,
                                      verbose_name='Geradores de cianeto',
                                      name='cyanide')
    amine = models.NullBooleanField(default=False, verbose_name='Aminas',
                                    name='amine')
    explosive = models.NullBooleanField(default=False,
                                        verbose_name='Explosivo',
                                        name='explosive')
    flammable = models.NullBooleanField(default=False,
                                        verbose_name='Inflamável',
                                        name='flammable')
    oxidizing = models.NullBooleanField(default=False, verbose_name='Oxidante',
                                        name='oxidizing')
    under_pressure = models.NullBooleanField(default=False,
                                             verbose_name='Sob pressão',
                                             name='under_pressure')
    toxic = models.NullBooleanField(default=False, verbose_name='Tóxico',
                                    name='toxic')
    corrosive = models.NullBooleanField(default=False,
                                        verbose_name='Corrosivo',
                                        name='corrosive')
    health_dangerous = models.NullBooleanField(default=False,
                                               verbose_name='Dano à saúde',
                                               name='health_dangerous')
    pollutant = models.NullBooleanField(default=False, verbose_name='Poluente',
                                        name='pollutant')
    cannot_agitate = models.NullBooleanField(default=False,
                                             verbose_name='Não pode ser agitado',
                                             name='cannot_agitate')

    comments = models.TextField(blank=True, verbose_name='Comentários')

    @property
    def chemical_makeup_names(self):
        main_substances = [substance.name for substance in self.chemical_makeup.all()]
        main_pct = ['(' + pct.strip() + ')' for pct in self.chemical_makeup_pct.split(',')]
        main_names = ', '.join([' '.join(tpl) for tpl in zip(main_substances, main_pct)])

        extra_substances = self.chemical_makeup_text.split(',') if self.chemical_makeup_text else []
        extra_pct = ['(' + pct.strip() + ')' for pct in self.chemical_makeup_text_pct.split(',')]
        extra_names = ', '.join(
            [' '.join(tpl) for tpl in zip(extra_substances, extra_pct)]
        )

        possible_comma = ', ' if main_names and extra_names else ''
        return main_names + possible_comma + extra_names

    chemical_makeup_names.fget.short_description = 'Composição Química'

    @property
    def chemical_percentages(self):
        substances = self.chemical_makeup_names.split(',')
        return {s[:s.find('(')].strip(): s[s.find("(") + 1:s.find(")")] for s
                in substances}

    @property
    def substances_amounts(self):
        amount = float(self.amount)
        return {name: amount*p2f(pctg) for name, pctg in self.chemical_percentages.items()}

    @property
    def substance_properties(self):
        return Properties.substance_properties(self)

    def boolean_to_x(self):
        return Properties.boolean_to_x(
            substance_properties=self.substance_properties
        )

    def __str__(self):
        return ': '.join(
            [MyUser.objects.get(user=self.generator).full_name,
             self.chemical_makeup_names])

    def inventory_label(self):
        s = ''

        if self.is_liquid == 'S':
            s += '1'
        elif self.is_liquid == 'L':
            s += '2'

            if self.solvent_type == 'O':
                s += '.1'
                if self.cyanide:
                    s += '.1'
                elif self.halogen:
                    s += '.2'
                elif self.toxic:
                    s += '.3'
                else:
                    s += '.0'

            elif self.solvent_type == 'A':
                s += '.2'
                if self.toxic:
                    s += '.1'
                else:
                    s += '.0'

                if self.pH == 7:
                    s += '.7'
                elif self.pH < 7:
                    s += '.6'
                elif self.pH > 7:
                    s += '.8'

            else:
                s += '.0'

        else:
            s += '0'

        return s
