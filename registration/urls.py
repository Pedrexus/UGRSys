from django.urls import path
from .views import home, home_logout, signup

urlpatterns = [
    path('', home, name='home'),
    path('logout/', home_logout, name='logout'),
    path('signup/', signup, name='signup')
]