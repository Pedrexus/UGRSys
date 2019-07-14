from collections import defaultdict

from django.contrib import admin
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe

from labs.filters import GeneratorListFilter
from registration.models import MyUser
from stats.models import Evaluation
from .models import Waste, Laboratory, Department
from .reports import csv_view, xlsx_view

admin.site.disable_action('delete_selected')


def export_as_csv(modeladmin, request, queryset):
    return csv_view(request, queryset)


export_as_csv.short_description = 'Exportar como CSV'


def export_as_xlsx(modeladmin, request, queryset):
    return xlsx_view(request, queryset)


export_as_csv.short_description = 'Exportar como Excel'


@admin.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    '''Class to add features to staff user to deal with waste objects'''
    actions = ['evaluate_wastes', export_as_csv, export_as_xlsx]
    #pq só evaluate_wastes é método da classe?

    date_hierarchy = 'last_modified_date'
    empty_value_display = None

    list_display = ('get_generator', 'view_amount_with_unit',
                    'chemical_makeup_names',
                    'status')

    list_display_links = ('view_amount_with_unit',)
    fields = ('amount', 'unit',)

    list_filter = (
        'status',
        GeneratorListFilter,
    )
    # list_editable = ('amount', )
    filter_horizontal = ('chemical_makeup',)

    def get_queryset(self, request):
        '''Gets set of waste objects'''
        queryset = super(WasteAdmin, self).get_queryset(request)
        return queryset.exclude(status=Waste.STATUS_BOOKMARK)

    def get_generator(self, obj):
        '''Gets user object'''
        return MyUser.objects.get(user=obj.generator).full_name

    #TODO: listar por Lab e departamento?

    get_generator.short_description = 'Gerador'

    def view_amount_with_unit(self, obj):
        '''Gets amount of waste'''
        #TODO: como essa função se comporta se for passada uma lista de
        #resíduos?
        return str(float(obj.amount)) + ' ' + obj.unit

    view_amount_with_unit.short_description = Waste._meta.get_field(
        "amount").verbose_name.title()

    def evaluate_wastes(self, request, queryset):
        '''Returns page with fields to technitian to evaluate
        the received waste

        O técnico só pode avaliar resíduos com
        STATUS_2: 'Aguardando retirada.
        Após a avaliação o resíduo receberá STATUS_3: 'Inventório DeGR') '''

        wastes_1 = queryset.filter(status=Waste.STATUS_1) #Com usuário
        wastes_3_or_4 = queryset.filter(
            status=Waste.STATUS_3) | queryset.filter(status=Waste.STATUS_4) #Com DeGR

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
            #Somente resíduos que foram retirados (status_2) podem seguir.
            #Se a query é valida, prossegue:
            queryset_ids = ','.join([str(waste.pk) for waste in queryset])
            return HttpResponseRedirect(
                reverse('evaluate_wastes', args=[queryset_ids])
            )

        #TODO: testamos o evaluate para um query c/ múltiplos resíduos?

    evaluate_wastes.short_description = "Avaliar resíduos"


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    '''Class to add features to staff user to deal with laboratory objects'''
    actions = ['delete_selected', 'lab_export_as_csv', 'export_as_xlsx']

    empty_value_display = ''

    list_display = (
        'name',
        'get_number_generators',
        'get_amount_waste_sent',
        'view_frequencies',
        'get_average_grade',
    )

    list_display_links = None
    list_filter = ('name',)  # 'average_grade',)
    list_editable = ('name',)

    def lab_export_as_csv(self, request, queryset):
        '''DON'T. Doesn't work as intended!!'''
        #TODO: deve retornar resíduos de um laboratorio
        # generators = queryset.objects.get()
        return csv_view(request, queryset)

    lab_export_as_csv.short_description = 'Exportar como CSV'

    def get_number_generators(self, obj):
        '''Returns number of registered users that belongs to
        such laboratory'''
        amount = len(MyUser.objects.filter(laboratory=obj))
        return str(amount)

    get_number_generators.short_description = 'Número de Geradores'

    def get_amount_waste_sent(self, obj):
        '''Provides statistics: amount of waste sent by lab

        All time record only. No filters yet available'''
        lab_users = [my_user.user for my_user in
                     MyUser.objects.filter(laboratory=obj)]
        lab_wastes = Waste.objects.filter(generator__in=lab_users)

        amount_kg = sum(
            waste.amount for waste in
            lab_wastes.filter(unit='Kg').exclude(status=Waste.STATUS_1)
        ) #.normalize()
        amount_l = sum(
            waste.amount for waste in
            lab_wastes.filter(unit='L').exclude(status=Waste.STATUS_1)
        ) #.normalize()

        return str(amount_kg) + ' Kg + ' + str(amount_l) + ' L'

    get_amount_waste_sent.short_description = 'Quantidade de Resíduo Enviado'

    @staticmethod
    def get_frequencies(obj):
        '''Provides statistics of lab: frequency of each waste'''
        #TODO: frequencia aqui não é uma série temporal,
        #mas quais são os resíduos mais frequentes??
        #não sei como isso deveria ser usado/implementado
        lab_users = [my_user.user for my_user in
                     MyUser.objects.filter(laboratory=obj)]
        lab_wastes = Waste.objects.filter(generator__in=lab_users)

        frequencies = defaultdict(lambda: defaultdict(float))
        for waste in lab_wastes:
            for name, amount in waste.substances_amounts.items():
                frequencies[name][waste.unit] += amount

        return frequencies

    def view_frequencies(self, obj):
        #vide get_frequencies
        freq = self.get_frequencies(obj)

        info = ['<strong>' + s_name + '</strong>' + ': ' + str(freq[s_name]['Kg']) + ' Kg + ' + str(freq[s_name]['L']) + ' L' for s_name in freq]

        return mark_safe(linebreaks(', \n'.join(info)))

    view_frequencies.short_description = 'Quantidade por Substância'
    # name, frequency = Counter(db_wastes).most_common(1)[0]

    def get_average_grade(self, obj):
        '''Provides statistics of lab: average grade of evaluated waste'''
        lab_users = [my_user.user for my_user in
                     MyUser.objects.filter(laboratory=obj)]
        lab_wastes = Waste.objects.filter(generator__in=lab_users)
        lab_eval = Evaluation.objects.filter(waste__in=lab_wastes)

        fields = Evaluation._meta.get_fields()[1:-1]
        grades = [sum([int(getattr(e, field.name)) for field in fields])/len(fields) for e in lab_eval]
        if len(lab_eval):
            avg_grade = 2*sum(grades)/len(lab_eval) #avaliação vai de 1 a 5. Tem que padronizar.
                        #TODO: ja foi feito um sum() ali em cima. Está correto isso??
        else:
            avg_grade = '' #nao deveria retornar 0 ou NaN?

        return str(avg_grade) + '/10' if avg_grade else ''
    get_average_grade.short_description = 'Avaliação Média'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    '''Class to add features to staff user to deal with department objects'''
    actions = ['delete_selected', 'export_as_csv', 'export_as_xlsx']

    empty_value_display = ''

    list_display = ('name',)
    # 'get_number_generators', 'get_amount_waste',
    # 'get_most_frequent_waste',
    # 'get_average_grade')
    list_display_links = None
    list_filter = ('name',)  # 'average_grade',)
    list_editable = ('name',)
