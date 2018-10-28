from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from labs.models import Department, Laboratory
from labs.validators import phone_regex
from registration.models import MyUser


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=50, required=True, help_text='',
                                label=_('Nome completo'))
    # TODO: omitir first_name e last_name no admin

    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        empty_label=None,
                                        label=_('Departamento'))
    laboratory = forms.ModelChoiceField(queryset=Laboratory.objects.all(),
                                        empty_label=None,
                                        label=_('Laboratório'))

    email = forms.EmailField(max_length=254, required=True,
                             help_text='Informe um endereço de e-mail válido.',
                             label=_('e-mail'))
    phone_number = forms.CharField(validators=[phone_regex], required=True,
                                   max_length=17, help_text=_(
            'Campo Obrigatório. Informe um número de telefone para contato.'),
                                   label=_('Contato'))

    class Meta:
        model = MyUser
        fields = ('username',
                  'full_name', 'department', 'laboratory',
                  'email', 'phone_number',
                  'password1', 'password2')


class UpdateMyUserForm(forms.ModelForm):
    full_name = forms.CharField(max_length=50, required=True, help_text='',
                                label=_('Nome completo'))
    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        empty_label=None,
                                        label=_('Departamento'))
    laboratory = forms.ModelChoiceField(queryset=Laboratory.objects.all(),
                                        empty_label=None,
                                        label=_('Laboratório'))
    phone_number = forms.CharField(validators=[phone_regex], required=True,
                                   max_length=17, help_text=_(
            'Campo Obrigatório. Informe um número de telefone para contato.'),
                                   label=_('Contato'))

    class Meta:
        model = MyUser
        fields = ('full_name', 'department', 'laboratory', 'phone_number')
