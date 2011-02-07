## Copyright 2009-2011 Luc Saffre
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

import lino

from lino.demos.std.settings import *

from lino.utils.jsgen import js_code

class DsbeSite(LinoSite):
  
    title = "Another Lino/DSBE site"
    domain = "dsbe.saffre-rumma.net"
    help_url = "http://lino.saffre-rumma.net/dsbe/index.html"
    
    residence_permit_upload_type = None
    work_permit_upload_type = None
    driving_licence_upload_type = None 
    
    def init_site_config(self,sc):
        super(DsbeSite,self).init_site_config(sc)
        #~ print 20100908, "lino_settings.py init_site_config"
        sc.next_partner_id = 200000

    def configure(self,sc):
        super(DsbeSite,self).configure(sc)
        
    def setup_main_menu(self):
  
        from django.utils.translation import ugettext_lazy as _
        from lino.utils import perms

        from lino import models as system
        from lino.modlib.dsbe import models as dsbe

        m = self.add_menu("contacts",_("~Contacts"))
        m.add_action('contacts.Companies')
        m.add_action('contacts.Persons')
        m.add_action('dsbe.MySearches')

        m = self.add_menu("my",_("~My menu"),can_view=perms.is_authenticated)
        #~ m.add_action('projects.Projects')
        m.add_action('notes.MyNotes')
        m.add_action('uploads.MyUploads')
        m.add_action('dsbe.MyContracts')
        m.add_action('contacts.MyPersons')
        for pg in dsbe.PersonGroup.objects.all():
            m.add_action('contacts.MyPersonsByGroup',label=pg.name,
                params=dict(master_instance=pg))
            #~ m.add_action('contacts.MyPersonsByGroup',label=pg.name,
            #~ params=dict(master_id=pg.pk))
            #~ m.add_request_action(contacts.MyPersonsByGroup().request(master_instance=pg),label=pg.name)

        m = self.add_menu("courses",_("~Courses"),can_view=perms.is_authenticated)
        m.add_action('dsbe.Courses')
        m.add_action('contacts.CourseProviders')
        m.add_action('dsbe.CourseContents')
        m.add_action('dsbe.CourseEndings')
        
        sitemenu = system.add_site_menu(self)
        
        m = sitemenu.add_menu("config",_("~Configure"),can_view=perms.is_authenticated)
        mm = m.add_menu("manager",_("~Manager"),can_view=perms.is_authenticated)
        ma = m.add_menu("admin",_("Local Site ~Administrator"),can_view=perms.is_staff)
        me = m.add_menu("expert",_("~Expert"),can_view=perms.is_staff)
        
        #~ m.add_action('projects.ProjectTypes')
        ma.add_action('notes.NoteTypes')
        ma.add_action('dsbe.ContractTypes')
        mm.add_action('dsbe.PersonGroups')
        ma.add_action('contacts.CompanyTypes')
        ma.add_action('contacts.ContactTypes')
        
        from lino.modlib.properties import models as properties
        
        me.add_action('properties.PropGroups')
        me.add_action('properties.PropTypes')
        for pg in properties.PropGroup.objects.all():
            #~ mm.add_request_action(properties.PropsByGroup().request(master_instance=pg),label=pg.name)
            mm.add_action('properties.PropsByGroup',params=dict(master_instance=pg),label=pg.name)
        
        ma.add_action('properties.PropsByGroup')
        #~ ma.add_action('dsbe.Skills1')
        #~ ma.add_action('dsbe.Skills2')
        #~ ma.add_action('dsbe.Skills3')
        me.add_action('countries.Languages')
        mm.add_action('countries.Countries')
        mm.add_action('countries.Cities')
        me.add_action('auth.Permissions')
        ma.add_action('auth.Users')
        me.add_action('auth.Groups')
        #~ m.add_action('dsbe.DrivingLicenses')
        mm.add_action('dsbe.StudyTypes')
        #~ m.add_action('dsbe.StudyContents')
        mm.add_action('dsbe.Activities')
        mm.add_action('dsbe.ExclusionTypes')
        mm.add_action('dsbe.AidTypes')
        mm.add_action('dsbe.ContractEndings')
        #~ m.add_action('dsbe.JobTypes')
        mm.add_action('dsbe.ExamPolicies')
        #~ m.add_action('dsbe.CoachingTypes')
        mm.add_action('links.LinkTypes')
        mm.add_action('uploads.UploadTypes')
        m.add_action('properties.Properties')

        m = sitemenu.add_menu("explorer",_("E~xplorer"),
          can_view=perms.is_staff)
        #m.add_action('properties.PropChoices')
        #~ m.add_action('properties.PropValues')
        m.add_action('notes.Notes')
        m.add_action('links.Links')
        m.add_action('dsbe.Exclusions')
        m.add_action('dsbe.Contracts')
        m.add_action('uploads.Uploads')
        m.add_action('dsbe.CourseRequests')
        m.add_action('contenttypes.ContentTypes')
        m.add_action('dsbe.PersonSearches')

        
        m = self.add_menu("help",_("~Help"))
        m.add_item('userman',_("~User Manual"),
            href='http://lino.saffre-rumma.net/dsbe/index.html')

        #~ m.add_item('home',_("~Home"),href='/')
        #~ self._menu.add_item('home',_("~Home"),href='/')
        #~ self._menu.items.append(dict(text=_("~Home"),href='/'))
        #~ self._menu.items.append(dict(xtype='menuseparator'))
        self._menu.items.append(dict(xtype='button',text=_("Home"),handler=js_code("function() {window.location='/';}")))
        #~ self._menu.items.append(dict(xtype='menuitem',html='<a href="/">%s</a>' % _("~Home")))


LINO_SITE = DsbeSite()


PROJECT_DIR = abspath(dirname(__file__))
DATA_DIR = join(PROJECT_DIR,"data")
#~ LINO_SETTINGS = join(PROJECT_DIR,"lino_settings.py")

MEDIA_ROOT = join(PROJECT_DIR,'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(DATA_DIR,'dsbe_demo.db')
        #~ 'NAME': ':memory:'
    }
}


TIME_ZONE = 'Europe/Brussels'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-BE'
#~ LANGUAGE_CODE = 'fr-BE'

#~ ROOT_URLCONF = 'lino.demos.dsbe.urls'

SITE_ID = 1 # see also fill.py

INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  #~ 'django.contrib.markup',
  #~ 'lino.modlib.system',
  'lino',
  'lino.modlib.countries',
  #~ 'lino.modlib.documents',
  'lino.modlib.properties',
  'lino.modlib.contacts',
  #~ 'lino.modlib.projects',
  'lino.modlib.notes',
  'lino.modlib.links',
  'lino.modlib.uploads',
  #'dsbe.modlib.contacts',
  #'dsbe.modlib.projects',
  'lino.modlib.dsbe',
  #~ 'south', # http://south.aeracode.org
)

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (
      join(abspath(DATA_DIR),'templates'),
      join(abspath(PROJECT_DIR),'templates'),
      join(abspath(dirname(lino.__file__)),'templates'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cqt^18t(Fb#14a@s%mbtdif+ih8fscpf8l9aw+0ivo2!3c(c%&'


#~ __all__ = [x for x in dir() if x[0].isupper()]

