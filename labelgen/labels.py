from django.template.loader import get_template
import os
from django.conf import settings
import barcode
from barcode.writer import ImageWriter


def render_label(template_src, context_dict={}):
    template = get_template(template_src)
    render_barcode(context_dict.get("barcode")) #ABSTRACT)
    html = template.render(context_dict)
    return html


def render_barcode(code):
    BARCODE = barcode.get_barcode_class('code39') #TODO: documentar o tipo de codigo de barras
    bar = BARCODE(code,writer=ImageWriter())
    bar.save(os.path.join(settings.MEDIA_ROOT,'barcode')) #TODO: hard-link pra uso no template