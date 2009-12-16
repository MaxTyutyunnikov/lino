## Copyright 2009 Luc Saffre
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


from django.db import models
from lino.modlib import fields
from lino import reports


#
# PROJECT TYPE
#
class ProjectType(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class ProjectTypes(reports.Report):
    model = ProjectType
    order_by = "name"

#
# PROJECT
#
class Project(models.Model):
    class Meta:
        abstract = True
        
    name = models.CharField(max_length=200)
    type = models.ForeignKey(ProjectType,blank=True,null=True)
    started = fields.MyDateField(blank=True,null=True) 
    stopped = fields.MyDateField(blank=True,null=True) 
    
    def __unicode__(self):
        return self.name
        
class Projects(reports.Report):
    model = 'projects.Project'
    order_by = "name"
    
