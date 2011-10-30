#
# mod_wsgi handler for the onlineweb django project
#


import site
site.addsitedir('/home/dotkom/norangsh/virtualenv/geocalendar/lib/python2.6/site-packages')

import os
import sys

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

sys.path.append('/home/dotkom/norangsh/web/geocalendar')
sys.path.append('/home/dotkom/norangsh/web/geocalendar/geocalendar')

os.environ['DJANGO_SETTINGS_MODULE'] = 'geocalendar.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

