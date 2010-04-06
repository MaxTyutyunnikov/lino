## Copyright 2009-2010 Luc Saffre
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


import traceback
#import logging ; logger = logging.getLogger('lino.reports')

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _

from django.db import models
from django.db.models.query import QuerySet
from django import forms
from django.conf.urls.defaults import patterns, url, include
from django.forms.models import modelform_factory
from django.forms.models import _get_foreign_key
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType


from django.http import HttpResponse
#from django.core import serializers
#from django.shortcuts import render_to_response
#from django.utils import simplejson
from django.utils.safestring import mark_safe

try:
    # l:\snapshot\xhtml2pdf
    import ho.pisa as pisa
except ImportError:
    pisa = None




import lino
from lino import layouts
from lino import actions
from lino.utils import perms, menus
from lino.core import datalinks
from lino.core import actors
from lino.ui import base

from lino.modlib.tools import resolve_model, resolve_field, get_app, model_label
#~ from lino.modlib import field_choices

def base_attrs(cl):
    #~ if cl is Report or len(cl.__bases__) == 0:
        #~ return
    #~ myattrs = set(cl.__dict__.keys())
    for b in cl.__bases__:
        for k in base_attrs(b):
            yield k
        for k in b.__dict__.keys():
            yield k


def add_quick_search_filter(qs,search_text):
    if not isinstance(qs,QuerySet): 
        # TODO: filter also simple lists 
        return qs
    q = models.Q()
    for field in qs.model._meta.fields:
        if isinstance(field,models.CharField):
            kw = {field.name+"__contains": search_text}
            q = q | models.Q(**kw)
    return qs.filter(q)
        
def data_elems(meta):
    for f in meta.fields: yield f.name
    for f in meta.many_to_many: yield f.name
    for f in meta.virtual_fields: yield f.name
    # todo: for slave in self.report.slaves
    
def get_data_elem(model,name):
    try:
        return model._meta.get_field(name)
    except models.FieldDoesNotExist,e:
        pass
    rpt = get_slave(model,name)
    if rpt is not None: return rpt
    m = get_unbound_meth(model,name)
    if m is not None: return m
    
    for vf in model._meta.virtual_fields:
        if vf.name == name:
            return vf


def rc_name(rptclass):
    return rptclass.app_label + '.' + rptclass.__name__
    
master_reports = []
slave_reports = []
generic_slaves = {}

def register_report(rpt):
    #rptclass.app_label = rptclass.__module__.split('.')[-2]
    if rpt.typo_check:
        myattrs = set(rpt.__class__.__dict__.keys())
        for attr in base_attrs(rpt.__class__):
            myattrs.discard(attr)
        if len(myattrs):
            lino.log.warning("%s defines new attribute(s) %s", rpt.__class__, ",".join(myattrs))
    
    if rpt.model is None:
        lino.log.debug("%s is an abstract report", rpt)
        return
        
    #~ rpt = cls()
    if rpt.master is None:
        master_reports.append(rpt)
        if rpt.use_as_default_report:
            lino.log.debug("register %s : model_report for %s", rpt.actor_id, model_label(rpt.model))
            rpt.model._lino_model_report = rpt
        else:
            lino.log.debug("register %s: not used as model_report",rpt.actor_id)
    elif rpt.master is ContentType:
        lino.log.debug("register %s : generic slave for %r", rpt.actor_id, rpt.fk_name)
        generic_slaves[rpt.actor_id] = rpt
    else:
        slave_reports.append(rpt)

    
    
def discover():
    """
    - Each model can receive a number of "slaves". 
      Slaves are reports that display detail data for a known instance of that model (their master).
      They are stored in a dictionary called '_lino_slaves'.
      
    - For each model we want to find out the "model report" ot "default report".
      The "choices report" for a foreignkey field is also currently simply the pointed model's
      model_report.
      `_lino_model_report`

    """
    
    lino.log.info("Analyzing up Reports...")
    lino.log.debug("Register Report actors...")
    for rpt in actors.actors_dict.values():
        if isinstance(rpt,Report) and rpt.__class__ is not Report:
            register_report(rpt)
            
    lino.log.debug("Instantiate model reports...")
    for model in models.get_models():
        rpt = getattr(model,'_lino_model_report',None)
        if rpt is None:
            rpt = report_factory(model)
            register_report(rpt)
            model._lino_model_report = rpt
            
    lino.log.debug("Analyze %d slave reports...",len(slave_reports))
    for rpt in slave_reports:
        slaves = getattr(rpt.master,"_lino_slaves",None)
        if slaves is None:
            slaves = {}
            #~ setattr(rpt.master,'_lino_slaves',slaves)
            rpt.master._lino_slaves = slaves
        slaves[rpt.actor_id] = rpt
        lino.log.debug("%s: slave for %s",rpt.actor_id, rpt.master.__name__)
    lino.log.debug("Assigned %d slave reports to their master.",len(slave_reports))
        
    #~ lino.log.debug("Setup model reports...")
    #~ for model in models.get_models():
        #~ model._lino_model_report.setup()
        
    #~ lino.log.debug("Instantiate property editors...")
    #~ for model in models.get_models():
        #~ pw = ext_elems.PropertiesWindow(model)
        #~ model._lino_properties_window = pw
            
    lino.log.debug("reports.setup() done")

def get_slave(model,name):
    rpt = actors.get_actor(name)
    if rpt is None: 
        return None
    if rpt.master is not ContentType:
        assert issubclass(model,rpt.master), "%s.master is %r,\nmust be subclass of %r" % (name,rpt.master,model)
    return rpt
    #~ rpt = generic_slaves.get(name,None)
    #~ if rpt is not None:
        #~ return rpt
    #~ for b in (model,) + model.__bases__:
        #~ d = getattr(b,"_lino_slaves",None)
        #~ if d:
            #~ rpt = d.get(name,None)
            #~ if rpt is not None:
                #~ return rpt

def get_model_report(model):
    return model._lino_model_report

class GridEdit(actions.Action):
    name = 'grid'
    def run_action(self,ar):
        return ar.ui.gridedit_report(ar)


class InsertRow(actions.RowsAction):
    label = _("Insert")
    name = 'insert'
    key = actions.INSERT # (ctrl=True)
    
    def run_action(self,rr):
        #~ rr = dlg.get_request()
        #~ for r in rr.insert_row(self): 
            #~ yield r
            
        if rr.rh.detail_link is None:
            raise Exception("This report has no detail layout")
        
        row = rr.create_instance()
        
        return rr.show_detail(row)
        
        #~ layout = layouts.get_detail_layout(row.__class__)
        
        #~ if layout is None:
        #~ dl = RowDataLink(rr.ui,row)
        #~ dl.setup()
        #~ lh = layout.get_handle(rr.ui)
        #~ return rr.show_window(dl,lh)
        
        #~ fh = actions.FormHandle(lh,dl)
        #~ yield dlg.show_modal_form(fh)
        #~ while True:
            #~ if dlg.modal_exit != 'ok':
                #~ yield dlg.cancel()
            #~ print dlg.params
            #~ if row.update(dlg.params):
                #~ row.save()
                #~ yield dlg.refresh_caller().over()
        
    def old_run_in_dlg(self,dlg):
        yield dlg.confirm(_("Insert new row. Are you sure?"))
        rr = dlg.get_request()
        row = rr.create_instance()
        row.save()
        yield dlg.refresh_caller().over()
        
        
  
class DeleteSelected(actions.RowsAction):
    needs_selection = True
    label = _("Delete")
    name = 'delete'
    key = actions.DELETE # (ctrl=True)
    
        
    def run_action(self,rr):
        if len(dlg.selected_rows) == 1:
            msg = _("Deleted row %s") % dlg.selected_rows[0]
        else:
            msg = _("Deleted %d rows") % len(dlg.selected_rows)
            
        for row in dlg.selected_rows:
            row.delete()
        return rr.refresh_caller().notify(_("Success") + ": " + msg)
        
    def run_in_dlg(self,dlg):
        if len(dlg.selected_rows) == 1:
            msg = _("Delete row %s") % dlg.selected_rows[0]
        else:
            msg = _("Delete %d rows") % len(dlg.selected_rows)
        yield dlg.confirm(msg + '. ' + _("Are you sure?"))
        for row in dlg.selected_rows:
            row.delete()
        yield dlg.refresh_caller().notify(_("Success") + ": " + msg).over()
        
class DetailAction(actions.ToggleWindowAction):
    def __init__(self,dtl):
        assert isinstance(dtl,layouts.DetailLayout)
        self.detail = dtl
        self.name = dtl._actor_name
        self.label = dtl.label
        actions.ToggleWindowAction.__init__(self)
        
    def run_action(self,rr):
        rr.toggle_window(self.detail)
                
class PropertiesAction(actions.ToggleWindowAction):
    name = 'properties'
    label = _('Properties')
    
class SlaveGridAction(actions.ToggleWindowAction):
    def __init__(self,slave):
        assert isinstance(slave,Report)
        self.slave = slave
        self.name = slave._actor_name
        self.label = slave.label
        actions.ToggleWindowAction.__init__(self)
        
    def run_action(self,rr):
        #~ slave_rh = rr.ui.get_handle(self.slave)
        #~ return self.slave.default_action.run_action()
        slave_rr = rr.ui.get_report_ar(self.slave)
        #~ slave_rh.
        #~ rr.toggle_window(slave_rh.)
        slave_rr.run()
                
        

class ReportHandle(datalinks.DataLink,actors.ActorHandle):
  
    detail_link = None
    
    def __init__(self,ui,report):
        #lino.log.debug('ReportHandle.__init__(%s)',rd)
        actors.ActorHandle.__init__(self,report)
        assert isinstance(report,Report)
        actions = list(report.actions)
        if report.model is not None:
            for dtl in report.detail_layouts:
                actions.append(DetailAction(dtl))
            for slave in report._slaves:
                actions.append(SlaveGridAction(slave))
            from lino.modlib.properties import models as properties
            #~ props_request = properties.PropValuesByOwner().request(\
                #~ ui,master=report.model)
            #~ if len(props_request) > 0:
            if len(properties.Property.properties_for_model(report.model)) > 0:
                actions.append(PropertiesAction())
        
        datalinks.DataLink.__init__(self,ui,actions)
        self.report = report
        self.content_type = ContentType.objects.get_for_model(self.report.model).pk
        
                
        
  
    def __str__(self):
        return str(self.report) + 'Handle'
            
    def setup(self):
        if self.report.use_layouts:
            self.list_layout = self.report.list_layout.get_handle(self.ui)
            self.details = [ pl.get_handle(self.ui) for pl in self.report.detail_layouts ]
            self.layouts = [ self.list_layout ] + self.details
            if len(self.details) > 0:
                self.detail_link = DetailDataLink(self,self.details[0])
        else:
            self.details = []
            self.layouts = []
            
            
        self.ui.setup_report(self)
        
        #~ if self.report.use_layouts:
            #~ def lh(layout_class,*args,**kw):
                #~ return layouts.LayoutHandle(self,layout_class(),*args,**kw)
            
            #~ self.choice_layout = lh(layouts.RowLayout,0,self.report.display_field)
            
            #~ index = 1
            #~ self.list_layout = lh(layouts.RowLayout,index,self.report.column_names)
            
            #~ self.layouts = [ self.choice_layout, self.row_layout ]
            #~ index = 2
            #~ for lc in self.report.page_layouts:
                #~ self.layouts.append(lh(lc,index))
                #~ index += 1
        #~ else:
            #~ self.choice_layout = None
            #~ self.row_layout = None
            #~ self.layouts = []
            
        
    #~ def get_default_layout(self):
        #~ return self.layouts[self.report.default_layout]
        
    #~ def get_create_layout(self):
        #~ return self.layouts[2]
        
    def submit_elems(self):
        return []
        
    def get_queryset(self,rr):
        return self.report.get_queryset(rr)
        
    def get_layout(self,name):
        return self.layouts[name]
        
    def get_absolute_url(self,*args,**kw):
        return self.ui.get_report_url(self,*args,**kw)
        
    def data_elems(self):
        for de in data_elems(self.report.model._meta): yield de
          
    def get_data_elem(self,name):
        return get_data_elem(self.report.model,name)
        #~ if de is not None:
            #~ return de
        #~ return getattr(self.report,name)
        
    #~ def get_actions(self):
        #~ return self.report.actions
        
    def get_details(self):
        return self.details
        #~ return self.layouts[1:]
          
    def get_slaves(self):
        return [ sl.get_handle(self.ui) for sl in self.report._slaves ]
            
    def get_title(self,rr):
        return self.report.get_title(rr)
        
    def request(self,**kw):
        return self.ui.get_report_ar(self,**kw)
        
        
            

#~ class RowHandle(datalinks.DataLink):
class DetailDataLink(datalinks.DataLink):
  
    def __init__(self,rh,lh):
        self.rh = rh
        self.lh = lh
        #~ self.rh = get_model_report(row.__class__).get_handle(ui)
        #~ RowHandle.__init__(self,ui,[actions.Cancel(), actions.OK()])
        datalinks.DataLink.__init__(self,rh.ui,[actions.Cancel(), actions.OK()])
        self.inputs = []
        self.row = None
        
    def get_queryset(self,rr):
        return [ self.row ]
        
    #~ def before_step(self,dlg):
        #~ d = self.rh.store.get_from_form(dlg.params)
        #~ dlg.params.update(**d)
        #~ for i in self.rh.store.inputs:
            #~ if isinstance(i,List):
                #~ v = dlg.request.POST.getlist(i.name)
            #~ else:
                #~ v = dlg.request.POST.get(i.name)
            #~ dlg.params[i.name] = v
            
    def data_elems(self):
        return self.rh.data_elems()
        #~ for de in self.rh.data_elems(): yield de
          
    def get_data_elem(self,name):
        return self.rh.get_data_elem(name)
        
    def get_title(self,dlg):
        return unicode(self.row)
        
    #~ def submit_elems(self):
        #~ for name in data_elems(self.row._meta): yield name
        
    #~ def setup(self):
        #~ self.list_layout = rpt.get_handle(self.ui)
        #~ self.details = [ pl.get_handle(self.ui) for pl in rpt.detail_layouts ]
        #~ self.layouts = [ self.list_layout ] + self.details
        #~ self.ui.setup_report(self)
        


class Report(actors.HandledActor): # actions.Action): # 
    _handle_class = ReportHandle
    _handle_selector = base.UI
    params = {}
    field = None
    queryset = None 
    model = None
    use_as_default_report = True
    order_by = None
    filter = None
    exclude = None
    title = None
    column_names = None
    hide_columns = None
    #~ hide_fields = None
    #label = None
    #~ param_form = ReportParameterForm
    #default_filter = ''
    #name = None
    form_class = None
    master = None
    slaves = None
    fk_name = None
    help_url = None
    #master_instance = None
    page_length = 10
    display_field = '__unicode__'
    boolean_texts = ('Ja','Nein',' ')
    #date_format = 'Y-m-d'
    date_format = 'd.m.y'
    #date_format = '%d.%m.%y'
    
    page_layouts = None # (layouts.PageLayout ,)
    #~ row_layout_class = None
    
    can_view = perms.always
    can_add = perms.is_authenticated
    can_change = perms.is_authenticated
    can_delete = perms.is_authenticated
    
    default_action = GridEdit()
    default_layout = 0
    
    typo_check = True
    url = None
    
    use_layouts = True
    
    button_label = None
    
    
    def __init__(self):
        if self.model is None:
            if self.queryset is not None:
                self.model = self.queryset.model
            # raise Exception(self.__class__)
        else:
            self.model = resolve_model(self.model,self.app_label,self)
        if self.model is not None:
            self.app_label = self.model._meta.app_label
            self.actions = self.actions + [ DeleteSelected(), InsertRow() ]
            m = getattr(self.model,'setup_report',None)
            if m:
                m(self)
                
        
        actors.HandledActor.__init__(self)
        
        #~ lino.log.debug("Report.__init__() %s", self)
        
        if self.fk_name:
            #~ self.master = resolve_model(self.master,self.app_label)
            try:
                fk, remote, direct, m2m = self.model._meta.get_field_by_name(self.fk_name)
                assert direct
                assert not m2m
                master = fk.rel.to
            except models.FieldDoesNotExist,e:
                #~ lino.log.debug("FieldDoesNotExist in %r._meta.get_field_by_name(%r)",self.model,self.fk_name)
                master = None
                for vf in self.model._meta.virtual_fields:
                    if vf.name == self.fk_name:
                        fk = vf
                        master = ContentType
            if master is None:
                raise Exception("%s : no master for fk_name %r in %s" % (
                    self,self.fk_name,self.model.__name__))
            self.master = master
            self.fk = fk
        else:
            assert self.master is None
        #~ elif self.master:
            #~ lino.log.warning("DEPRECATED: replace %s.master by fk_name" % self.actor_id)
            #~ #assert isinstance(self.master,object), "%s.master is a %r" % (self.name,self.master)
            #~ assert issubclass(self.master,models.Model), "%s.master is a %r" % (self.actor_id,self.master)
            #~ self.fk = _get_foreign_key(self.master,self.model) #,self.fk_name)
        
        
        #self.setup()
        
        #register_report(self)
        
        
    @classmethod
    def spawn(cls,suffix,**kw):
        kw['app_label'] = cls.app_label
        return type(cls.__name__+str(suffix),(cls,),kw)
        
    def do_setup(self):
        if self.model is not None:
            self.list_layout = layouts.list_layout_factory(self)
            
            self.detail_layouts = getattr(self.model,'_lino_layouts',[])
            if hasattr(self.model,'_lino_slaves'):
                if self.slaves is None:
                    #self._slaves = [sl() for sl in self.model._lino_slaves.values()]
                    self._slaves = self.model._lino_slaves.values()
                else:
                    raise Exception("20091120 no longer possible")
                    self._slaves = []
                    for slave_name in self.slaves.split():
                        sl = get_slave(self.model,slave_name)
                        if sl is None:
                            lino.log.info(
                                "[Warning] invalid name %s in %s.slaves" % (
                                    slave_name,self.actor_id))
                        self._slaves.append(sl)
            else:
                self._slaves = []
                
        if self.button_label is None:
            self.button_label = self.label

        
    # implements actions.Action
    def get_url(self,ui,**kw):
        kw['run'] = True
        rh = self.get_handle(ui)
        return rh.get_absolute_url(**kw)
        #return ui.get_report_url(rh,**kw)
        
        
    #~ def get_action(self,name):
        #~ for a in self.actions:
            #~ if a.name == name:
                #~ return a
        #~ return actors.Actor.get_action(self,name)
              
    def add_actions(self,*args):
        """Used in Model.setup_report() to specify actions for each report on
        this model."""
        self.actions += args
        #~ for a in more_actions:
            #~ self._actions.append(a)
        
    #~ def unused_ext_components(self):
        #~ if len(self.store.layouts) == 2:
            #~ for s in self.store.layouts:
                #~ yield s._main
        #~ else:
            #~ yield self.store.layouts[0]._main
            #~ comps = [l._main for l in self.store.layouts[1:]]
            #~ yield extjs.TabPanel(None,"EastPanel",*comps)
            
        #~ yield self.layouts[0]._main
        #~ if len(self.layouts) == 2:
            #~ yield self.layouts[1]._main
        #~ else:
            #~ comps = [l._main for l in self.layouts[1:]]
            #~ yield layouts.TabPanel(None,"EastPanel",*comps)

        
            
    def get_title(self,rr):
        #~ if self.title is None:
            #~ return self.label
        
            
        title = self.title or self.label
        if rr is not None and self.master is not None:
            title += ": " + unicode(rr.master_instance)
        return title
        
    #~ def get_queryset(self,master_instance=None,quick_search=None,order_by=None,**kw):
    def get_queryset(self,rr):
        if self.queryset is not None:
            qs = self.queryset
        else:
            qs = self.model.objects.all()
        kw = self.get_master_kw(rr.master_instance,**rr.params)
        if kw is None:
            return []
        if len(kw):
            qs = qs.filter(**kw)

        if self.filter:
            qs = qs.filter(**self.filter)
        if self.exclude:
            qs = qs.exclude(**self.exclude)
              
        if rr.quick_search is not None:
            #~ qs = add_quick_search_filter(qs,self.model,rr.quick_search)
            qs = add_quick_search_filter(qs,rr.quick_search)
        order_by = rr.order_by or self.order_by
        if order_by:
            qs = qs.order_by(*order_by.split())
        return qs
        
        
    def setup_request(self,req):
        pass
        
    def get_master_kw(self,master_instance,**kw):
        #lino.log.debug('%s.get_master_kw(%r) master=%r',self,kw,self.master)
        if self.master is None:
            assert master_instance is None, "Report %s doesn't accept a master" % self.actor_id
        elif self.master is ContentType:
            if master_instance is None:
                kw[self.fk.ct_field] = None,
                kw[self.fk.fk_field] = None
            else:
                ct = ContentType.objects.get_for_model(master_instance.__class__)
                kw[self.fk.ct_field] = ct
                kw[self.fk.fk_field] = master_instance.pk
        else:
            if master_instance is None:
                if not self.fk.null:
                    return # cannot add rows to this report
                kw[self.fk.name] = master_instance
                
                #kw["%s__exact" % self.fk.name] = None
            elif not isinstance(master_instance,self.master):
                raise Exception("%r is not a %s" % (master_instance,self.master.__name__))
            else:
                kw[self.fk.name] = master_instance
        return kw
        
    def create_instance(self,req,**kw):
        instance = self.model(**kw)
        m = getattr(instance,'on_create',None)
        if m:
            m(req)
        #self.on_create(instance,req)
        return instance
        
    #~ def on_create(self,instance,req):
        #~ pass
        
    def getLabel(self):
        return self.label
        
    #~ def __str__(self):
        #~ return rc_name(self.__class__)
        
    def ajax_update(self,request):
        print request.POST
        return HttpResponse("1", mimetype='text/x-json')


    def as_text(self, *args,**kw):
        from lino.ui import console
        return console.ui.report_as_text(self)
        
    @classmethod
    def register_page_layout(cls,*layouts):
        cls.page_layouts = tuple(cls.page_layouts) + layouts
        
    def row2dict(self,row,d):
        "Overridden by lino.modlib.properties.PropValuesByOwner"
        for n in self.column_names.split():
            d[n] = getattr(row,n)
        return d
        
    def render_to_dict(self,**kw):
        #~ rh = self.get_handle(None) # ReportHandle(None,self)
        rr = self.request(None,**kw)
        return rr.render_to_dict()
        
    def request(self,ui,**kw):
        return self.get_handle(ui).request(**kw)

        
def report_factory(model):
    lino.log.debug('report_factory(%s) -> app_label=%r',model.__name__,model._meta.app_label)
    cls = type(model.__name__+"Report",(Report,),dict(model=model,app_label=model._meta.app_label))
    return actors.register_actor(cls())

#~ def choice_report_factory(model,field):
    #~ clsname = model.__name__+"_"+field.name+'_'+"Choices"
    #~ fldname = model._meta.app_label+'.'+model.__class__.__name__+'.'+field.name
    #~ return type(clsname,(Report,),dict(field=fldname,app_label=model._meta.app_label,column_names='__unicode__'))

def get_unbound_meth(cl,name):
    meth = getattr(cl,name,None)
    if meth is not None:
        return meth
    for b in cl.__bases__:
        meth = getattr(b,name,None)
        if meth is not None:
            return meth

