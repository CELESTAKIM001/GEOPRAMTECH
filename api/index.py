import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geopram_tech.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel expects 'app' for WSGI
app = application
