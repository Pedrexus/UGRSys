from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Waste


# from django.forms import formset_factory


class WasteForm(forms.ModelForm):
    class Meta:
        model = Waste
        fields = ('amount',
                  'unit',
                  'chemical_makeup',
                  'chemical_makeup_text',
                  'is_liquid',
                  'solvent_type',
                  'pH',
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
                  'cannot_agitate',
                  'comments',
                  )
        labels = {
            'amount':               _('Quantidade'),
            'unit':                 _('unidade'),
            'is_liquid':            _('Estado físico'),
            'solvent_type':         _('Tipo de solvente'),
            'pH':                   _('pH'),
            'halogen':              _('O resíduo contém halogenados?'),
            'acetonitrile':         _('O resíduo contém acetonitrila?'),
            'heavy_metals':         _('O resíduo contém metais pesados?'),
            'sulfur':               _(
                'O resíduo contém substâncias sulfuradas?'),
            'cyanide':              _(
                'O resíduo contém geradores de cianeto?'),
            'amine':                _('O resíduo contém aminas?'),
            'chemical_makeup':      _('Composição Química'),
            'chemical_makeup_text': _('Composição Química Extra'),
            'explosive':            _('explosivo?'),
            'flammable':            _('inflamável?'),
            'oxidizing':            _('oxidante?'),
            'under_pressure':       _('sob pressão?'),
            'toxic':                _('tóxico?'),
            'corrosive':            _('corrosivo?'),
            'health_dangerous':     _('perigo à saude?'),
            'pollutant':            _('dano ambiental?'),
            'cannot_agitate':       _('proibido agitar?'),
            'comments':             _('Comentários adicionais')
        }
        help_texts = {
            'amount':               _(
                'Uma estimativa da quantidade de resíduo.'),
            'chemical_makeup':      _('Composição química do resíduo.'),
            'chemical_makeup_text': _(
                'Substâncias que não tenham sido encontradas no campo anterior.'),
            'solvent_type':         _(
                'Caso a solução seja líquida, qual o solvente?'),
        }
        error_messages = {
            'chemical_makeup': {
                'max_length': _(
                    "Mais de 200 caracteres. Está muito longo."),
            },
        }
        widgets = {
            'comments':        forms.Textarea(attrs={'cols': 75,'rows': 10}),
            'chemical_makeup': forms.SelectMultiple(
                attrs={'style': "display: none"}),
        }
