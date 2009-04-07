# -*- coding: utf-8 -*-

## Copyright 2008-2009 Luc Saffre.
## This file is part of the Lino project. 

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from models import Contact, Product, Invoice, Country
from models import Companies
from django.test import TestCase

from django.forms.models import modelform_factory, formset_factory
from lino.django.tom.layout import EditLayoutRenderer, ShowLayoutRenderer


class TestCase(TestCase):
    fixtures=[ 'demo.yaml' ]
    def setUp(self):
        pass
        
    def test01(self):
        luc=Contact.objects.get(id=2)
        self.assertEquals(unicode(luc), 'Luc Saffre')
        self.assertEquals(luc.as_address("\n"), u'''\
Mr. Luc Saffre
Rummajaani talu
Vana-Vigala küla
Vigala vald
78003 Raplamaa''')

    def test02(self):
      
        """A simple query. Select all contacts whose lastName contains an 'a', ordered by lastName.
        """
        
        s="\n".join([unicode(c) 
          for c in Contact.objects.filter(
            lastName__contains="a").order_by("lastName")])
        #print "\n"+s
        self.assertEquals(s,u"""\
Andreas Arens
Bäckerei Ausdemwald (Alfons Ausdemwald)
Bernard Bodard
Emil Eierschal
Jérôme Jeanémart
Karl Kask
Hans Flott & Co (Lisa Lahm)
Luc Saffre
Mets ja Puu OÜ (Tõnu Tamme)""")

    def test03(self):
        luc=Contact.objects.get(id=2)
        i1=Invoice(number=2000,customer=luc)
        i1.save()
        i2=Invoice(customer=luc)
        i2.save()
        self.assertEquals(i2.number,2001)
        
    def test04(self):
        luc=Contact.objects.get(id=2)
        table=Product.objects.get(id=1)
        chair=Product.objects.get(id=2)
        i=Invoice(customer=luc)
        i.save()
        i.invoiceitem_set.create(pos=1,product=table,qty=1)
        
    def test05(self):
        s=Companies().as_text(column_widths=dict(companyName=20,country=12))
        #print "\n"+s
        self.assertEquals(s.split(),u"""
Companies
=========
companyName         |country     |title         |firstName     |lastName
--------------------+------------+--------------+--------------+--------------
Bernd Brecht        |Germany     |Herr          |Bernd         |Brecht
Bäckerei Ausdemwald |Belgium     |Herrn         |Alfons        |Ausdemwald
Donderweer bv       |Netherlands |              |              |
Hans Flott & Co     |Germany     |Frau          |Lisa          |Lahm
Mets ja Puu OÜ      |Estonia     |              |Tõnu          |Tamme
Minu Firma OÜ       |Estonia     |              |              |
""".split(),"Companies().as_text() has changed in demo")
        
    def test06(self):
        model=Contact
        frmclass = modelform_factory(model)
        for obj in model.objects.all():
            frm = frmclass(instance=obj)
            layout = EditLayoutRenderer(obj.page_layout(),frm)
            s = layout.as_html()
            self.failUnless(s.startswith("<table"))
            
            layout = ShowLayoutRenderer(obj.page_layout(),obj)
            s = layout.as_html()
            self.failUnless(s.startswith("<table"))
            
    def test07(self):
        form_class = modelform_factory(Country)
        fs_class = formset_factory(form_class,can_delete=True)
        fs = fs_class()
        s=fs.forms[0].as_table()
        #print "\n"+s
        self.assertEquals(s.split(),u"""
<tr><th><label for="id_form-0-name">Name:</label></th><td><input id="id_form-0-name" type="text" name="form-0-name" maxlength="200" /></td></tr>
<tr><th><label for="id_form-0-isocode">Isocode:</label></th><td><input id="id_form-0-isocode" type="text" name="form-0-isocode" maxlength="2" /></td></tr>
<tr><th><label for="id_form-0-DELETE">Delete:</label></th><td><input type="checkbox" name="form-0-DELETE" id="id_form-0-DELETE" /></td></tr>
        """.split())
        
        
            



## Run these tests using "python manage.py test".
## see http://docs.djangoproject.com/en/dev/topics/testing/#topics-testing
