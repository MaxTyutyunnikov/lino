## Copyright 2013 Luc Saffre
## This file is part of the Lino project.

from django.db import models
from lino import dd
from django.utils.translation import ugettext_lazy as _

class Entry(dd.CreatedModified,dd.UserAuthored):
    
    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")
        
    
    subject = models.CharField(_("Subject"),blank=True,max_length=200)
    body = dd.RichTextField(_("Body"),blank=True)
    company = models.ForeignKey('contacts.Company')
    
class Entries(dd.Table):
    model = Entry    
    detail_layout = """
    id user created modified
    company
    subject
    body
    """
    insert_layout = """
    company
    subject
    """
    
class EntriesByCompany(Entries):
    master_key = 'company'
    
class MyEntries(Entries,dd.ByUser):
    pass
    

#~ @dd.receiver(dd.post_analyze)
#~ def my_permissions(sender,**kw):
    #~ 
    #~ self = sender
    #~ 
    #~ self.modules.contacts.Partners.required.pop('user_groups',None)
    #~ self.modules.contacts.Companies.required.pop('user_groups',None)
    #~ self.modules.contacts.Persons.required.pop('user_groups',None)
#~ 

@dd.receiver(dd.post_startup)
def my_change_watchers(sender,**kw):
    """
    This site watches the changes to Partner, Person, Company and Note
    """
    self = sender
    
    from lino.modlib.changes.models import watch_changes as wc
    
    """
    In our example we want to collect changes to Company and Entry 
    objects to their respective Partner.
    """
    wc(self.modules.contacts.Partner)
    wc(self.modules.contacts.Company,master_key='partner_ptr')
    wc(self.modules.watch_tutorial.Entry,master_key='company__partner_ptr')
                
    """
    add two application-specific panels, one to Partners, one to Companies:
    """
    self.modules.contacts.Partners.add_detail_tab('changes','changes.ChangesByMaster')
    self.modules.contacts.Companies.add_detail_tab('entries','watch_tutorial.EntriesByCompany')


def setup_main_menu(site,ui,profile,m):
    m = m.add_menu("entries",_("Entries"))
    m.add_action(MyEntries)
