from django import forms
from django.utils.translation import gettext_lazy as _

from stats.models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation

        fields = (
            'in_accordance_with_description',
            'flask_conditions',
            'storage_conditions',
            'tag_conditions',
            'help_from_generator',
            'extra_comments',
        )

        labels = {
            'in_accordance_with_description': _('De acordo com a descrição'),
            'flask_conditions': _('Condições da bomba'),
            'storage_conditions': _('Situação da armazenagem'),
            'tag_conditions': _('Situação da etiqueta'),
            'help_from_generator': _('Atendimento do gerador'),
            'extra_comments': _('Comentário adicionais'),
        }
        empty_labels = {
            'in_accordance_with_description': _('De acordo com a descrição'),
            'flask_conditions': _('Condições da bomba'),
            'storage_conditions': _('Situação da armazenagem'),
            'tag_conditions': _('Situação da etiqueta'),
            'help_from_generator': _('Atendimento do gerador'),
        }
        help_texts = {
            'in_accordance_with_description': _('A descrição e a etiqueta '
                                                'estão em conformidade com'
                                                ' o resíduo?'),
            'flask_conditions': _('a bomba está trincada ou sobrecarregada?'),
            'storage_conditions': _('A bomba está suja'
                                    ' ou foi difícil de encontrá-la?'),
            'tag_conditions': _('A etiqueta está bem colocada,'
                                ' as informações dela estão legíveis?'),
            'help_from_generator': _('Como foi o auxílio que o gerador'
                                     ' do resíduo lhe concedeu?'),
            'extra_comments': _('Algum comentário adicional ao gerador?')
        }
        error_messages = {

        }
        widgets = {
            'extra_comments': forms.Textarea(attrs={'cols': 75, 'rows': 10}),
        }
