import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"{os.getenv('PROJECT_NAME', 'project')}.settings")

application = get_asgi_application()
