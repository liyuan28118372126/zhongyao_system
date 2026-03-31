"""Settings package."""

from .base import *

# Import environment-specific settings
import os

if os.environ.get('DJANGO_ENV') == 'production':
    from .prod import *
else:
    from .dev import *
