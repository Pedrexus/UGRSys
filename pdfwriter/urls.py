from django.urls import path

from .views import generate_view

urlpatterns = [
    path('<user_id>/<residuo_id>', generate_view, name='pdfwriter'),
]
