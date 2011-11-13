# -*- coding: UTF-8 -*-
## Copyright 2010-2011 Luc Saffre
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



import re

from django.utils.translation import ugettext_lazy as _
#~ from django.db import models
#~ from django.conf import settings

from lino.utils import join_words

name_prefixes1 = ("HET", "'T",'VAN','DER', 'TER','VOM','VON','OF', "DE", "DU", "EL", "AL")
name_prefixes2 = ("VAN DEN","VAN DER","VAN DE","IN HET", "VON DER","DE LA")





def name2kw(s,last_name_first=True):
    """
Split a string that contains both last_name and first_name.
The caller must indicate whether the string contains 
last_name first (e.g. Saffre Luc) or first_name first (e.g. Luc Saffre)

Examples:

>>> name2kw("Saffre Luc")
{'first_name': 'Luc', 'last_name': 'Saffre'}
>>> name2kw("Rilke Rainer Maria")
{'first_name': 'Rainer Maria', 'last_name': 'Rilke'}
>>> name2kw("Van Rompuy Herman")
{'first_name': 'Herman', 'last_name': 'Van Rompuy'}
>>> name2kw("'T Jampens Jan")
{'first_name': 'Jan', 'last_name': "'T Jampens"}
>>> name2kw("Van den Bossche Marc Antoine Bernard")
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Van den Bossche'}



>>> name2kw("Luc Saffre",False)
{'first_name': 'Luc', 'last_name': 'Saffre'}
>>> name2kw("Rainer Maria Rilke",False)
{'first_name': 'Rainer Maria', 'last_name': 'Rilke'}
>>> name2kw("Herman Van Rompuy",False)
{'first_name': 'Herman', 'last_name': 'Van Rompuy'}
>>> name2kw("Jan 'T Jampens",False)
{'first_name': 'Jan', 'last_name': "'T Jampens"}
>>> name2kw("Marc Antoine Bernard Van den Bossche",False)
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Van den Bossche'}



Bibliography:

#. http://en.wikipedia.org/wiki/Dutch_name
#. http://www.myheritage.com/support-post-130501/dutch-belgium-german-french-surnames-with-prefix-such-as-van




    """
    kw = {}
    a = s.strip().split()
    if len(a) == 1:
        return dict(last_name=a[0])
    elif len(a) == 2:
        if last_name_first:
            return dict(last_name=a[0],first_name= a[1])
        else:
            return dict(last_name=a[1],first_name= a[0])
    else:
        # string consisting of more than 3 words
        if last_name_first:
            a01 = a[0] + ' ' + a[1]
            if a01.upper() in name_prefixes2:
                return dict(
                  last_name = a01 + ' ' + a[2],
                  first_name = ' '.join(a[3:]))
            elif a[0].upper() in name_prefixes1:
                return dict(
                    last_name = a[0] + ' ' + a[1],
                    first_name = ' '.join(a[2:]))
            else:
                return dict(last_name = a[0],
                    first_name = ' '.join(a[1:]))
        else:
            if len(a) >= 4:
                pc = a[-3] + ' ' + a[-2] # prefix2 candidate
                if pc.upper() in name_prefixes2:
                    return dict(
                        last_name = pc + ' ' + a[-1],
                        first_name = ' '.join(a[:-3]))
            pc = a[-2] # prefix candidate
            if pc.upper() in name_prefixes1:
                return dict(
                    last_name = pc + ' ' + a[-1],
                    first_name = ' '.join(a[:-2]))
        return dict(
            last_name = a[-1],
            first_name = ' '.join(a[:-1]))
            
    return kw
    
def street2kw(s,**kw):
    """
Parse a string to extract the fields street, street_no and street_box.

Examples:
    
>>> street2kw(u"Limburger Weg")
{'street': u'Limburger Weg'}
>>> street2kw(u"Loten 3")
{'street_box': u'', 'street': u'Loten', 'street_no': u'3'}
>>> street2kw(u"Loten 3A")
{'street_box': u'A', 'street': u'Loten', 'street_no': u'3'}

>>> street2kw(u"In den Loten 3A")
{'street_box': u'A', 'street': u'In den Loten', 'street_no': u'3'}

>>> street2kw(u"Auf'm Bach")
{'street': u"Auf'm Bach"}
>>> street2kw(u"Auf'm Bach 3")
{'street_box': u'', 'street': u"Auf'm Bach", 'street_no': u'3'}
>>> street2kw(u"Auf'm Bach 3a")
{'street_box': u'a', 'street': u"Auf'm Bach", 'street_no': u'3'}
>>> street2kw(u"Auf'm Bach 3 A")
{'street_box': u'A', 'street': u"Auf'm Bach", 'street_no': u'3'}

>>> street2kw(u"rue des 600 Franchimontois 1")
{'street_box': u'', 'street': u'rue des 600 Franchimontois', 'street_no': u'1'}

>>> street2kw(u"Neustr. 1 (Referenzadr.)")
{'addr2': u'(Referenzadr.)', 'street': u'Neustr.', 'street_no': u'1'}
    
    """
    #~ m = re.match(r"(\D+),?\s*(\d+)\s*(\w*)", s)
    m = re.match(r"(.+),?\s+(\d+)\s*(\D*)$", s)
    if m:
        kw['street'] = m.group(1).strip()
        kw['street_no'] = m.group(2).strip()
        street_box = m.group(3).strip()
        if len(street_box) > 5:
            kw['addr2'] = street_box
        else:
            kw['street_box'] = street_box
    else:
        kw['street'] = s
    return kw

GENDER_MALE = 'M'
GENDER_FEMALE = 'F'
GENDER_CHOICES = ((GENDER_MALE,_('Male')),(GENDER_FEMALE,_('Female')))


def get_salutation(lang,gender,nominative=False):
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
    if lang == 'de':
        if gender == GENDER_FEMALE:
            return "Frau"
        if nominative:
            return "Herr"
        return "Herrn"
    if lang == 'fr':
        if gender == GENDER_FEMALE:
            return "Mme"
        return "M."
    if gender == GENDER_FEMALE:
        return "Mrs"
    return "Mr"
        


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()




