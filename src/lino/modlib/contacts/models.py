## Copyright 2008-2009 Luc Saffre
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


import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils.safestring import mark_safe

#from lino.modlib.countries import models as countries
#countries = reports.get_app('countries')

from django import forms

from lino import reports
from lino import layouts
from lino.utils import perms


class Contact(models.Model):
  
    class Meta:
        abstract = True
        
    name = models.CharField(max_length=200,editable=False)
    national_id = models.CharField(max_length=200,blank=True)
    addr1 = models.CharField(max_length=200,blank=True)
    addr2 = models.CharField(max_length=200,blank=True)
    country = models.ForeignKey('countries.Country',blank=True,null=True)
    #city = models.ForeignKey("City",blank=True,null=True)
    city = models.CharField(max_length=200,blank=True)
    zip_code = models.CharField(max_length=10,blank=True)
    region = models.CharField(max_length=200,blank=True)
    language = models.ForeignKey('countries.Language',blank=True,null=True)
    
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    phone = models.CharField(max_length=200,blank=True)
    gsm = models.CharField(max_length=200,blank=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    remarks = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
        
    def as_address(self,linesep="\n<br/>"):
        l = filter(lambda x:x,[self.name,self.addr1,self.addr2])
        s = linesep.join(l)
        if self.city:
          s += linesep+self.city
        if self.zipCode:
          s += linesep+self.zipCode
          if self.region:
            s += " " + self.region
        elif self.region:
            s += linesep + self.region
        if self.id == 1:
            foreigner = False
        else:
            foreigner = (self.country != Contact.objects.get(id=1).country)
        if foreigner: # (if self.country != sender's country)
            s += linesep + unicode(self.country)
        return mark_safe(s)
    
class ContactPageLayout(layouts.PageLayout):
    
    box2 = """national_id:15
              language
              """
    box3 = """country region
              city zip_code:10
              addr1:40
              addr2
              """
    box4 = """email:40 
              url
              phone
              gsm
              """
    main = """box1 box2
              box3 box4
              remarks:60x6
              """
       
 

class Person(Contact):    
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200,blank=True)
    nationality = models.ForeignKey('countries.Country',
        blank=True,null=True,
        related_name='by_nationality')
        
    class Meta:
        abstract = True
        app_label = 'contacts'
    
    def save(self,*args,**kw):
        self.before_save()
        r = super(Contact,self).save(*args,**kw)
        return r
        
    def before_save(self):
        if True: # not self.name:
            l = filter(lambda x:x,[self.last_name,self.first_name,self.title])
            self.name = " ".join(l)

class PersonPageLayout(ContactPageLayout):
    box1 = "last_name first_name:15 title:10"
    box2 = """national_id:15 id
              nationality language
              """

class Persons(reports.Report):
    model = "contacts.Person"
    #label = "Personen"
    page_layouts = (PersonPageLayout,)
    columnNames = "first_name last_name title country id name"
    can_delete = True
    order_by = "last_name first_name id"
    #can_view = perms.is_authenticated

class PersonsByCountry(Persons):
    fk_name = 'country'
    order_by = "city addr1"
    columnNames = "city addr1 name nationality language"

class PersonsByNationality(Persons):
    fk_name = 'nationality'
    order_by = "city addr1"
    columnNames = "city addr1 name country language"



class Company(Contact):
    class Meta:
        abstract = True
        app_label = 'contacts'
    
    vat_id = models.CharField(max_length=200,blank=True)
    
    def as_address(self,linesep="\n<br/>"):
        s = Contact.as_address(self,linesep)
        return self.name + linesep + s

class CompanyPageLayout(ContactPageLayout):
    box1 = "name vat_id:12"
              
class Companies(reports.Report):
    #label = "Companies"
    page_layouts = (CompanyPageLayout,)
    columnNames = "name country id"
    model = 'contacts.Company'
    order_by = "name"
    #~ queryset = Contact.objects.exclude(companyName__exact=None)\
      #~ .order_by("companyName")
    
class CompaniesByCountry(Companies):
    fk_name = 'country'
    columnNames = "city addr1 name country language"
    order_by = "city addr1"
    
#~ class PersonsByCountryPage(layouts.PageLayout):
    #~ label = "Persons by Country"
    #~ main = """
    #~ isocode name
    #~ PersonsByCountry
    #~ """
#~ countries.Countries.register_page_layout(PersonsByCountryPage)

#~ class CompaniesByCountryPage(layouts.PageLayout):
    #~ label = "Companies by Country"
    #~ main = """
    #~ isocode name
    #~ CompaniesByCountry
    #~ """
#~ countries.Countries.register_page_layout(CompaniesByCountryPage)

        



            
#~ class Contacts(reports.Report):
    #~ page_layouts = (ContactPageLayout,)
    #~ columnNames = "id:3 companyName firstName lastName title country"
    #~ can_delete = True
    #~ model = Contact
    #~ order_by = "id"
    #~ #can_view = perms.is_authenticated

        
#~ class Companies(Contacts):
    #~ #queryset=Contact.objects.order_by("companyName")
    #~ columnNames = "companyName country title firstName lastName"
    #~ exclude = dict(companyName__exact='')
    #~ order_by = "companyName"
    

#~ class Persons(Contacts):
    #~ filter = dict(companyName__exact='')
    #~ order_by = "lastName firstName"
    #~ columnNames = "title firstName lastName country id"
    


#~ class ContactsByCountry(Contacts):
    #~ model = "contacts.Partner"
    #~ master = "countries.Country"
    #~ order_by = "city addr1"
    
#~ class CountryAndPartnersPage(layouts.PageLayout):
    #~ label = "Contacts by Country"
    #~ main = """
    #~ isocode name
    #~ ContactsByCountry
    #~ """
    

#~ class Countries(countries.Countries):
    #~ page_layouts = (layouts.PageLayout,CountryAndPartnersPage)
    
  

