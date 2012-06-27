# -*- coding: UTF-8 -*-
## Copyright 2008-2012 Luc Saffre
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
"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


#~ import lino
#~ logger.debug(__file__+' : started')

from lino import dd
from lino.utils import perms
from lino import mixins
from lino.modlib.contacts import models as contacts
from lino.modlib.cal.models import DurationUnits, update_reminder

class UploadType(dd.Model):
    
    class Meta:
        verbose_name = _("Upload Type")
        verbose_name_plural = _("Upload Types")
        
    name = models.CharField(max_length=200,verbose_name=_('Name'))
    
    def __unicode__(self):
        return self.name
        
class UploadTypes(dd.Table):
    model = 'uploads.UploadType'
    column_names = "name *"
    order_by = ["name"]
    
        
class Upload(
    mixins.Uploadable,
    #~ contacts.PartnerDocument,
    #~ mixins.Reminder, 
    mixins.AutoUser,
    mixins.CreatedModified,
    mixins.Controllable):
    
    allow_cascaded_delete = True
    
    class Meta:
        verbose_name = _("Upload")
        verbose_name_plural = _("Uploads")
        
    type = models.ForeignKey("uploads.UploadType",
      blank=True,null=True)
      #~ verbose_name=_('upload type'))
      
    valid_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("valid until"))
        
    #~ owner_type = models.ForeignKey(ContentType,blank=True,null=True)
    #~ owner_id = models.PositiveIntegerField(blank=True,null=True)
    #~ owner = generic.GenericForeignKey('owner_type', 'owner_id')
    
    description = models.CharField(_("Description"),max_length=200,blank=True) # ,null=True)
    
    #~ def __unicode__(self):
        #~ return self.description or self.file.name

    def __unicode__(self):
        if self.description:
            s = self.description
        else:
            s = self.file.name
            i = s.rfind('/')
            if i != -1:
                s = s[i+1:]
        if self.type:
            s = unicode(self.type) + ' ' + s
        return s
        
    def save(self,*args,**kw):
        super(Upload,self).save(*args,**kw)
        self.update_reminders()
        
    def update_reminders(self):
        """
        Also called from :func:`lino.apps.pcsw.models.update_all_reminders`.
        """
        #~ logger.info("Upload.update_reminders() %s : owner is %s", self.pk, self.owner)
        
        update_reminder(1,self,self.user,
          self.valid_until,
          _("%s expires") % self.type,
          2,DurationUnits.months)
      
    #~ def update_owned_instance(self,task):
        #~ # logger.info("Upload.update_owned_instance() %s : owner is %s", self.pk, self.owner)
        #~ mixins.AutoUser.update_owned_instance(self,task)
        #~ mixins.Controllable.update_owned_instance(self,task)
          
        
class Uploads(dd.Table):
    model = Upload
    order_by = ["modified"]
    column_names = "file user created modified *"
    detail_template = """
    file user
    type description 
    # person company
    # reminder_date reminder_text delay_value delay_type reminder_done
    modified created owner
    # show_date show_time 
    # show_date time timestamp
    """
    
    
    

#~ class UploadsByPerson(Uploads):
    #~ master_key = 'person'
    #~ column_names = "file user company created modified"
    #~ show_slave_grid = False
    
#~ class UploadsByCompany(Uploads):
    #~ master_key = 'company'
    #~ column_names = "file user person created modified"
    #~ show_slave_grid = False
    
class UploadsByController(Uploads):
    master_key = 'owner'
    column_names = "file type description user * "
    slave_grid_format = 'summary'
    
    
class MyUploads(Uploads,mixins.ByUser):
    #~ column_names = "file user person company owner created modified"
    column_names = "file description user owner *"
    #~ label = _("My uploads")
    order_by = ["modified"]


MODULE_LABEL = _("Uploads")

def site_setup(site):
    pass
  
def setup_main_menu(site,ui,user,m):
    pass
            
  
def setup_master_menu(site,ui,user,m): 
    pass
  
def setup_my_menu(site,ui,user,m): 
    m  = m.add_menu("uploads",MODULE_LABEL)
    m.add_action(MyUploads)
    
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("uploads",MODULE_LABEL)
    m.add_action(UploadTypes)
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("uploads",MODULE_LABEL)
    m.add_action(Uploads)
