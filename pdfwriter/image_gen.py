from django.http import HttpResponse
from PIL import Image

import random

def graphics(request):
# ... create/load image here ...
    INK = "red", "blue", "green", "yellow"
    image = Image.new("RGB", (800, 600), random.choice(INK))

    # serialize to HTTP response
    response = HttpResponse()
    image.save(response, "PNG")
    return response