from django.contrib import admin
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Waste, Laboratory, Department

admin.site.register(Laboratory)
admin.site.register(Department)


@admin.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    actions = ['evaluate_wastes', ]

    date_hierarchy = 'last_modified_date'
    empty_value_display = ''

    list_display = ('generator', 'view_amount_with_unit',
                    'chemical_makeup_names', 'chemical_makeup_text',
                    'status')
    list_display_links = None
    # list_editable = ('status',)
    list_filter = ('status', 'generator',)
    filter_horizontal = ('chemical_makeup',)

    def get_queryset(self, request):
        queryset = super(WasteAdmin, self).get_queryset(request)
        return queryset.exclude(status=Waste.STATUS_BOOKMARK)

    def view_amount_with_unit(self, obj):
        return str(float(obj.amount)) + ' ' + obj.unit

    view_amount_with_unit.short_description = Waste._meta.get_field(
        "amount").verbose_name.title()

    def evaluate_wastes(self, request, queryset):
        wastes_1 = queryset.filter(status=Waste.STATUS_1)
        wastes_3_or_4 = queryset.filter(
            status=Waste.STATUS_3) | queryset.filter(status=Waste.STATUS_4)

        message_bit_1 = ''
        if len(wastes_1) != 0:
            if len(wastes_1) == 1:
                message_bit_1 = '1 resíduo está com o usuário. '
            else:
                message_bit_1 = f'{len(wastes_1)} resíduos estão com o usuário. '

        message_bit_2 = ''
        if len(wastes_3_or_4) != 0:
            if len(wastes_3_or_4) == 1:
                message_bit_2 = '1 resíduo já está com o DeGR. '
            else:
                message_bit_2 = f'{len(wastes_3_or_4)} resíduos já estão com o DeGR. '

        if message_bit_1 or message_bit_2:
            message = message_bit_1 + message_bit_2 + \
                      'Avalie apenas resíduos que estão aguardando retirada.'
            self.message_user(request, message, level=messages.ERROR)
        else:
            queryset_ids = ','.join([str(waste.pk) for waste in queryset])
            return HttpResponseRedirect(
                reverse('evaluate_wastes', args=[queryset_ids])
            )

    evaluate_wastes.short_description = "Avaliar resíduos"
