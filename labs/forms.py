from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from django.forms import formset_factory

from labs.validators import phone_regex
from .models import Waste, MyUser


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=50, required=True, help_text='',
                                label=_('Nome completo'))
    #name = full_name.split(' ')
    #first_name = name[0]
    #last_name = ' '.join(name[1:])

    department = forms.CharField(max_length=50, required=True, help_text='',
                                 label=_('Departamento'))
    email = forms.EmailField(max_length=254, required=False,
                             help_text='Informe um endereço de e-mail válido.',
                             label=_('e-mail'))
    phone_number = forms.CharField(validators=[phone_regex], required=True,
                                   max_length=17, help_text=_(
            'Campo Obrigatório. Informe um número de telefone para contato.'),
                                   label=_('Contato'))

    class Meta:
        model = User
        fields = ('username',
                  'full_name', 'department', 'email', 'phone_number',
                  'password1', 'password2')


class WasteForm(forms.ModelForm):
    class Meta:
        model = Waste
        fields = ('amount',
                  'pH',
                  'unit',
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
            'explosive': forms.RadioSelect,
            'flammable': forms.RadioSelect,
            'oxidizing': forms.RadioSelect,
            'under_pressure': forms.RadioSelect,
            'toxic': forms.RadioSelect,
            'corrosive': forms.RadioSelect,
            'health_dangerous': forms.RadioSelect,
            'pollutant': forms.RadioSelect,
            'can_agitate': forms.RadioSelect,
            'comments': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
        }
