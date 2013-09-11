import os
import sys

sys.path = ['/home/ubuntu/UclaCalorieCounter'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'UclaCalorieCounter.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
