from django.contrib import admin
from django.utils.html import format_html

from .models import Waste, Laboratory, Department, Substance, SubstanceName

admin.site.register(Laboratory)
admin.site.register(Department)


@admin.register(SubstanceName, Substance)
class SubstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_modified_date'
    empty_value_display = ''

    list_display = ('generator', 'view_amount_with_unit',
                    'chemical_makeup_names', 'chemical_makeup_text',
                    'status')

    def view_amount_with_unit(self, obj):
        return str(obj.amount) + ' ' + obj.unit

    view_amount_with_unit.short_description = Waste._meta.get_field(
        "amount").verbose_name.title()
