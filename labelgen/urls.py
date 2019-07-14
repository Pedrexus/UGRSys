from django.urls import path

from .views import generate_view
from .image_gen import graphics

urlpatterns = [
    path('img', graphics), #TODO: acho que ngm mais chama esse path
    path('<residuo_id>', generate_view, name='pdf_waste'), #TODO: mudar
    #pdf_waste pra algo que faça sentido
]
