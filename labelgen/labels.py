from django.template.loader import get_template
import os
from django.conf import settings
import barcode
from barcode.writer import ImageWriter
import random, string #why? deprecated

def render_label(template_src, context_dict={}):
    '''Renders a html page that will be print as a label'''
    template = get_template(template_src)
    render_barcode(context_dict.get("barcode")) #ABSTRACT
    html = template.render(context_dict)
    return html


def render_barcode(code):
    '''Renders a barcode as a image and saves to the media folder'''
    BARCODE = barcode.get_barcode_class('code39') #TODO: documentar o tipo de codigo de barras
    bar = BARCODE(code,writer=ImageWriter())
    bar.save(os.path.join(settings.MEDIA_ROOT,'barcode')) #TODO: hard-link pra uso no template
