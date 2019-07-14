import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from labs.models import Waste
from registration.models import MyUser
from .labels import render_label


@login_required
def generate_view(request, residuo_id, *args, **kwargs):
    '''Generates a label (html page) to be printed'''

    waste = Waste.objects.get(pk=residuo_id)
    generator = MyUser.objects.get(user=request.user)
    #assim estamos assumindo que o request.user == waste.generator.
    #será seguro?

    checks = waste.boolean_to_x()
    #TODO: trazer essa função pra cá.
    #não faz sentido deixar na classe.
    #ainda por cima está em Substance, não Waste.

    #print(waste.chemical_makeup_names)
    print(waste.chemical_makeup)

    context = { #passa essas informações pra pagina em html:
        "residuo": waste.chemical_makeup_names,
         # "residuo_extra": waste.chemical_makeup_text,
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
    label = render_label('labelgen/label.html', context) #em templates/labelgen
    return HttpResponse(label, content_type='html')

def barcode_number(waste):
    #TODO: passar isso pra classe Waste. E garantir unicidade!
    #TODO: colocar data e limite de dígitos
    date = re.sub("\D", "", str(waste.creation_date))[:8] #YYYYMMDD :8
    return date+str(waste.pk).zfill(6) #preenche até 6 digitos. Quando passar de 1 milhao de resíduos vai quebrar

