from PIL import Image
import barcode
from barcode.writer import ImageWriter

def graphics(request):
# ... create/load image here ...
    #INK = "red", "blue", "green", "yellow"
    #image = Image.new("RGB", (800, 600), random.choice(INK))

    EAN = barcode.get_barcode_class('ean13')
    ean = EAN(u'5901234123457',writer=ImageWriter())

    img = Image.new("RGB", (300,300), "#FFFFFF")
    with open('/img.png', 'w') as f:
        ean.write(f)

    return