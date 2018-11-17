from django.contrib import admin
from django.core.checks import messages
from django.utils.html import format_html

from .models import Waste, Laboratory, Department, Substance, SubstanceName

admin.site.register(Laboratory)
admin.site.register(Department)


@admin.register(SubstanceName, Substance)
class SubstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    actions = ['evaluate_wastes', ]

    date_hierarchy = 'last_modified_date'
    empty_value_display = ''

    list_display = ('generator', 'view_amount_with_unit',
                    'chemical_makeup_names', 'chemical_makeup_text',
                    'status')
    # list_display_links = None
    # list_editable = ('status',)
    list_filter = ('status', 'generator',)
    filter_horizontal = ('chemical_makeup',)

    def view_amount_with_unit(self, obj):
        return str(float(obj.amount)) + ' ' + obj.unit

    view_amount_with_unit.short_description = Waste._meta.get_field(
        "amount").verbose_name.title()

    def evaluate_wastes(self, request, queryset):
        wastes_1 = queryset.filter(status=Waste.STATUS_1)
        if len(wastes_1) != 0:
            if len(wastes_1) == 1:
                message_bit = '1 resíduo está com o usuário. '
            else:
                message_bit = f'{len(wastes_1)} resíduos estão com o usuário. '
            message = message_bit + \
                'Avalie apenas resíduos que estão aguardando retirada.'

            self.message_user(request, message, level=messages.ERROR)
        else:
            queryset.update(status=Waste.STATUS_3)

    evaluate_wastes.short_description = "Avaliar resíduos"
