from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from labs.models import Waste
from .labels import render_label

import re

@login_required
def generate_view(request, residuo_id, *args, **kwargs):
    waste = Waste.objects.get(pk=residuo_id)
    checks = waste.boolean_to_x()

    context = {
        "residuo": waste.chemical_makeup,
         "barcode": barcode_number(waste),
        "nome_gerador": waste.generator,
        "laboratorio": waste.generator.laboratory,
        "telefone": waste.generator.phone_number,
        "data_de_postagem": waste.creation_date,
        "email": waste.generator.email,
        "halogen_check": checks['halogen'],
        "acetonitrile_check": checks['acetonitrile'],
        "heavy_metals_check": checks['heavy_metals'],
        "sulfur_check": checks['sulfur'],
        "cyanide_check": checks['cyanide'],
        "amine_check": checks['amine'],
        "pH": waste.pH,
        "inventory_location": waste.inventory_label()
    }

#TODO: INCLUIR OPÇÃO PARA OUTROS TAMANHOS DE ETIQUETA
    label = render_label('labelgen/label.html', context)
    return HttpResponse(label, content_type='html')

def barcode_number(waste):
    #TODO: colocar data e limite de dígitos
    date = re.sub("\D", "", str(waste.creation_date))[:8] #YYYYMMDD :8
    return date+str(waste.pk).zfill(6) #preenche até 6 digitos. Quando passar de 1 milhao de resíduos vai quebrar eu conserto.

