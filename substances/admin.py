from django.contrib import admin

from substances.models import SubstanceName, Substance


@admin.register(SubstanceName)
class NameAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]


@admin.register(Substance)
class SubstanceAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    empty_value_display = None

    list_display = (
        'name',
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
    )
