# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino ; if not, see <http://www.gnu.org/licenses/>.

"""

Garbles person names in the database so that it may be used for a demo.

"""

import os
import sys
#~ import datetime

#~ from dateutil import parser as dateparser

from django.conf import settings
#~ from django.core.management import call_command
#~ from django.db import IntegrityError
#~ from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

#~ from lino import lino_site
#~ from lino.utils import dbfreader
from lino.utils import dblogger
from lino.utils import Cycler
#~ from lino import diag

#~ from lino.modlib.contacts.utils import name2kw, street2kw
#~ from lino.utils import join_words
from lino.utils.choicelists import Gender

from lino import dd
#~ from lino.tools import is_valid_email
#~ import lino

from lino.utils import confirm

#~ print 'Loading demo names...'
#~ from lino.modlib.contacts.fixtures import demo_fr as demo
from lino.utils import demonames as demo

def last_names():
    yield demo.LAST_NAMES_BELGIUM
    yield demo.LAST_NAMES_MUSLIM
    yield demo.LAST_NAMES_BELGIUM
    yield demo.LAST_NAMES_RUSSIA
    yield demo.LAST_NAMES_BELGIUM
    yield demo.LAST_NAMES_AFRICAN
LAST_NAMES = Cycler(last_names())
    
def male_first_names():
    yield demo.MALE_FIRST_NAMES_FRANCE
    yield demo.MALE_FIRST_NAMES_MUSLIM
    yield demo.MALE_FIRST_NAMES_FRANCE
    yield demo.MALE_FIRST_NAMES_RUSSIA
    yield demo.MALE_FIRST_NAMES_FRANCE
    yield demo.MALE_FIRST_NAMES_AFRICAN
MALES = Cycler(male_first_names())
    
def female_first_names():
    yield demo.FEMALE_FIRST_NAMES_FRANCE
    yield demo.FEMALE_FIRST_NAMES_MUSLIM
    yield demo.FEMALE_FIRST_NAMES_FRANCE
    yield demo.FEMALE_FIRST_NAMES_RUSSIA
    yield demo.FEMALE_FIRST_NAMES_FRANCE
    yield demo.FEMALE_FIRST_NAMES_AFRICAN
FEMALES = Cycler(female_first_names())

NATIONALITIES = Cycler('BE','MA','BE','RU','BE','CD')

#~ print 'Done'

      
REQUEST = dblogger.PseudoRequest('garble')

class Command(BaseCommand):
    args = '(no arguments)'
    help = 'Garbles person names in the database so that it may be used for a demo.'

    def handle(self, *args, **options):
            
        dbname = settings.DATABASES['default']['NAME']
        if not confirm("This is going to GARBLE your database (%s).\nAre you sure (y/n) ?" % dbname):
            raise CommandError("User abort.")
            
        User = dd.resolve_model(settings.LINO.user_model)
        Person = dd.resolve_model(settings.LINO.person_model)
        Country = dd.resolve_model('countries.Country')
        
        for p in Person.objects.all():
            if User.objects.filter(partner=p).count() > 0:
                # users keep their original name
                pass
            else:
                p.nationality = Country.objects.get(isocode=NATIONALITIES.pop())
                p.last_name = LAST_NAMES.pop()
                if p.gender == Gender.male:
                    p.first_name = MALES.pop()
                    FEMALES.pop()
                else:
                    p.first_name = FEMALES.pop()
                    MALES.pop()
                #~ dblogger.log_changes(REQUEST,p)
                #~ p.full_clean()
                p.save()
                dblogger.info("%s from %s",unicode(p),unicode(p.nationality))
            
        dblogger.info("GARBLE done on database %s." % dbname)
