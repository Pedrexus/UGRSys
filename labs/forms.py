from django import forms
from django.utils.translation import gettext_lazy as _
#from django.forms import formset_factory

from .models import Waste


class WasteForm(forms.ModelForm):
    class Meta:
        model = Waste
        #TODO: colocar os booleanos todos juntos
        fields = ('amount',
                  'unit',
                  'is_liquid',
                  'solvent_type',
                  'pH',
                  'chemical_makeup',
                  'halogen',
                  'acetonitrile',
                  'heavy_metals',
                  'sulfur',
                  'cyanide',
                  'amine',
                  'explosive',
                  'flammable',
                  'oxidizing',
                  'under_pressure',
                  'toxic',
                  'corrosive',
                  'health_dangerous',
                  'pollutant',
                  'can_agitate',
                  'comments',
                  )
        labels = {
            'amount': _('Quantidade?'),
            'unit': _('unidade?'),
            'is_liquid':_('Estado?'),
            'solvent_type':_('Caso a solução seja líquida, qual o solvente?'),
            'pH': _('pH'),
            'halogen': _('O resíduo contém halogenados?'),
            'acetonitrile': _('O resíduo contém acetonitrila?'),
            'heavy_metals': _('O resíduo contém metais pesados?'),
            'sulfur': _('O resíduo contém enxofre ou substâncias sulfuradas?'),
            'cyanide': _('O resíduo contém geradores de cianeto?'),
            'amine': _('O resíduo contém aminas?'),
            'chemical_makeup': _('Composição?'), #TODO mudar o form da composição
            'explosive': _('explosivo?'),
            'flammable': _('inflamável?'),
            'oxidizing': _('oxidante?'),
            'under_pressure': _('sob pressão?'),
            'toxic': _('tóxico?'),
            'corrosive': _('corrosivo?'),
            'health_dangerous': _('perigo à saude?'),
            'pollutant': _('poluente?'),
            'can_agitate': _('pode ser agitado?'),
            'comments': _('Comentários adicionais')
        }
        help_texts = {
            'amount': _('Uma estimativa da quantidade de resíduo.'),
            'chemical_makeup': _('Composição química do resíduo.')
        }
        error_messages = {
            'chemical_makeup': {
                'max_length': _(
                    "Mais de 200 caracteres. Está muito longo."),
            },
        }
        widgets = {
           # 'explosive': forms.RadioSelect,
           # 'flammable': forms.RadioSelect,
           # 'oxidizing': forms.RadioSelect,
           # 'under_pressure': forms.RadioSelect,
           # 'toxic': forms.RadioSelect,
           # 'corrosive': forms.RadioSelect,
           # 'health_dangerous': forms.RadioSelect,
           # 'pollutant': forms.RadioSelect,
           # 'can_agitate': forms.RadioSelect,
            'comments': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
        }
