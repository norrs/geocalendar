import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'geocalendar.settings'

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
