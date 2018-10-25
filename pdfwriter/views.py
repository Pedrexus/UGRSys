from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template

from labs.models import Waste
from .labels import render_to_pdf

@login_required
def generate_view(request, residuo_id, *args, **kwargs):
    template = get_template('pdfwriter/label.html')

    waste = Waste.objects.get(pk=residuo_id)

    context = {
        "residuo": waste.chemical_makeup,
        "nome_gerador": waste.generator,
        "laboratorio":waste.generator.department,
        "telefone": waste.generator.phone_number,
        "data_de_postagem": waste.creation_date,
        "email": waste.generator.email,
    }
    html = template.render(context)
    pdf = render_to_pdf('pdfwriter/label.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
