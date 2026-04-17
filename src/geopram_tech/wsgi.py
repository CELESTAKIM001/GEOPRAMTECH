"""
WSGI config for GEOPRAM TECHNOLOGIES project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geopram_tech.settings")

application = get_wsgi_application()
