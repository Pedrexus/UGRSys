from django.urls import path

from dynamicForm.views import myview, dynamic_form

urlpatterns = [
    path('', dynamic_form, name='myview'),
]