from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template

from labs.models import Waste
from .labels import render_to_pdf


@login_required
def generate_view(request, residuo_id, *args, **kwargs):
    waste = Waste.objects.get(pk=residuo_id)
    checks = waste.boolean_to_X()

    context = {
        "residuo": waste.chemical_makeup,
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
    # template = get_template('pdfwriter/label.html')
    # html = template.render(context)
    pdf = render_to_pdf('pdfwriter/label.html', context)
    return HttpResponse(pdf, content_type='html')
