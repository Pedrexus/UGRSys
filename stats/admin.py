from django.contrib import admin

from stats.filters import GeneratorListFilter, DepartmentListFilter, \
    LaboratoryListFilter
from stats.models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):

    list_display = (
        'get_generator',
        'get_waste_names',
        'in_accordance_with_description',
        'flask_conditions',
        'storage_conditions',
        'tag_conditions',
        'help_from_generator',
    )
    list_editable = (
        'in_accordance_with_description',
        'flask_conditions',
        'storage_conditions',
        'tag_conditions',
        'help_from_generator',
    )
    empty_value_display = ''
    list_display_links = None
    list_filter = (
        GeneratorListFilter,
        DepartmentListFilter,
        LaboratoryListFilter
    )

    def get_generator(self, obj):
        return obj.waste.generator
    get_generator.short_description = 'Gerador'

    def get_waste_names(self, obj):
        return obj.waste.chemical_makeup_names
    get_waste_names.short_description = 'Resíduo'