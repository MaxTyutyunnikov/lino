# -*- coding: utf-8 -*-
## Copyright 2011 Luc Saffre
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
This module contains "quick" tests that are run on a demo database 
without any fixture. You can run only these tests by issuing::

  python manage.py test dsbe.NoFixturesTest

  
"""
import logging
logger = logging.getLogger(__name__)

#~ from django.utils import unittest
#~ from django.test.client import Client
#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
from lino.modlib.contacts.models import Companies

from lino.utils import i2d
from lino.tools import resolve_model
#Companies = resolve_model('contacts.Companies')
from lino.utils.test import TestCase

Person = resolve_model('contacts.Person')
Property = resolve_model('properties.Property')
PersonProperty = resolve_model('properties.PersonProperty')

#~ class NoFixturesTest(TestCase):
class Test(TestCase):
    pass
    #~ fixtures = ['std']
            
  
def test01(self):
    """
    Used on :doc:`/blog/2011/0414`.
    """
    from lino.utils.dpy import Serializer
    from lino.apps.dsbe.models import Company, CourseProvider
    ser = Serializer()
    #~ ser.models = [CourseProvider,Company]
    ser.models = [CourseProvider]
    ser.write_preamble = False
    self.assertEqual(Company._meta.parents,{})
    parent_link_field = CourseProvider._meta.parents.get(Company)
    #~ print parent_link_field.name
    #~ self.assertEqual(CourseProvider._meta.parents.get(Company),{})
    #~ self.assertEqual(CourseProvider._meta.parents,{})
    fields = [f.attname for f in CourseProvider._meta.fields]
    local_fields = [f.attname for f in CourseProvider._meta.local_fields]
    self.assertEqual(','.join(local_fields),'company_ptr_id')
    fields = [f.attname for f in Company._meta.fields]
    local_fields = [f.attname for f in Company._meta.local_fields]
    self.assertEqual(fields,local_fields)
    #~ self.assertTrue(','.join([f.attname for f in local_fields]),'company_ptr_id')
      
    #~ foo = Company(name='Foo')
    #~ foo.save()
    bar = CourseProvider(name='Bar')
    bar.save()
    
    #~ ser.serialize([foo,bar])
    ser.serialize([bar])
    #~ print ser.stream.getvalue()
    self.assertEqual(ser.stream.getvalue(),"""
def create_dsbe_courseprovider(company_ptr_id):
    return insert_child(Company.objects.get(pk=company_ptr_id),CourseProvider)


def dsbe_courseprovider_objects():
    yield create_dsbe_courseprovider(1)


def objects():
    for o in dsbe_courseprovider_objects(): yield o
""")
    
    
def test02(self):
    """
    Testing whether `/api/notes/NoteTypes/1?fmt=json` 
    has no item `templateHidden`.
    See :doc:`/blog/2011/0509`.
    """
    #~ from lino.apps.dsbe.models import NoteType
    from lino.modlib.notes.models import NoteType
    i = NoteType(build_method='appyodt',template="Default.odt",id=1)
    i.save()
    response = self.client.get('/api/notes/NoteTypes/1?fmt=json')
    result = self.check_json_result(response,'data title navinfo disable_delete id')
    self.assertEqual(result['data']['template'],'Default.odt')
    self.assertEqual(result['data'].has_key('templateHidden'),False)
    
    response = self.client.get('/api/notes/NoteTypes/1?fmt=detail')
    #~ print '\n'.join(response.content.splitlines()[:1])
    
    c = response.content
    
    self.assertTrue(c.endswith('''}); // end of onReady()
</script></head><body id="body">
</body></html>'''))

    if False:
        """
        TODO:
        expat has a problem to parse the HTML generated by Lino.
        Problem occurs near <div class="htmlText">...
        Note that even if the parseString gets through, we won't 
        have any INPUT elements since they will be added dynamically 
        by the JS code...
        """
        fd = file('tmp.html','w')
        fd.write(c)
        fd.close()
        
        from xml.dom import minidom 
        dom = minidom.parseString(c)
        print dom.getElementsByTagName('input')
        response = self.client.get('/api/lino/SiteConfigs/1?fmt=json')
        