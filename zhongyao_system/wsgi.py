"""WSGI config for Zhongyao System project."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyao_system.settings')

application = get_wsgi_application()
