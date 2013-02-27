# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Default settings module for a :mod:`lino.projects.cosi` project.
"""
      
from __future__ import unicode_literals

from os.path import join, abspath, dirname

from lino.projects.std.settings import *

from django.utils.translation import ugettext_lazy as _

class Lino(Lino):
  
    #~ title = __name__
    short_name = "Lino Così"
    #~ short_name = "Lino Cosi"
    description = _("a Lino application to make Belgian accounting simple.")
    version = "0.1"
    url = "http://www.lino-framework.org/autodoc/lino.projects.cosi"
    author = 'Luc Saffre'
    author_email = 'luc.saffre@gmail.com'
    
    demo_fixtures = 'std few_countries few_cities few_languages demo demo2 userman'.split()
    
    languages = ['en','de','fr']
    #~ languages = 'de fr et en'.split()
    
    #~ project_model = 'tickets.Project'
    user_model = 'users.User'
    
    #~ remote_user_header = "REMOTE_USER"
    
    #~ override_modlib_models = [ 'contacts.Partner' ]
    #~ override_modlib_models = [
      #~ 'contacts.Person','contacts.Company',
      #~ 'households.Household']
    
    #~ def get_description(self):
        #~ from django.utils.translation import ugettext_lazy as _
        #~ from django.utils.translation import string_concat
        #~ return _("a Lino application to make Belgian accounting simple.")
    #~ description = property(get_description)
        
    #~ def get_app_source_file(self): return __file__
      
    #~ def get_application_info(self):
        #~ return (__name__,__version__,__url__)
      
    def get_main_action(self,user):
        return self.modules.ui.Home.default_action
        
    #~ def setup_quicklinks(self,ui,user,tb):
        #~ tb.add_action(self.modules.contacts.Persons.detail_action)
        
    def setup_choicelists(self):
        """
        Defines application-specific default user profiles.
        Local site administrators can override this in their :xfile:.
        """
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office accounting')
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"),       '_ _ _', 'anonymous',readonly=True,authenticated=False)
        add('100', _("User"),            'U U U', 'user')
        add('900', _("Administrator"),   'A A A', 'admin')
        
            
    def get_installed_apps(self):
        for a in super(Lino,self).get_installed_apps():
            yield a
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.users'
        #~ yield 'django.contrib.auth'
        yield 'lino.modlib.countries'
        #~ yield 'lino.modlib.properties'
        #~ yield 'lino.modlib.partners'
        yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.households'
        yield 'lino.modlib.products'
        yield 'lino.modlib.accounts'
        yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        yield 'lino.modlib.declarations'
        #~ 'lino.modlib.journals',
        yield 'lino.modlib.sales'
        yield 'lino.modlib.finan'
        #~ 'lino.modlib.projects',
        #~ yield 'lino.modlib.blogs'
        #~ yield 'lino.modlib.tickets'
        #~ 'lino.modlib.links',
        #~ yield 'lino.modlib.uploads'
        #~ 'lino.modlib.thirds',
        #~ yield 'lino.modlib.cal'
        #~ yield 'lino.modlib.outbox'
        #~ yield 'lino.modlib.postings'
        yield 'lino.modlib.pages'
        yield 'lino.projects.cosi'


LINO = Lino(__file__,globals()) 

