# -*- coding: utf-8 -*-
import os
import sys
import platform
#manage.py
sys.path.insert(0, '/home/c/name/pass/public_html/projectgau')
#settings.py
sys.path.insert(0, '/home/c/name/pass/public_html/projectgau/projectgau')
#myenv
sys.path.insert(0, '/home/c/name/pass/venv/lib/python{0}/site-packages'.format(platform.python_version()[0:3]))
os.environ["DJANGO_SETTINGS_MODULE"] = "projectgau.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()