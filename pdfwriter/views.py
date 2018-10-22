from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .labels import render_to_pdf


def generate_view(request, user_id, residuo_id, *args, **kwargs):
    template = get_template('pdfwriter/etiqueta.html')
    context = {
        "residuo": 'aaaa',
        "nome_gerador": 'aaaaaaaaaaaaa',
        "laboratorio":'aaaaa',
        "telefone": '000000',
        "residuo_id": str(residuo_id),
        "email": 'bbbbbbbb',
    }
    html = template.render(context)
    pdf = render_to_pdf('./etiqueta.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
