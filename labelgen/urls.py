from django.urls import path

from .views import generate_view
from .image_gen import graphics

urlpatterns = [
    path('img', graphics),
    path('<residuo_id>', generate_view, name='pdf_waste'),  #TODO: descobrir pq se eu mudar o name quebra a lista de residuos

]
