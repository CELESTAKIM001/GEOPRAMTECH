import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geopram_tech.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "geopramtech@gmail.com", "admin!123")
    print("Superuser created: admin")
else:
    user = User.objects.get(username="admin")
    user.set_password("admin!123")
    user.save()
    print("Admin password updated")
