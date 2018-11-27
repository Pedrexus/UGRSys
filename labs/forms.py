from django import forms
from django.utils.translation import gettext_lazy as _

# from django.forms import formset_factory
from labs.validators import message_percentages_regex
from .models import Waste


class WasteForm(forms.ModelForm):
    class Meta:
        model = Waste

        fields = ('amount',
                  'unit',
                  'chemical_makeup',
                  'chemical_makeup_pct',
                  'chemical_makeup_text',
                  'chemical_makeup_text_pct',
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
            'amount': _('Quantidade'),
            'unit': _('unidade'),
            'is_liquid': _('Estado físico'),
            'solvent_type': _('Tipo de solvente'),
            'pH': _('pH'),
            'halogen': _('O resíduo contém halogenados?'),
            'acetonitrile': _('O resíduo contém acetonitrila?'),
            'heavy_metals': _('O resíduo contém metais pesados?'),
            'sulfur': _(
                'O resíduo contém substâncias sulfuradas?'),
            'cyanide': _(
                'O resíduo contém geradores de cianeto?'),
            'amine': _('O resíduo contém aminas?'),
            'chemical_makeup': _('Composição Química'),
            'chemical_makeup_pct': _('Concentrações'),
            'chemical_makeup_text': _('Composição Química Extra'),
            'chemical_makeup_text_pct': _('Concentrações Extra'),
            'explosive': _('explosivo?'),
            'flammable': _('inflamável?'),
            'oxidizing': _('oxidante?'),
            'under_pressure': _('sob pressão?'),
            'toxic': _('tóxico?'),
            'corrosive': _('corrosivo?'),
            'health_dangerous': _('perigo à saude?'),
            'pollutant': _('dano ambiental?'),
            'cannot_agitate': _('proibido agitar?'),
            'comments': _('Comentários adicionais')
        }
        help_texts = {
            'amount': _(
                'Uma estimativa da quantidade de resíduo.'),

            'chemical_makeup': _('Composição química do resíduo.'),
            'chemical_makeup_pct': _('Separe as concentrações por vírgula,'
                                     ' e.g.: 30%, 15%, 55%'),

            'chemical_makeup_text': _('Substâncias que não tenham sido'
                                      ' encontradas no campo anterior. '
                                      'Separe-as por vírgula, '
                                      'e.g.: Bananas, Chocolate'),
            'chemical_makeup_text_pct': _('Concentrações dos compostos extras.'
                                          ' Separe por vírgula a concentração'
                                          ' de cada um dos compostos.'),

            'solvent_type': _(
                'Caso a solução seja líquida, qual o solvente?'),
        }
        error_messages = {
            'chemical_makeup_pct': {
                'validators': message_percentages_regex
            },
            'chemical_makeup_text_pct': {
                'validators': message_percentages_regex
            }
        }
        widgets = {
            'comments': forms.Textarea(attrs={'cols': 75, 'rows': 10}),
            'chemical_makeup': forms.SelectMultiple(
                attrs={'style': "display: none"}),
        }

    def clean(self):
        cleaned_data = super(WasteForm, self).clean()
        chemical_makeup = cleaned_data.get("chemical_makeup")
        chemical_makeup_pct = cleaned_data.get("chemical_makeup_pct")
        chemical_makeup_text = cleaned_data.get("chemical_makeup_text")
        chemical_makeup_text_pct = cleaned_data.get("chemical_makeup_text_pct")

        def make_msg(len_, text=False):
            # TODO: muito confuso. Impossível entender.
            extra_ = 'escritas' if text else 'selecionadas'
            extra_sing = extra_[:-1]

            msg_bit = f"as {len_} substâncias {extra_}. " \
                f"" if len_ > 1 else f"a substância {extra_sing}."
            msg = "Insira concentrações para " + msg_bit + \
                  " Dica: se não tiver certeza, coloque '0%'."
            return msg

        len_ = len(chemical_makeup)
        if len_ and len_ != len(chemical_makeup_pct.split(',')):
            self.add_error('chemical_makeup_pct', make_msg(len_))
        elif len(chemical_makeup_text) and \
                len(chemical_makeup_text.split(',')) != len(
                chemical_makeup_text_pct.split(',')):
            self.add_error('chemical_makeup_text_pct',
                           make_msg(len(chemical_makeup_text.split(',')),
                                    text=True))
