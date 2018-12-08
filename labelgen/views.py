import base64
import io

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from labs.models import Waste
from registration.models import MyUser
import pyqrcode as qr


@login_required
def generate_view(request, residuo_id, *args, **kwargs):
    waste = Waste.objects.get(pk=residuo_id)
    generator = MyUser.objects.get(user=request.user)
    checks = waste.boolean_to_x()

    context = {
        "residuo": waste.chemical_makeup_names,
        "qrcode": qr_as_tag(obj=waste, encode='svg'),
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

    # TODO: INCLUIR OPÇÃO PARA OUTROS TAMANHOS DE ETIQUETA
    return render(request, 'labelgen/label.html', context)


def qr_as_tag(obj, encode='svg'):
    if encode == 'svg':
        return qrcreate(obj).getvalue().split(b'\n')[1].decode("utf-8")
    elif encode == 'png':
        binary_img = base64.b64encode(qrcreate(obj).getvalue())
        img_tag = "<img src='data:image/png;base64," + binary_img + "'/>"
        return img_tag


def qrcreate(obj):
    text = waste_as_text(obj)
    img = qr.create(text, error='L', version=12, mode='binary')

    buffer = io.BytesIO()
    img.svg(buffer, scale=2)

    # do whatever you want with buffer.getvalue()
    return buffer


def waste_as_text(waste):
    generator = MyUser.objects.get(user=waste.generator)
    text = f"Dados do Resíduo:\n " \
        f"\tNome do Gerador:\t {generator}\n" \
        f"\tContato do Gerador:\t {generator.phone_number}\n" \
        f"\te-mail do Gerador:\t {generator.email}\n" \
        f"\tGrupo do Gerador:\t {generator.laboratory}\n" \
        f"\tData de Criação:\t {waste.creation_date}\n" \
        f"\tComposição Química:\t {waste.chemical_makeup_names}\n" \
        f"\tpH:\t {waste.pH}\n"

    return text
