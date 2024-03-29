## Copyright 2012 Luc Saffre
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
GROPH : Generated Read-Only Plain Html

:setting:`ROOT_URLCONF` 

ROOT_URLCONF = 'lino.ui.groph.urls'


"""

from django.conf.urls import patterns, url

from lino.ui.groph.views import Index

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='my-view'),
    #~ url(r'^mine/$', MyView.as_view(), name='my-view'),
)
