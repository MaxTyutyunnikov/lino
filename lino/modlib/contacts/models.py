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
This module deserves more documentation.

It defines tables like `Person` and `Company`

"""

import logging
logger = logging.getLogger(__name__)


import datetime
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
#~ from django.utils.translation import ugettext

from django import forms
from django.utils import translation


import lino
#~ from lino import layouts

from lino import dd
#~ from lino import fields

from lino import mixins
from lino.utils import join_words
from lino.utils.choosers import chooser
from lino.utils import babel 
#~ from lino.models import get_site_config

from lino.modlib.contacts.utils import Gender

#~ from lino.modlib.countries.models import CountryCity
from lino.modlib.countries.models import CountryRegionCity

#~ from lino.modlib.contacts.utils import get_salutation
#~ from lino.modlib.contacts.utils import GENDER_CHOICES, get_salutation


from lino.utils import mti


def get_salutation(gender,nominative=False):
    """
    Returns "Mr" or "Mrs" or a translation thereof, 
    depending on the gender and the current babel language.
    
    Note that the English abbreviations 
    `Mr <http://en.wikipedia.org/wiki/Mr.>`_ and 
    `Mrs <http://en.wikipedia.org/wiki/Mrs.>`_
    are written either with (AE) or 
    without (BE) a dot. Since the babel module doesn't yet allow 
    to differentiate dialects, we opted for the british version.
    
    The optional keyword argument `nominative` used only when babel language
    is "de": specifying ``nominative=True`` will return "Herr" instead of default 
    "Herrn" for male persons.
    
    """
    if not gender: return ''
    if gender == Gender.female: return _("Mrs")
    from django.utils.translation import pgettext
    if nominative:
        return pgettext("nominative salutation","Mr") 
    return pgettext("indirect salutation","Mr") 
    




class CompanyType(babel.BabelNamed):
    """
    Represents a possible choice for the  `type`
    field of a :class:`Company`.
    """
    
    class Meta:
        verbose_name = _("company type")
        verbose_name_plural = _("company types")
        
    abbr = babel.BabelCharField(_("Abbreviation"),max_length=30,blank=True)
    
        
class CompanyTypes(dd.Table):
    required = dict(user_level='manager')
    model = 'contacts.CompanyType'
    column_names = 'name *'
    #~ label = _("Company types")




#~ class Contact(mti.MultiTableBase,CountryCity):
class Partner(mti.MultiTableBase,CountryRegionCity):
    """
    Base class for anything that has contact information 
    (postal address, email, phone,...).
    
    """
    
    """
    preferred width for ForeignKey fields to a Partner
    """
    _lino_preferred_width = 20 
    
  
    class Meta:
        abstract = settings.LINO.is_abstract_model('contacts.Partner')
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
  
    name = models.CharField(max_length=200,verbose_name=_('Name'))
    addr1 = models.CharField(_("Address line before street"),
        max_length=200,blank=True,
        help_text="Address line before street")
    
    street_prefix = models.CharField(_("Street prefix"),max_length=200,blank=True,
        help_text="Text to print before name of street, but to ignore for sorting.")
    
    street = models.CharField(_("Street"),max_length=200,blank=True,
        help_text="Name of street. Without house number.")
    
    street_no = models.CharField(_("No."),max_length=10,blank=True,
        help_text="House number")
    
    street_box = models.CharField(_("Box"),max_length=10,blank=True,
        help_text="Text to print after :attr:`steet_no` on the same line")
    
    addr2 = models.CharField(_("Address line after street"),
        max_length=200,blank=True,
        help_text="Address line to print below street line")
    
    #~ zip_code = models.CharField(_("Zip code"),
        #~ max_length=10,blank=True)
    #~ region = models.CharField(_("Region"),
        #~ max_length=200,blank=True)
    language = babel.LanguageField()
    
    email = models.EmailField(_('E-Mail'),blank=True) # ,null=True)
    url = models.URLField(_('URL'),blank=True)
    phone = models.CharField(_('Phone'),max_length=200,blank=True)
    gsm = models.CharField(_('GSM'),max_length=200,blank=True)
    fax = models.CharField(_('Fax'),max_length=200,blank=True)
    
    remarks = models.TextField(_("Remarks"),blank=True) # ,null=True)
    
    is_person = mti.EnableChild(
        settings.LINO.person_model,
        verbose_name=_("is Person"),
        help_text=_("Whether this Partner is a Person."))
        
    is_company = mti.EnableChild(
        settings.LINO.company_model,
        verbose_name=_("is Company"),
        help_text=_("Whether this Partner is a Company."))
        
    def save(self,*args,**kw):
        if self.id is None:
            sc = settings.LINO.site_config # get_site_config()
            if sc.next_partner_id is not None:
                self.id = sc.next_partner_id
                sc.next_partner_id += 1
                sc.save()
        #~ logger.info("20120327 Partner.save(%s,%s)",args,kw)
        super(Partner,self).save(*args,**kw)
        
    def __unicode__(self):
        return self.name
        
    def address_person_lines(self):
        #~ yield self.name
        yield self.get_full_name()
        
    def get_full_name(self,*args,**kw):
        """\
Returns a one-line string representing this Partner.
The default returns simply the `name` field, ignoring any parameters, 
but e.g. :class:`PersonMixin` overrides this.
        """
        #~ print '20120729 Partner.get_full_name`'
        
        #~ try:
            #~ p = getattr(self,'person')
            #~ return p.get_full_name(*args,**kw)
        #~ except ObjectDoesNotExist:
            #~ pass
        return self.name
    full_name = property(get_full_name)
        
        
    def address_location_lines(self):
        #~ lines = []
        #~ lines = [self.name]
        if self.addr1:
            yield self.addr1
        if self.street:
            yield join_words(
              self.street_prefix, self.street,
              self.street_no,self.street_box)
        if self.addr2:
            yield self.addr2
        #lines = [self.name,street,self.addr1,self.addr2]
        if self.region: # format used in Estonia
            if self.city:
                yield unicode(self.city)
            s = join_words(self.zip_code,self.region)
        else: 
            s = join_words(self.zip_code,self.city)
        if s:
            yield s 
        #~ foreigner = True # False
        #~ if self.id == 1:
            #~ foreigner = False
        #~ else:
            #~ foreigner = (self.country != self.objects.get(pk=1).country)
        if self.country is not None:
            sc = settings.LINO.site_config # get_site_config()
            if not sc.site_company or self.country != sc.site_company.country: 
                # (if self.country != sender's country)
                yield unicode(self.country)
            
        #~ logger.debug('%s : as_address() -> %r',self,lines)
        
    def address_lines(self):
        for ln in self.address_person_lines() : yield ln
        for ln in self.address_location_lines() : yield ln
          
    #~ def address(self,linesep="\n<br/>"):
    def address(self,linesep="\n"):
        """
        The plain text full postal address (person and location). 
        Lines are separated by `linesep`.
        """
        #~ return linesep.join(self.address_lines())
        return linesep.join(list(self.address_person_lines()) + list(self.address_location_lines()))
    address.return_type = models.TextField(_("Address"))
    
    def address_location(self,linesep="\n"):
        """
        The plain text postal address location part. 
        Lines are separated by `linesep`.
        """
        return linesep.join(self.address_location_lines())
        
    @dd.displayfield(_("Address"))
    def address_column(self,request):
        return self.address_location(', ')
    #~ address_column.return_type = dd.DisplayField(_("Address"))
    
    @dd.displayfield(_("Name"))
    def name_column(self,request):
        #~ return join_words(self.last_name.upper(),self.first_name)
        return unicode(self)
    

class PartnerDetail(dd.FormLayout):
  
    main = """
    address_box:60 contact_box:30
    bottom_box
    """
    
    address_box = dd.Panel("""
    name_box
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """,label = _("Address"))
    
    contact_box = dd.Panel("""
    info_box
    email:40 
    url
    phone
    gsm fax
    """,label = _("Contact"))

    bottom_box = """
    remarks 
    is_person is_company #is_user
    """
        
    name_box = "name"
    info_box = "id language"
    
    
    #~ def setup_handle(self,dh):
        #~ dh.address_box.label = _("Address")
        #~ dh.contact_box.label = _("Contact")
  
    
    
class Partners(dd.Table):
    model = 'contacts.Partner'
    column_names = "name email * id" 
    order_by = ['name','id']
    #~ column_names = "name * id" 
    detail_layout = PartnerDetail()
    insert_layout = dd.FormLayout("""
    name
    language email
    """,window_size=(40,'auto'))
    
    @classmethod
    def get_queryset(self):
        return self.model.objects.select_related('country','city')


#~ class AllPartners(Partners):
  
    #~ @classmethod
    #~ def get_actor_label(self):
        #~ return _("All %s") % self.model._meta.verbose_name_plural
        
class PartnersByCity(Partners):
    master_key = 'city'
    order_by = 'street street_no street_box addr2'.split()
    column_names = "street street_no street_box addr2 name language *"
    
class PartnersByCountry(Partners):
    master_key = 'country'
    column_names = "city street street_no name language *"
    order_by = "city street street_no".split()



class Born(dd.Model):
    """
    Abstract base class that adds a `birth_date` 
    field and a virtual field "Age".
    """
    class Meta:
        abstract = True
        
    birth_date = dd.IncompleteDateField(
        blank=True,
        verbose_name=_("Birth date"),
        help_text = u"""\
Unkomplette Geburtsdaten sind erlaubt, z.B. 
<br>"00.00.1980" heißt "irgendwann im Jahr 1980", 
<br>"00.07.1980" heißt "im Juli 1980"
<br>oder"23.07.0000" heißt "Geburtstag am 23. Juli, Alter unbekannt".""")
        
    
    def get_age_years(self,today=None):
        if self.birth_date and self.birth_date.year:
            if today is None:
                today = datetime.date.today()
            try:
                return today - self.birth_date.as_date()
            except ValueError:
                pass
      
    @dd.displayfield(_("Age"))
    def age(self,request,today=None):
        a = self.get_age_years(today)
        if a is None:
            return unicode(_('unknown'))
        s = _("%d years") % (a.days / 365)
        if self.birth_date and self.birth_date.is_complete():
            return s
        return u"±" + s


        

class PersonMixin(dd.Model):
    """
    Can be used also for Persons that are no Partners
    """
    class Meta:
        abstract = True
        
    first_name = models.CharField(max_length=200,
      #~ blank=True,
      verbose_name=_('First name'))
    "Space-separated list of all first names."
    
    last_name = models.CharField(max_length=200,
      #~ blank=True,
      verbose_name=_('Last name'))
    """Last name (family name)."""
    
    title = models.CharField(max_length=200,blank=True,
      verbose_name=_('Title'))
    """Text to print as part of the first address line in front of first_name."""
        
    gender = Gender.field(blank=True)
        
    def get_salutation(self,**salutation_options):
        return get_salutation(
            #~ translation.get_language(),
            self.gender,**salutation_options)
    
        
    def get_full_name(self,salutation=True,**salutation_options):
        """Returns a one-line string composed of salutation, first_name and last_name.
        
The optional keyword argument `salutation` can be set to `False` 
to suppress salutations. 
See :func:`lino.apps.pcsw.tests.pcsw_tests.test04` 
and
:func:`lino.modlib.contacts.tests.test01` 
for some examples.

Optional `salutation_options` see :func:`get_salutation`.
        """
        #~ print '20120729 PersonMixin.get_full_name`'
        #~ return '%s %s' % (self.first_name, self.last_name.upper())
        words = []
        if salutation:
            words.append(self.get_salutation(**salutation_options))
        words += [self.first_name, self.last_name.upper()]
        return join_words(*words)
    full_name = property(get_full_name)
    #~ full_name.return_type = models.CharField(max_length=200,verbose_name=_('Full name'))
    
  
class Person(PersonMixin,Partner):
    """
    Mixin for models that represent a physical person. 
    """
    class Meta:
        #~ abstract = True
        abstract = settings.LINO.is_abstract_model('contacts.Person')
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    def address_person_lines(self,*args,**kw):
        "Deserves more documentation."
        if self.title:
            yield self.title
        yield self.get_full_name(*args,**kw)
        #~ l = filter(lambda x:x,[self.first_name,self.last_name])
        #~ yield  " ".join(l)
        
    def full_clean(self,*args,**kw):
        """
        Set the :attr:`Partner.name` field of this person. 
        This field is visible in the Partner's detail but not 
        in the Person's detail and serves for sorting 
        when selecting a Partner. 
        It also serves for quick search on Persons.
        """
        #~ l = filter(lambda x:x,[self.last_name,self.first_name])
        #~ self.name = " ".join(l)
        self.name = join_words(self.last_name,self.first_name)
        super(Person,self).full_clean(*args,**kw)





class PersonDetail(PartnerDetail):
  
    #~ main = """
    #~ address_box contact_box
    #~ bottom_box contacts.RolesByPerson
    #~ """
    
    name_box = "last_name first_name:15 gender title:10"
    #~ info_box = "id:5 language:10 birth_date:10"
    info_box = "id:5 language:10"

    bottom_box = "remarks contacts.RolesByPerson"
        
    
    #~ def setup_handle(self,dh):
        #~ PartnerDetail.setup_handle(self,dh)
        #~ dh.address_box.label = _("Address")
        #~ dh.contact_box.label = _("Contact")
  


class Persons(dd.Table):
    """
    List of all Persons.
    """
    model = settings.LINO.person_model
    order_by = ["last_name","first_name","id"]
    column_names = "name_column:20 address_column email phone:10 gsm:10 id language:10 *"
    detail_layout = PersonDetail()
    
    insert_layout = dd.FormLayout("""
    title first_name last_name
    gender language
    """,window_size=(60,'auto'))
    


#~ class CompanyMixin(dd.Model):
class Company(Partner):
    """
    Abstract base class for a company.
    See also :doc:`/tickets/14`.
    """
    class Meta:
        abstract = settings.LINO.is_abstract_model('contacts.Company')
        #~ abstract = True
        app_label = 'contacts'
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
    
    prefix = models.CharField(max_length=200,blank=True) 
    vat_id = models.CharField(_("VAT id"),max_length=200,blank=True)
    """The national VAT identification number.
    """
    
    type = models.ForeignKey('contacts.CompanyType',blank=True,null=True,
      verbose_name=_("Company type"))
    """Pointer to this company's :class:`CompanyType`. 
    """
    
    #~ def get_full_name(self,**salutation_options):
    def get_full_name(self,salutation=True,**salutation_options):
        """Deserves more documentation."""
        #~ print '20120729 Company.get_full_name`'
        if self.type:
            return join_words(self.type.abbr,self.name)
        return self.name
    full_name = property(get_full_name)
    
    #~ @classmethod
    #~ def site_setup(cls,lino):
        #~ raise Exception('20110810')


class CompanyDetail(PartnerDetail):
  
    bottom_box = "remarks contacts.RolesByCompany"

    name_box = """prefix name type:20"""
    info_box = "id:5 language:10 vat_id:12"



class Companies(Partners):
    model = settings.LINO.company_model
    order_by = ["name"]
    detail_layout = CompanyDetail()
    insert_layout = dd.FormLayout("""
    name 
    language:20 email:40
    type id
    """,window_size=(60,'auto'))
    
#~ class List(Partner):
    #~ pass

#~ class Lists(Partners):
    #~ model = List
    #~ order_by = ["name"]
    #~ detail_layout = """
    #~ id name
    #~ language email
    #~ MembersByList
    #~ """
    #~ insert_layout = dd.FormLayout("""
    #~ name 
    #~ language email
    #~ """,window_size=(40,'auto'))



# class ContactType(babel.BabelNamed):
class RoleType(babel.BabelNamed):
    """
    TODO: rename "RoleType" to "Function".
    """
    class Meta:
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")


class RoleTypes(dd.Table):
    required = dict(user_level='manager')
    model = RoleType


#~ class Contact(dd.Model):
class Role(dd.Model):
    """
    Represents a given :class:`Person` having a given Function 
    in a given :class:`Company`.
    TODO: rename "Role" to "Contact".
    """
  
    class Meta:
        verbose_name = _("Contact Person")
        verbose_name_plural = _("Contact Persons")
        
    type = models.ForeignKey('contacts.RoleType',
      blank=True,null=True,
      verbose_name=_("Contact Role"))
    person = models.ForeignKey(settings.LINO.person_model,related_name='rolesbyperson')
    company = models.ForeignKey(settings.LINO.company_model,related_name='rolesbycompany')
    #~ type = models.ForeignKey('contacts.ContactType',blank=True,null=True,
      #~ verbose_name=_("contact type"))

    #~ def __unicode__(self):
        #~ if self.person_id is None:
            #~ return super(Contact,self).__unicode__()
        #~ if self.type is None:
            #~ return unicode(self.person)
        #~ return u"%s (%s)" % (self.person, self.type)
    def __unicode__(self):
        if self.person_id is None:
            return super(Role,self).__unicode__()
        if self.type is None:
            return unicode(self.person)
        return u"%s (%s)" % (self.person, self.type)
            
    #~ def address_lines(self):
        #~ for ln in self.person.address_person_lines():
            #~ yield ln
        #~ if self.company:
            #~ for ln in self.company.address_person_lines():
                #~ yield ln
            #~ for ln in self.company.address_location_lines():
                #~ yield ln
        #~ else:
            #~ for ln in self.person.address_location_lines():
                #~ yield ln
    def address_lines(self):
        for ln in self.person.address_person_lines():
            yield ln
        if self.company:
            for ln in self.company.address_person_lines():
                yield ln
            for ln in self.company.address_location_lines():
                yield ln
        else:
            for ln in self.person.address_location_lines():
                yield ln

#~ class ContactsByCompany(dd.Table):
    #~ model = 'contacts.RoleOccurence'
    #~ master_key = 'company'
    #~ column_names = 'person type *'

#~ class ContactsByPerson(dd.Table):
    #~ label = _("Contact for")
    #~ model = 'contacts.RoleOccurence'
    #~ master_key = 'person'
    #~ column_names = 'company type *'
    
class Roles(dd.Table):
    required = dict(user_level='manager')
    #~ required_user_level = UserLevels.manager
    model = 'contacts.Role'   
    
class RolesByCompany(Roles):
    required = dict()
    #~ required_user_level = None
    label = _("Contact persons")
    master_key = 'company'
    column_names = 'person type *'

class RolesByPerson(Roles):
    required = dict()
    #~ required_user_level = None
    label = _("Contact for")
    master_key = 'person'
    column_names = 'company type *'
    
    
    
class PartnerDocument(dd.Model):
    """
    Adds two fields 'partner' and 'person' to this model, 
    making it something that refers to a "partner". 
    `person` means a "contact person" for the partner.
    
    """
    
    class Meta:
        abstract = True
        
    company = models.ForeignKey(settings.LINO.company_model,
        blank=True,null=True)
        
    person = models.ForeignKey(settings.LINO.person_model,
        blank=True,null=True)
        
    def get_partner(self):
        if self.company is not None:
            return self.company
        return self.person
        
    def get_mailable_recipients(self):
        for p in self.company, self.person:
            if p is not None and p.email:
                #~ yield "%s <%s>" % (p, p.email)
                yield ('to', p)
                #~ yield ('to', unicode(p), p.email)
        
    def get_postable_recipients(self):
        for p in self.company, self.person:
            if p is not None:
                yield p
        
        
    #~ def summary_row(self,ui,rr,**kw):
        #~ if self.person:
            #~ if self.company:
                #~ # s += ": " + ui.href_to(self.person) + " / " + ui.href_to(self.company)
                #~ return ui.href_to(self.company) + ' ' + ugettext("attn:") + ' ' + ui.href_to(self.person)
            #~ else:
                #~ return ui.href_to(self.person)
        #~ elif self.company:
            #~ return ui.href_to(self.company)
            
    #~ def summary_row(self,ui,rr,**kw):
    def summary_row(self,ar,**kw):
        """
        A :modmeth:`summary_row` method for partner documents.
        """
        href_to = ar.href_to
        #~ href_to = ui.ext_renderer.href_to
        s = href_to(self)
        #~ if self.person and not dd.has_fk(rr,'person'):
        if self.person:
            if self.company:
                s += " (" + href_to(self.person) \
                    + "/" + href_to(self.company) + ")"
            else:
                s += " (" + href_to(self.person) + ")"
        elif self.company:
            s += " (" + href_to(self.company) + ")"
        return s
            
    def update_owned_instance(self,other):
        #~ print '20120627 PartnerDocument.update_owned_instance'
        if isinstance(other,mixins.ProjectRelated):
            # the following hack doesn't work when loading data by dumpy
            # because LINO.person_model are still strings at that moment
            if isinstance(self.person,settings.LINO.person_model):
                other.project = self.person
            elif isinstance(self.company,settings.LINO.person_model):
                other.project = self.company
        other.person = self.person
        other.company = self.company
        super(PartnerDocument,self).update_owned_instance(other)
        



class OldCompanyContact(dd.Model):
    """
    Abstract class which adds two fields `company` and `contact`.
    """
    class Meta:
        abstract = True
        
    company = models.ForeignKey(settings.LINO.company_model,
        related_name="%(app_label)s_%(class)s_set_by_company",
        verbose_name=_("Company"),
        blank=True,null=True)
        
    contact = models.ForeignKey("contacts.Role",
      related_name="%(app_label)s_%(class)s_set_by_contact",
      blank=True,null=True,
      verbose_name=_("represented by"))
      
    @chooser()
    def contact_choices(cls,company):
        if company is not None:
            return cls.contact_choices_queryset(company)
        return []
        
    @classmethod
    def contact_choices_queryset(cls,company):
        return Role.objects.filter(company=company)

    def full_clean(self,*args,**kw):
        if self.company:
            if self.contact is None \
              or self.contact.company is None \
              or self.contact.company.pk != self.company.pk:
                qs = self.contact_choices_queryset(self.company)
                #~ qs = self.company.rolesbyparent.all()
                if qs.count() == 1:
                    self.contact = qs[0]
                else:
                    #~ print "20120227 clear contact!"
                    self.contact = None
        super(CompanyContact,self).full_clean(*args,**kw)


class ContactRelated(dd.Model):
    """
    Abstract class for things that relate to a company represented by a person as a given role.
    Adds 3 fields `company`, `contact_person` and `contact_role`.
    """
    class Meta:
        abstract = True
        
    company = models.ForeignKey(settings.LINO.company_model,
        related_name="%(app_label)s_%(class)s_set_by_company",
        verbose_name=_("Company"),
        blank=True,null=True)
        
    contact_person = models.ForeignKey("contacts.Person",
      related_name="%(app_label)s_%(class)s_set_by_contact_person",
      blank=True,null=True,
      verbose_name=_("represented by"))
      
    contact_role = models.ForeignKey("contacts.RoleType",
      related_name="%(app_label)s_%(class)s_set_by_contact_role",
      blank=True,null=True,
      verbose_name=_("represented as"))
      
    @chooser()
    def contact_person_choices(cls,company):
        if company is not None:
            return cls.contact_person_choices_queryset(company)
        return []
        
    def get_contact(self):
        roles = Role.objects.filter(company=self.company,person=self.contact_person)
        #~ print '20120929 get_contact', roles
        if roles.count() == 1:
            return roles[0]
        
    def contact_person_changed(self,ar):
        #~ print '20120929 contact_person_changed'
        if self.company and not self.contact_person_id:
            roles = Role.objects.filter(company=self.company)
            if roles.count() == 1:
                self.contact_person = roles[0].person
                self.contact_role = roles[0].type
            return 
      
    @classmethod
    def contact_person_choices_queryset(cls,company):
    #~ def contact_choices_queryset(cls,company):
        return settings.LINO.person_model.objects.filter(rolesbyperson__company=company).distinct()

    def full_clean(self,*args,**kw):
        if not settings.LINO.loading_from_dump:
            if self.company and self.contact_person is None:
                qs = self.contact_person_choices_queryset(self.company)
                #~ qs = self.company.rolesbyparent.all()
                if qs.count() == 1:
                    self.contact_person = qs[0]
                else:
                    #~ print "20120227 clear contact!"
                    self.contact = None
            contact = self.get_contact()
            if contact is not None:
                self.contact_role = contact.type
                #~ print '20120929b', contact.type
        super(ContactRelated,self).full_clean(*args,**kw)


    


#~ if settings.LINO.is_installed('contacts'):
  
    #~ """
    #~ Don't inject fields if contacts is just being imported from some other module.
    #~ """
    
#~ dd.inject_field(settings.LINO.user_model,
    #~ 'partner',
    #~ models.ForeignKey(Partner,
        #~ blank=True,null=True,
        #~ verbose_name=_("Partner")))



from lino.models import SiteConfig

dd.inject_field(SiteConfig,
    'next_partner_id',
    models.IntegerField(default=100, # first 100 for users from demo fixtures.
        verbose_name=_("The next automatic id for Person or Company")
    ),"""The next automatic id for Person or Company. 
    Deserves more documentation.
    """)
    
dd.inject_field(SiteConfig,
    'site_company',
    models.ForeignKey(settings.LINO.company_model,
        blank=True,null=True,
        verbose_name=_("The company that runs this site"),
        related_name='site_company_sites',
        help_text=_("The Company to be used as sender in documents.")))
    

#~ dd.inject_field(Partner,
    #~ 'is_person',
    #~ mti.EnableChild(
        #~ settings.LINO.person_model,
        #~ verbose_name=_("is Person"),
        #~ help_text=_("Whether this Partner is a Person.")))
#~ dd.inject_field(Partner,
    #~ 'is_company',
    #~ mti.EnableChild(
        #~ settings.LINO.company_model,
        #~ verbose_name=_("is Company"),
        #~ help_text=_("Whether this Partner is a Company.")))


MODULE_LABEL = _("Contacts")

def site_setup(site):
    site.modules.countries.Cities.set_detail_layout("""
    name country 
    parent type id
    CitiesByCity
    contacts.PartnersByCity
    """)
    


def setup_main_menu(site,ui,user,m):
    m = m.add_menu("contacts",MODULE_LABEL)
    #~ actors = (Persons,Companies,Partners)
    #~ for m in (Person,Company,Partner):
        #~ if m._meta.abstract: 
            #~ return 
    """
    We use the string representations and not the classes because 
    other installed applications may want to override these tables.
    """
    #~ for a in (Persons,Companies,Partners):
    for a in ('contacts.Persons','contacts.Companies','contacts.Partners'):
        m.add_action(a)

def setup_my_menu(site,ui,user,m): 
    pass
  
def setup_master_menu(site,ui,user,m): 
    pass
    
def setup_config_menu(site,ui,user,m): 
    config_contacts = m.add_menu("contacts",MODULE_LABEL)
    config_contacts.add_action(CompanyTypes)
    config_contacts.add_action(RoleTypes)
    config_contacts.add_action(site.modules.countries.Countries)
    config_contacts.add_action(site.modules.countries.Cities)
    config_contacts.add_action(site.modules.countries.Languages)
            
    #~ m  = m.add_menu("contacts",_("~Contacts"))
    #~ m.add_action('contacts.RoleTypes')
  
def setup_explorer_menu(site,ui,user,m):
    m = m.add_menu("contacts",MODULE_LABEL)
    m.add_action(site.modules.contacts.Roles)
    m.add_action(site.modules.countries.Cities)
  
#~ def setup_quicklinks(site,ui,user,m):
    #~ m.add_action(Person.detail_action)
        
  