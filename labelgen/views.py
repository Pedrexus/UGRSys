import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from labs.models import Waste
from registration.models import MyUser
from .labels import render_label


@login_required
def generate_view(request, residuo_id, *args, **kwargs):
    waste = Waste.objects.get(pk=residuo_id)
    generator = MyUser.objects.get(user=request.user)
    checks = waste.boolean_to_x()

    #print(waste.chemical_makeup_names)
    print(waste.chemical_makeup)

    context = {
        "residuo": waste.chemical_makeup_names,
         "residuo_extra": waste.chemical_makeup_text,
         "barcode": barcode_number(waste),
        "nome_gerador": generator,
        "laboratorio": generator.laboratory,
        "telefone": generator.phone_number,
        "data_de_postagem": waste.creation_date,
        "email": generator.email,
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
    return date+str(waste.pk).zfill(6) #preenche até 6 digitos. Quando passar de 1 milhao de resíduos vai quebrar

