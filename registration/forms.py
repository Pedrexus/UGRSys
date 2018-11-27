from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from labs.models import Department, Laboratory
from labs.validators import phone_regex
from registration.models import MyUser, User


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=50, required=True, help_text='',
                                label=_('Nome completo'))
    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        empty_label=_('Departamento'),
                                        label=_('Departamento'))
    laboratory = forms.ModelChoiceField(queryset=Laboratory.objects.all(),
                                        empty_label=_('Laboratório'),
                                        label=_('Laboratório'))

    email = forms.EmailField(max_length=254, required=True,
                             help_text='Informe um endereço de e-mail válido.',
                             label=_('e-mail'))
    phone_number = forms.CharField(validators=[phone_regex], required=True,
                                   max_length=17, help_text=_(
            'Informe um número de telefone para contato.'),
                                   label=_('Contato'))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.save()

        my_user = MyUser.objects.create(
            user=user,
            full_name=self.cleaned_data.get('full_name'),
            department=self.cleaned_data.get('department'),
            laboratory=self.cleaned_data.get('laboratory'),
            email=self.cleaned_data.get('email'),
            phone_number=self.cleaned_data.get('phone_number'),
        )
        if commit:
            my_user.save()

        return my_user


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
