# -*- coding: UTF-8 -*-
## Copyright 2008-2011 Luc Saffre
## This file is part of the Lino-DSBE project.
## Lino-DSBE is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-DSBE is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-DSBE; if not, see <http://www.gnu.org/licenses/>.

"""
Installs a set of property types and property groups specific to 
:mod:`lino.apps.dsbe`.

"""


from django.utils.translation import ugettext as _
#~ from django.conf import settings

from lino.utils.instantiator import Instantiator
from lino.utils.babel import babel_values
from lino.models import update_site_config
from lino.modlib.properties.models import PropType


def objects():
    onoff = PropType.objects.get(pk=1)  # created in std.dpy
    appraisal = PropType.objects.get(pk=2) # created in std.dpy
    
    pgroup = Instantiator('properties.PropGroup').build
    
    skills = pgroup(**babel_values('name',**dict(
      en="Skills",de=u"Fachkompetenzen",
      fr=u"Compétences professionnelles")))
    skills.save()
    yield skills
    softskills = pgroup(**babel_values('name',**dict(
        en="Soft skills",
        de=u"Sozialkompetenzen",
        fr=u"Compétences sociales")))
    softskills.save()
    yield softskills
    obstacles = pgroup(**babel_values('name',**dict(
        en="Obstacles",de=u"Hindernisse",
        fr="Obstacles")))
    obstacles.save()
    yield obstacles
    
    update_site_config(
      propgroup_skills = skills,
      propgroup_softskills = softskills,
      propgroup_obstacles = obstacles,
      )
    
    
    #~ skills = settings.LINO.config.propgroup_skills
    skill = Instantiator('properties.Property',group=skills,type=onoff).build
    yield skill(**babel_values('name',
          de=u"Gartenarbeit",
          fr=u"Jardinier",
          en=u"Gardener",
          ))
    yield skill(**babel_values('name',
          de=u"Verkäufer",
          fr=u"Vendeur",
          en=u"Salesman",
          ))
    yield skill(**babel_values('name',
          de=u"Haushaltshilfe",
          fr=u"Aide ménage",
          en=u"Household aid",
          ))
    yield skill(**babel_values('name',
          de=u"Bäckerei",
          fr=u"Pâtisserie",
          en=u"Bakery",
          ))
    yield skill(**babel_values('name',
          de=u"Kochen",
          fr=u"Cuisiner",
          en=u"Cook",
          ))
    yield skill(**babel_values('name',
          de=u"Führerschein",
          fr=u"Permis de conduire",
          en=u"Driving licence",
          ))
          
    skill = Instantiator('properties.Property',group=softskills,type=appraisal).build
    yield skill(**babel_values('name',
          de=u"Gehorsam",
          fr=u"Obéissant",
          en=u"Obedient",
          ))
    yield skill(**babel_values('name',
          de=u"Führungsfähigkeit",
          fr=u"Leader",
          en=u"Leader",
          ))
          
    skill = Instantiator('properties.Property',group=obstacles,type=onoff).build
    yield skill(**babel_values('name',
          de=u"nicht am Wochenende",
          fr=u"pas le week-end",
          en=u"no work on weekend",
          ))
    no_shift = skill(**babel_values('name',
          de=u"keine Schichtarbeit",
          fr=u"pas de travail posté",
          en=u"no shift work",
          ))
    yield no_shift
    
    yield skill(**babel_values('name',
          de=u"nur Vollzeit",
          fr=u"seulement temps plein",
          en=u"only full-time",
          ))
    yield skill(**babel_values('name',
          de=u"nur Teilzeit",
          fr=u"seulement mi-temps",
          en=u"only part-time",
          ))
    yield skill(**babel_values('name',
          de=u"Körperliche Einschränkung",
          fr=u"Handicap physique",
          en=u"Physical handicap",
          ))
    yield skill(**babel_values('name',
          de=u"Geistige Einschränkung",
          fr=u"Handicap mental",
          en=u"Mental handicap",
          ))
    yield skill(**babel_values('name',
          de=u"Psychische Einschränkung",
          fr=u"Handicap psychique",
          en=u"Psychological handicap",
          ))
    yield skill(**babel_values('name',
          de=u"Gesundheitliche Einschränkung",
          fr=u"Handicap santé",
          en=u"Health handicap",
          ))
    yield skill(**babel_values('name',
          de=u"Juristische Probleme",
          fr=u"Problème juridiques",
          en=u"Juristic problems",
          ))
          
    yield skill(**babel_values('name',
          de=u"Suchtprobleme",
          fr=u"Toxicomanie ",
          en=u"Addiction problems",
          ))
    yield skill(**babel_values('name',
          de=u"Mangelnde Sozialkompetenz",
          fr=u"Manque de compétence sociale",
          en=u"Lack of social competence",
          ))
    yield skill(**babel_values('name',
          de=u"Motivationsmangel",
          fr=u"Manque motivation",
          en=u"Lack of motivation",
          ))
    yield skill(**babel_values('name',
          de=u"Personen zu Lasten",
          fr=u"Personnes à charge",
          en=u"Head of a family",
          ))
    yield skill(**babel_values('name',
          de=u"Kleinkinder",
          fr=u"Petits enfants à charge",
          en=u"Small children",
          ))
    yield skill(**babel_values('name',
          de=u"Analphabet",
          fr=u"Analphabète",
          en=u"Illiterate",
          ))
