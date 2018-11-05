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
    status_list = ['user_inventory','waiting_removal','degr_inventory','neutralized']
    status = status_list[0]
    user_editable = True

    generator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  verbose_name='Gerador')

    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Data de criação')
    last_modified_date = models.DateTimeField(auto_now=True,
                                              verbose_name='Data de modificação')

    amount = models.DecimalField(max_digits=10, decimal_places=3,
                                 verbose_name='Quantidade')

    #TODO: existem mais status: inventorio_usuario, pedido pra recolher, recolhido, inventorio degr, processado

    pH = models.DecimalField(max_digits=2, decimal_places=0, null=True,
                             blank=True, default=Decimal('7'))
    #TODO: tamanho da embalagem
    #TODO: realmente vale a pena ter as duas unidades?
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

    # deprecated?: o default deve ser vazio e nao pode ser permitido ficar vazio.
    # deprecated?: checar informações redundantes
    STATE = (
        ('L','Líquido'),
        ('S','Sólido')
    )

    is_liquid = models.CharField(max_length=7, choices=STATE, default='L',
                            verbose_name='Estado do resíduo:')

    SOLVENT = (
        ('A','Solução Aquosa'),
        ('O','Solvente Orgânico')
    )

    solvent_type = models.CharField(max_length=7, choices=SOLVENT, default='A',
                                 verbose_name='Solvente principal', name='solvent_type')

    halogen = models.BooleanField(default=False, verbose_name='Halogenados', name='halogen')
    acetonitrile = models.BooleanField(default=False, verbose_name='Acetonitrilas', name='acetonitrile')
    heavy_metals = models.BooleanField(default=False, verbose_name='Metais pesados', name='heavy_metals')
    sulfur = models.BooleanField(default=False, verbose_name='Sulfurados', name='sulfur')
    cyanide = models.BooleanField(default=False, verbose_name='Geradores de cianeto', name='cyanide')
    amine = models.BooleanField(default=False, verbose_name='Aminas', name='amine')
    explosive = models.BooleanField(default=False, verbose_name='Explosivo', name='explosive')
    flammable = models.BooleanField(default=False, verbose_name='Inflamável', name='flammable')
    oxidizing = models.BooleanField(default=False, verbose_name='Oxidante', name='oxidizing')
    under_pressure = models.BooleanField(default=False, verbose_name='Sob pressão', name='under_pressure') #pushing down on me...
    toxic = models.BooleanField(default=False, verbose_name='Tóxico', name='toxic') #THAT'S SILLY
    corrosive = models.BooleanField(default=False, verbose_name='Corrosivo', name='corrosive')
    health_dangerous = models.BooleanField(default=False, verbose_name='Dano à saúde', name='health_dangerous') #THAT'S SILLY
    pollutant = models.BooleanField(default=False, verbose_name='Poluente', name='pollutant') #THAT'S SILLY
    can_agitate = models.BooleanField(default=False, verbose_name='Agitável', name='can_agitate')

    comments = models.TextField(blank=True, verbose_name='Comentários')

    class Meta:
        verbose_name = 'Resíduo'
        verbose_name_plural = 'Resíduos'

    def __str__(self):
        #TODO: por que tem que aparecer o nome do gerador na lista de residuos?
        return ': '.join([self.generator.full_name, self.chemical_makeup])

    def boolean_to_X(self):
        substance_properties = {'halogen': self.halogen,
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
                                'health_dangerous':self.health_dangerous,
                                'pollutant' :self.pollutant,
                                'can_agitate':self.can_agitate
                                }

        property_checks = {name: (lambda x: 'X' if x else ' ')(boolean) for
                         name, boolean in substance_properties.items()}

        return property_checks

    # TODO: adicionar localização no estoque e talvez data de produção.
    def inventory_label(self):
        s = ''

        if self.is_liquid=='S':
            s+='1'
        elif self.is_liquid=='L':
            s+='2'

            if self.solvent_type == 'O':
                s+='.1'
                if self.cyanide:
                    s+='.1'
                elif self.halogen:
                    s+='.2'
                elif self.toxic:
                    s+='.3'
                else:
                    s+='.0'

            elif self.solvent_type =='A':
                s+= '.2'
                if self.toxic:
                    s+='.1'
                else:
                    s+='.0'

                if self.pH==7:
                    s+='.7'
                elif self.pH<7:
                    s+='.6'
                elif self.pH > 7:
                        s += '.8'

            else:
                s+= '.0'


        else:
            s+='0'

        return s

    def status_update(self):
        if self.status == 'user_inventory':
            self.user_editable == True
        else:
            self.user_editable == False