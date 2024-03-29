# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
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
Defines the model mixin :class:`Duplicable`.
"duplicable" [du'plikəblə] means "able to produce a duplicate ['duplikət],['du:plikeit]".
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.related import ForeignRelatedObjectsDescriptor

from lino.core.dbutils import obj2str
from lino.core import actions
from lino.core import model


class Duplicate(actions.Action):
    """
    Duplicate the row on which it is being executed.
    """
    label = _("Duplicate")
    sort_index = 11
    show_in_workflow = False
    readonly = True # like InsertRow. See docs/blog/2012/0726
    icon_name = 'arrow_divide'
    #~ action_name = 'duplicate'

  
    def is_callable_from(self,caller):
        if isinstance(caller,actions.InsertRow): 
            return False
        return True
        
    def get_action_permission(self,ar,obj,state):
        if ar.get_user().profile.readonly: 
            return False
        return super(Duplicate,self).get_action_permission(ar,obj,state)
        
    def run_from_code(self,ar,**known_values):
        obj = ar.selected_rows[0]
        #~ if not isinstance(ar,actions.ActionRequest):
            #~ raise Exception("Expected and ActionRequest but got %r" % ar)
        #~ related = dict()
        #~ for m2m in self._meta.many_to_many:
            #~ print m2m
        #~ print self._lino_ddh.fklist
        related = []
        for m,fk in obj._lino_ddh.fklist:
            #~ related[fk] = m.objects.filter(**known_values)
            if fk.name in m.allow_cascaded_delete:
                related.append((fk,m.objects.filter(**{fk.name:obj})))
            #~ if issubclass(m,Duplicable):
                #~ related[fk.related_name] = getattr(self,fk.name)
                #~ related[fk.name] = getattr(self,fk.rel.related_name)
        #~ print related
        #~ raise Exception("20120612")
        #~ for name,de in self.duplicated_fields:
            #~ if isinstance(de,models.Field):
                #~ known_values[name] = getattr(self,name)
            #~ elif isinstance(de,ForeignRelatedObjectsDescriptor):
                #~ ro = getattr(self,name)
                #~ related[de] = ro
                #~ # print de.related.parent_model
                #~ # print de.related.model
                #~ # print de.related.opts
                #~ # print de.related.field
                #~ # print de.related.name
                #~ # print de.related.var_name
                #~ # print '---'
            #~ else:
                #~ raise Exception("20120612 Cannot handle %r" % de)
                
        #~ print 20120608, known_values
        if True:
            #~ known_values = dict()
            for f in obj._meta.fields:
                if not f.primary_key:
                    known_values[f.name] = getattr(obj,f.name)
            new = obj.__class__(**known_values)
            #~ new = ar.create_instance(**kw)
            """
            20120704 create_instances causes fill_from_person() on a CBSS request.
            """
        else:
            # doesn't seem to want to work
            new = obj
            for f in obj._meta.fields:
                if f.primary_key:
                    setattr(new,f.name,None) # causes Django to consider this an unsaved instance
            #~ new.pk = None # causes Django to consider this an unsaved instance
        
        #~ print 20120704, obj2str(new)
        new.save(force_insert=True)
        #~ new = duplicate(self)
        #~ new.on_duplicate(ar)
        new.on_duplicate(ar,None)
        #~ m = getattr(new,'on_duplicate',None)
        #~ if m is not None:
            #~ m(ar,None)
        
        for fk,qs in related:
            for relobj in qs:
                relobj.pk = None # causes Django to save a copy
                setattr(relobj,fk.name,new)
                #~ if isinstance(obj,Duplicable):
                relobj.on_duplicate(ar,new)
                #~ m = getattr(obj,'on_duplicate',None)
                #~ if m is not None:
                    #~ m(ar,new)
                relobj.save(force_insert=True)
        
        #~ for de,rm in related.items():
            #~ # rm is the RelatedManager
            #~ for obj in rm.all():
                #~ obj.pk = None
                #~ setattr(obj,de.related.field.name,new)
                #~ m = getattr(obj,'on_duplicate',None)
                #~ if m is not None:
                    #~ m(ar,new)
                #~ obj.save()
                
        return new
        
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        new = self.run_from_code(ar)
        kw = dict()
        kw.update(refresh=True)
        kw.update(message=_("Duplicated %(old)s to %(new)s.") % dict(old=obj,new=new))
        #~ kw.update(new_status=dict(record_id=new.pk))
        kw.update(goto_record_id=new.pk)
        return ar.success(**kw)
        
        
  

class Duplicable(model.Model):
    """
    Adds a row action "Duplicate" which duplicates (creates a clone of) 
    the object it was called on.
    
    Subclasses may override :meth:`on_duplicate` to customize the default 
    behaviour,
    which is to copy all fields except the primary key 
    and all related objects that are duplicable.
    
    """
    class Meta:
        abstract = True
        
    duplicate = Duplicate()
    
        
    #~ @dd.action(_("Duplicate"),sort_index=60,show_in_workflow=False,readonly=True)
    #~ def duplicate(self,ar,**kw):
        #~ related = []
        #~ for m,fk in self._lino_ddh.fklist:
            #~ if m.allow_cascaded_delete:
                #~ related.append((fk,m.objects.filter(**{fk.name:self})))
        #~ if True:
            #~ for f in self._meta.fields:
                #~ if not f.primary_key:
                    #~ kw[f.name] = getattr(self,f.name)
            #~ new = self.__class__(**kw)
            #~ """
            #~ 20120704 create_instances causes fill_from_person() on a CBSS request.
            #~ """
        #~ else:
            #~ # doesn't seem to want to work
            #~ new = self
            #~ for f in self._meta.fields:
                #~ if f.primary_key:
                    #~ setattr(new,f.name,None) # causes Django to consider this an unsaved instance
            #~ new.pk = None # causes Django to consider this an unsaved instance
        
        #~ new.save(force_insert=True)
        #~ new.on_duplicate(ar,None)
        
        #~ for fk,qs in related:
            #~ for obj in qs:
                #~ obj.pk = None # causes Django to save a copy
                #~ setattr(obj,fk.name,new)
                #~ obj.on_duplicate(ar,new)
                #~ obj.save(force_insert=True)
        
        #~ kw = dict()
        #~ kw.update(refresh=True)
        #~ kw.update(message=_("Duplicated %(old)s to %(new)s.") % dict(old=self,new=new))
        #~ kw.update(goto_record_id=new.pk)
        #~ return ar.success(**kw)
        
