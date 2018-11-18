from django.contrib import admin

from substances.models import SubstanceName, Substance

admin.site.register(SubstanceName)


@admin.register(Substance)
class SubstanceAdmin(admin.ModelAdmin):
    empty_value_display = ''

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
