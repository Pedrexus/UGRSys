from django.urls import path
from .views import home, home_logout, signup, activate, account_activation_sent
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('logout/', home_logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='update_password'),
]
