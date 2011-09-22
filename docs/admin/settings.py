# -*- coding: UTF-8 -*-
# Django settings for mysite project.
from os.path import join, dirname
from lino.apps.dsbe.settings import *

class Lino(Lino):

    title = u"My first Lino site"
    csv_params = dict(delimiter=',',encoding='utf-16')

LINO = Lino(__file__,globals())

LANGUAGE_CODE = 'fr' # "main" language
LANGUAGES = language_choices('fr','nl','en')

LINO.appy_params.update(pythonWithUnoPath='/etc/openoffice.org3/program/python')

LOGGING = dict(filename='/var/log/lino/system.log'),level='DEBUG')
# some alternative examples:
# LOGGING = dict(filename=join(LINO.project_dir,'log','system.log'),level='DEBUG')
# LOGGING = dict(filename=None,level='DEBUG')


# MySQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', 
#         'NAME': 'mysite',                  
#         'USER': 'django',                     
#         'PASSWORD': 'my cool password',               
#         'HOST': 'localhost',                  
#         'PORT': 3306,
#     }
# }

# sqlite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite', 
        'NAME': join(LINO.project_dir,'mysite.db')
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cqt^18t(Fb#14a@s%mbtdif+ih8fscpf8l9aw+0ivo2!3c(c%&'

EMAIL_HOST = "mail.example.com"
#EMAIL_PORT = ""
