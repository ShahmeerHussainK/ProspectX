"""
ASGI config for projectEVS project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import sys

filepath = os.path.abspath(__file__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(filepath)))))




import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prospectx_new.settings")
django.setup()
application = get_default_application()
