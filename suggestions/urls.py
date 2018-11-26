from django.urls import path

from suggestions.views import user_report

urlpatterns = [
    path('report/', user_report, name='user_report'),
]