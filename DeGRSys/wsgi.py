"""
WSGI config for DeGRSys project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

from dj_static import Cling
from django.core.wsgi import get_wsgi_application

sys.path.append('/opt/bitnami/apps/django/django_projects/DeGRSys')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/DeGRSys/egg_cache")

os.environ['DJANGO_SETTINGS_MODULE'] = 'DeGRSys.settings'

# allow django to serve static files
application = Cling(get_wsgi_application())
