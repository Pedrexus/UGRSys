"""DeGRSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.registration, name='registration')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='registration')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from labs import urls as labs_urls
from registration import urls as home_urls
from pdfwriter import urls as pdf_urls
from dynamicForm import urls as dynamic_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('labs/', include(labs_urls)),
    path('', include(home_urls)),
    path('pdf/', include(pdf_urls)),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view()),

    # path('dynamic/', include(dynamic_urls)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
