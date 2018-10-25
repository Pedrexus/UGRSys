from django.urls import path

from .views import generate_view

urlpatterns = [
    path('<residuo_id>', generate_view, name='pdf_waste'),
]
