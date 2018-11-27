from django import forms
from django.utils.translation import gettext_lazy as _

from suggestions.models import Suggestion


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion

        fields = (
            'comments',
        )
        labels = {
            'comments': _('Deixe aqui sua sugestão ou comentário para que '
                          'possamos melhorar. E caso tenha encontrado algum '
                          '"bug", não deixe de reportar, por favor XD'),
        }
        help_texts = {
            'comments': _('Faça uma sugestão ou reporte um "bug" pra gente.')
        }
        widgets = {
            'comments': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
        }