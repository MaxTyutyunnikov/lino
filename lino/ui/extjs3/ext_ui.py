# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import time
#import traceback
import cPickle as pickle
from urllib import urlencode
import codecs

#~ import Cheetah
from Cheetah.Template import Template as CheetahTemplate

from django import http
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.http import HttpResponse, Http404
from django import http
from django.core import exceptions
from django.utils import functional
from django.utils.encoding import force_unicode

from django.template.loader import get_template
from django.template import RequestContext

from django.utils.translation import ugettext as _
from django.utils import simplejson as json

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf.urls.defaults import patterns, url, include


import lino
from . import ext_elems
from . import ext_store
from . import ext_windows
#~ from . import ext_viewport
#~ from . import ext_requests
from lino.ui import requests as ext_requests
#~ from lino.ui import store as ext_store
from lino import actions #, layouts #, commands
from lino import reports
from lino import fields
from lino.ui import base
from lino.core import actors
from lino.utils import dblogger
from lino.utils import ucsv
from lino.utils import choosers
from lino.utils import babel
from lino.utils import menus
from lino.utils.config import find_config_file
from lino.utils import jsgen
from lino.utils.jsgen import py2js, js_code, id2js

from lino.utils.jscompressor import JSCompressor
if False:
    jscompress = JSCompressor().compress
else:    
    def jscompress(s): return s
      
from lino.mixins import printable

from lino.core.coretools import app_labels

from lino.fields import LANGUAGE_CHOICES
#~ from lino.modlib.properties.utils import STRENGTH_CHOICES, KNOWLEDGE_CHOICES

from lino.utils.choicelists import DoYouLike, HowWell
STRENGTH_CHOICES = DoYouLike.get_choices()
KNOWLEDGE_CHOICES = HowWell.get_choices()

from lino.tools import obj2str, obj2unicode

#~ from lino.ui.extjs.ext_windows import WindowConfig # 20100316 backwards-compat window_confics.pck 


class HttpResponseDeleted(HttpResponse):
    status_code = 204
    
def prepare_label(mi):
    label = unicode(mi.label) # trigger translation
    n = label.find(mi.HOTKEY_MARKER)
    if n != -1:
        label = label.replace(mi.HOTKEY_MARKER,'')
        #label=label[:n] + '<u>' + label[n] + '</u>' + label[n+1:]
    return label
    
        
#~ def element_name(elem):
    #~ return u"%s (#%s in %s.%s)" % (elem,elem.pk,elem._meta.app_label,elem.__class__.__name__)


def parse_bool(s):
    return s == 'true'
    
def parse_int(s,default=None):
    if s is None: return None
    return int(s)

def json_response_kw(msg=None,**kw):
    if msg:
        kw.update(message=msg)
    return json_response(kw)
    
def json_response(x):
    #s = simplejson.dumps(kw,default=unicode)
    #return HttpResponse(s, mimetype='text/html')
    s = py2js(x)
    #~ logger.debug("json_response() -> %r", s)
    # http://dev.sencha.com/deploy/dev/docs/source/BasicForm.html#cfg-Ext.form.BasicForm-fileUpload
    return HttpResponse(s, content_type='text/html')
    return HttpResponse(s, content_type='text/json')
    #~ r = HttpResponse(s, content_type='application/json')
    # see also http://stackoverflow.com/questions/477816/the-right-json-content-type
    #~ return r
    #~ return HttpResponse(s, mimetype='text/html')
    
def error_response(e,message=None,**kw):
    kw.update(success=False)
    if hasattr(e,'message_dict'):
        kw.update(errors=e.message_dict)
    #~ kw.update(alert_msg=cgi.escape(message_prefix+unicode(e)))
    kw.update(alert=True)
    
    kw.update(message=message)
    if message is None:
        message = unicode(e)
    kw.update(message=cgi.escape(message))
    #~ kw.update(message=message_prefix+unicode(e))
    dblogger.debug('error_response %s',kw)
    return json_response(kw)
    

def elem2rec1(ar,rh,elem,**rec):
    rec.update(data=rh.store.row2dict(ar,elem))
    return rec

def elem2rec_insert(ar,ah,elem):
    """
    Returns a dict of this record, designed for usage by an InsertWindow.
    """
    rec = elem2rec1(ar,ah,elem)
    #~ rec.update(title=_("Insert into %s...") % ar.get_title())
    rec.update(title=ar.get_action_title())
    #~ rec.update(id=elem.pk) or -99999)
    return rec

def elem2rec_detailed(ar,rh,elem,**rec):
    """
    Adds additional information for this record, used only by detail views.
    
    The "navigation information" is a set of pointers to the next, previous, 
    first and last record relativ to this record in this report. 
    (This information can be relatively expensive for records that are towards 
    the end of the report. 
    See :doc:`/blog/2010/0716`,
    :doc:`/blog/2010/0721`,
    :doc:`/blog/2010/1116`,
    :doc:`/blog/2010/1207`.)
    
    recno 0 means "the requested element exists but is not contained in the requested queryset".
    This can happen after changing the quick filter (search_change) of a detail view.
    
    """
    rec = elem2rec1(ar,rh,elem,**rec)
    rec.update(title=ar.get_title() + u" » " + unicode(elem))
    #~ rec.update(title=rh.report.model._meta.verbose_name + u"«%s»" % unicode(elem))
    #~ rec.update(title=unicode(elem))
    rec.update(id=elem.pk)
    #~ if rh.report.disable_delete:
    rec.update(disable_delete=rh.report.disable_delete(elem,ar.request))
    if rh.report.show_prev_next:
        first = None
        prev = None
        next = None
        last = None
        #~ ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)
        recno = 0
        if ar.total_count > 0:
            if True:
                # this algorithm is clearly quicker on reports with a few thousand Persons
                id_list = list(ar.queryset.values_list('pk',flat=True))
                assert len(id_list) == ar.total_count, \
                    "len(id_list) is %d while ar.total_count is %d" % (len(id_list),ar.total_count)
                first = id_list[0]
                last = id_list[-1]
                try:
                    i = id_list.index(elem.pk)
                except ValueError:
                    pass
                else:
                    recno = i + 1
                    if i > 0:
                        #~ prev = ar.queryset[i-1]
                        prev = id_list[i-1]
                    if i < ar.total_count - 1:
                        #~ next = ar.queryset[i+1]
                        next = id_list[i+1]
            else:
                first = ar.queryset[0]
                last = ar.queryset.reverse()[0]
                if ar.total_count > 200:
                    #~ TODO: check performance
                    pass
                g = enumerate(ar.queryset) # a generator
                try:
                    while True:
                        index, item = g.next()
                        if item == elem:
                            if index > 0:
                                prev = ar.queryset[index-1]
                            recno = index + 1
                            index,next = g.next()
                            break
                except StopIteration:
                    pass
                if first is not None: first = first.pk
                if last is not None: last = last.pk
                if prev is not None: prev = prev.pk
                if next is not None: next = next.pk
        rec.update(navinfo=dict(
            first=first,prev=prev,next=next,last=last,recno=recno,
            message=_("Row %(rowid)d of %(rowcount)d") % dict(rowid=recno,rowcount=ar.total_count)))
    return rec
            
    
    


class ExtUI(base.UI):
    _response = None
    name = 'extjs3'
    verbose_name = "ExtJS with Windows"
    Panel = ext_elems.Panel
    
    #~ USE_WINDOWS = False  # If you change this, then change also Lino.USE_WINDOWS in lino.js

    def __init__(self,*args,**kw):
        self.reserved_names = [getattr(ext_requests,n) for n in ext_requests.URL_PARAMS]
        jsgen.register_converter(self.py2js_converter)
        #~ self.window_configs = {}
        #~ if os.path.exists(self.window_configs_file):
            #~ logger.info("Loading %s...",self.window_configs_file)
            #~ wc = pickle.load(open(self.window_configs_file,"rU"))
            #~ #logger.debug("  -> %r",wc)
            #~ if type(wc) is dict:
                #~ self.window_configs = wc
        #~ else:
            #~ logger.warning("window_configs_file %s not found",self.window_configs_file)
            
        base.UI.__init__(self,*args,**kw) # will create a.window_wrapper for all actions
        
        #~ self.welcome_template = get_template('welcome.html')
        
        #~ from django.template.loader import find_template
        #~ source, origin = find_template('welcome.html')
        #~ print source, origin
        
        fn = find_config_file('welcome.html')
        logger.info("Using welcome template %s",fn)
        self.welcome_template = CheetahTemplate(file(fn).read())
        self.build_lino_js()
        
    def create_layout_element(self,lh,panelclass,name,**kw):
        
        #~ if name == "_":
            #~ return ext_elems.Spacer(lh,name,**kw)
            
        de = lh.rh.report.get_data_elem(name)
        #~ if de is None:
            #~ raise Exception("no data element %s in %s" % (name,lh.rh.report))
            
        #~ if isinstance(de,list):
            #~ for i in de:
                #~ return lh.desc2elem(panelclass,name,de.ct_field + ' ' + de.fk_field,**kw)
            
        if isinstance(de,actions.ImageAction):
            return ext_elems.PictureElement(lh,name,de,**kw)

        if isinstance(de,models.Field):
            if isinstance(de,(babel.BabelCharField,babel.BabelTextField)):
                if len(babel.BABEL_LANGS) > 0:
                    elems = [ self.create_field_element(lh,de,**kw) ]
                    for lang in babel.BABEL_LANGS:
                        bf = lh.rh.report.get_data_elem(name+'_'+lang)
                        elems.append(self.create_field_element(lh,bf,**kw))
                    return elems
            return self.create_field_element(lh,de,**kw)
        if isinstance(de,generic.GenericForeignKey):
            # create a horizontal panel with 2 comboboxes
            return lh.desc2elem(panelclass,name,de.ct_field + ' ' + de.fk_field,**kw)
            #~ return ext_elems.VirtualFieldElement(lh,name,de,**kw)
            
        if isinstance(de,reports.Report):
            if isinstance(lh.layout,reports.DetailLayout):
                # a Report in a DetailWindow
                kw.update(tools=[
                  js_code("Lino.report_window_button(ww,Lino.%s)" % de.default_action)
                ])
                if de.show_slave_grid:
                    # a Report in a DetailWindow, displayed as a Slave Grid
                    e = ext_elems.SlaveGridElement(lh,name,de,**kw)
                    #~ e = ext_elems.GridElement(lh,name,de.get_handle(self),**kw)
                    #~ lh.slave_grids.append(e)
                    return e
                    #~ return ext_elems.GridElementBox(lh,e)
                else:
                    # a Report in a DetailWindow, displayed as a summary in a HtmlBox 
                    o = dict(drop_zone="FooBar")
                    a = de.get_action('insert')
                    if a is not None:
                        kw.update(ls_insert_handler=js_code("Lino.%s" % a))
                        kw.update(ls_bbar_actions=[
                          self.a2btn(a),
                          ])
                    field = fields.HtmlBox(verbose_name=de.label,**o)
                    field.name = de._actor_name
                    field._return_type_for_method = de.slave_as_summary_meth(self,'<br>')
                    lh.add_store_field(field)
                    e = ext_elems.HtmlBoxElement(lh,field,**kw)
                    return e
            else:
                #~ field = fields.TextField(verbose_name=de.label)
                field = fields.HtmlBox(verbose_name=de.label)
                field.name = de._actor_name
                field._return_type_for_method = de.slave_as_summary_meth(self,', ')
                lh.add_store_field(field)
                e = ext_elems.HtmlBoxElement(lh,field,**kw)
                return e
                
        if isinstance(de,fields.VirtualField):
            return self.create_vurt_element(lh,name,de,**kw)
            
        if callable(de):
            rt = getattr(de,'return_type',None)
            if rt is not None:
                return self.create_meth_element(lh,name,de,rt,**kw)
                
        if not name in ('__str__','__unicode__','name','label'):
            value = getattr(lh.layout,name,None)
            if value is not None:
                if isinstance(value,basestring):
                    return lh.desc2elem(panelclass,name,value,**kw)
                if isinstance(value,reports.StaticText):
                    return ext_elems.StaticTextElement(lh,name,value)
                if isinstance(value,reports.DataView):
                    return ext_elems.DataViewElement(lh,name,value)
                    #~ return ext_elems.TemplateElement(lh,name,value)
                if isinstance(value,printable.PicturePrintMethod):
                    return ext_elems.PictureElement(lh,name,value)
                #~ if isinstance(value,layouts.PropertyGrid):
                    #~ return ext_elems.PropertyGridElement(lh,name,value)
                raise KeyError("Cannot handle value %r in %s.%s." % (value,lh.layout._actor_name,name))
        msg = "Unknown element %r referred in layout %s of %s" % (name,lh.layout,lh.rh.report)
        raise KeyError(msg)
        

    def create_vurt_element(self,lh,name,vf,**kw):
        #~ assert vf.get.func_code.co_argcount == 2, (name, vf.get.func_code.co_varnames)
        return self.create_field_element(lh,vf,**kw)
        
    def create_meth_element(self,lh,name,meth,rt,**kw):
        #~ if hasattr(rt,'_return_type_for_method'):
            #~ raise Exception(
              #~ "%s.%s : %r has already an attribute '_return_type_for_method'" % (
                #~ lh,name,rt))
        rt.name = name
        rt._return_type_for_method = meth
        if meth.func_code.co_argcount != 2:
            raise Exception("Method %s has %d arguments (must have 2)" % (meth,meth.func_code.co_argcount))
            #~ , (name, meth.func_code.co_varnames)
        #~ kw.update(editable=False)
        e = self.create_field_element(lh,rt,**kw)
        #~ if lh.rh.report.actor_id == 'contacts.Persons':
            #~ print 'ext_ui.py create_meth_element',name,'-->',e
        if name == 'preview':
            print 20110714, 'ext_ui.create_meth_element', meth, repr(e)
        return e
        #~ e = lh.main_class.field2elem(lh,return_type,**kw)
        #~ assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        #~ lh._store_fields.append(e.field)
        #~ return e
            
        #~ if rt is None:
            #~ rt = models.TextField()
            
        #~ e = ext_elems.MethodElement(lh,name,meth,rt,**kw)
        #~ assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        #~ lh._store_fields.append(e.field)
        #~ return e
          
    def create_field_element(self,lh,field,**kw):
        e = lh.main_class.field2elem(lh,field,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (lh.layout,name)
        lh.add_store_field(e.field)
        return e
        #return FieldElement(self,field,**kw)
        
    #~ def create_virt_element(self,name,field,**kw):
        #~ e = self.ui.VirtualFieldElement(self,name,field,**kw)
        #~ return e
        
    #~ def field2elem(self,lh,field,**kw):
        #~ # used also by lino.ui.extjs.ext_elem.MethodElement
        #~ return lh.main_class.field2elem(lh,field,**kw)
        #~ # return self.ui.field2elem(self,field,**kw)
        
    #~ def create_prop_element(self,lh,prop,**kw):
        #~ ...
      


    def main_panel_class(self,layout):
        if isinstance(layout,reports.ListLayout) : 
            return ext_elems.GridMainPanel
        #~ if isinstance(layout,layouts.TabLayout) : 
            #~ return ext_elems.TabMainPanel
        if isinstance(layout,reports.DetailLayout) : 
            return ext_elems.DetailMainPanel
        #~ if isinstance(layout,layouts.FormLayout) : 
            #~ return ext_elems.FormMainPanel
        raise Exception("No element class for layout %r" % layout)
            

    
    #~ def save_window_config(self,a,wc):
        #~ self.window_configs[str(a)] = wc
        #~ #a.window_wrapper.config.update(wc=wc)
        #~ a.window_wrapper.update_config(wc)
        #~ f = open(self.window_configs_file,'wb')
        #~ pickle.dump(self.window_configs,f)
        #~ f.close()
        #~ logger.debug("save_window_config(%r) -> %s",wc,a)
        #~ self.build_lino_js()
        #~ lh = actors.get_actor(name).get_handle(self)
        #~ if lh is not None:
            #~ lh.window_wrapper.try_apply_window_config(wc)
        #~ self._response = None

    #~ def load_window_config(self,action,**kw):
        #~ wc = self.window_configs.get(str(action),None)
        #~ if wc is not None:
            #~ logger.debug("load_window_config(%r) -> %s",str(action),wc)
            #~ for n in ('x','y','width','height'):
                #~ if wc.get(n,0) is None:
                    #~ del wc[n]
                    #~ #raise Exception('invalid window configuration %r' % wc)
            #~ kw.update(**wc)
        #~ return kw

  
    def get_urls(self):
        #~ urlpatterns = patterns('',
            #~ (r'^$', self.index_view))
        rx = '^'
        urlpatterns = patterns('',
            (rx+'$', self.index_view),
            (rx+r'grid_action/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<grid_action>\w+)$', self.json_report_view),
            (rx+r'grid_config/(?P<app_label>\w+)/(?P<actor>\w+)$', self.grid_config_view),
            (rx+r'detail_config/(?P<app_label>\w+)/(?P<actor>\w+)$', self.detail_config_view),
            (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)$', self.api_list_view),
            (rx+r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$', self.api_element_view),
            (rx+r'choices/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<fldname>\w+)$', self.choices_view),
        )
        if settings.LINO.use_tinymce:
            urlpatterns += patterns('',
                (rx+r'templates/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)$', 
                    self.templates_view),
                (rx+r'templates/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)/(?P<tplname>\w+)$', 
                    self.templates_view),
            )
            
            
        #~ if sys.platform == 'win32':
        if settings.LINO.extjs_root:
          
            logger.info("Running on a development server: install /media URLs ")
            

            if not os.path.exists(settings.LINO.extjs_root):
                raise Exception("EXTJS_ROOT %s does not exist" % settings.LINO.extjs_root)
                
            prefix = settings.MEDIA_URL[1:]
            assert prefix.endswith('/')
            
            urlpatterns += patterns('django.views.static',
            (r'^%sextjs/(?P<path>.*)$' % prefix, 
                'serve', {
                'document_root': settings.LINO.extjs_root,
                'show_indexes': True }))
                
            urlpatterns += patterns('django.views.static',
                (r'^%stinymce/(?P<path>.*)$' % prefix, 
                    'serve', {
                    'document_root': settings.LINO.tinymce_root,
                    'show_indexes': True }))
                
            LINO_MEDIA = os.path.abspath(os.path.join(
                os.path.dirname(lino.__file__),'..','media'))
            urlpatterns += patterns('django.views.static',
                (r'^%slino/(?P<path>.*)$' % prefix, 
                    'serve', {
                    'document_root': LINO_MEDIA,
                    'show_indexes': True }))

            urlpatterns += patterns('django.views.static',
                (r'^%s(?P<path>.*)$' % prefix, 'serve', 
                  { 'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
            )

        #~ print '\n'.join([repr(i) for i in urlpatterns])
        return urlpatterns

    def html_page(self,*args,**kw):
        return '\n'.join([ln for ln in self.html_lines(*args,**kw)])
        
    def html_lines(self,request,on_ready=[],**kw):
        #~ c = RequestContext(request,dict(site=self.site,lino=lino))
        self.welcome_template.ui = self
        self.welcome_template.user = request.user
        self.welcome_template.site = settings.LINO # self.site
        self.welcome_template.lino = lino
        #~ main=ext_elems.ExtPanel(
        main=dict(
          id="main_area",
          xtype='container',
          region="center",
          autoScroll=True,
          layout='fit',
          #~ html=self.welcome_template.render(c),
          html=unicode(self.welcome_template),
          #~ html=self.site.index_html.encode('ascii','xmlcharrefreplace'),
        )
        #~ if not on_ready:
            #~ on_ready = [
              #~ 'new Lino.IndexWrapper({html:%s}).show();' % 
                #~ py2js(self.site.index_html.encode('ascii','xmlcharrefreplace'))]
            #~ main.update(items=dict(layout='fit',html=self.site.index_html.encode('ascii','xmlcharrefreplace')))
        #~ main.update(id='main_area',region='center')
        yield '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        yield '<html><head>'
        yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
        #~ title = kw.get('title',None)
        #~ if title:
        yield '<title id="title">%s</title>' % settings.LINO.title
        #~ yield '<!-- ** CSS ** -->'
        #~ yield '<!-- base library -->'
        
        
        yield '<link rel="stylesheet" type="text/css" href="%s/extjs/resources/css/ext-all.css" />' % self.media_url()
        #~ yield '<!-- overrides to base library -->'
        if settings.LINO.use_vinylfox:
            p = self.media_url() + '/lino/vinylfox/'
            #~ p = self.media_url('lino','vinylfox') + '/'
            yield '<link rel="stylesheet" type="text/css" href="%sresources/css/htmleditorplugins.css" />' % p
          
        if settings.LINO.use_filterRow:
            p = self.media_url() + '/lino/filterRow'
            yield '<link rel="stylesheet" type="text/css" href="%s/filterRow.css" />' % p
            
        if settings.LINO.use_gridfilters:
            yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/statusbar/css/statusbar.css" />' % self.media_url() 
            yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/gridfilters/css/GridFilters.css" />' % self.media_url() 
            yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/gridfilters/css/RangeMenu.css" />' % self.media_url() 
            
        yield '<link rel="stylesheet" type="text/css" href="%s/extjs/examples/ux/fileuploadfield/css/fileuploadfield.css" />' % self.media_url() 
        
        yield '<link rel="stylesheet" type="text/css" href="%s/lino/extjs/lino.css">' % self.media_url()
        
        if settings.LINO.use_awesome_uploader:
            yield '<link rel="stylesheet" type="text/css" href="%s/lino/AwesomeUploader/AwesomeUploader.css">' % self.media_url()
            yield '<link rel="stylesheet" type="text/css" href="%s/lino/AwesomeUploader/AwesomeUploader Progress Bar.css">' % self.media_url()
         
        #~ yield '<!-- ** Javascript ** -->'
        #~ yield '<!-- ExtJS library: base/adapter -->'
        yield '<script type="text/javascript" src="%s/extjs/adapter/ext/ext-base.js"></script>' % self.media_url() 
        if settings.DEBUG:
            widget_library = 'ext-all-debug'
        else:
            widget_library = 'ext-all'
        #~ yield '<!-- ExtJS library: all widgets -->'
        yield '<script type="text/javascript" src="%s/extjs/%s.js"></script>' % (self.media_url(), widget_library)
        #~ if True:
            #~ yield '<style type="text/css">'
            #~ # http://stackoverflow.com/questions/2106104/word-wrap-grid-cells-in-ext-js 
            #~ yield '.x-grid3-cell-inner, .x-grid3-hd-inner {'
            #~ yield '  white-space: normal;' # /* changed from nowrap */
            #~ yield '}'
            #~ yield '</style>'
        if False:
            yield '<script type="text/javascript" src="%s/extjs/Exporter-all.js"></script>' % self.media_url() 
            
        if False:
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/CheckColumn.js"></script>' % self.media_url() 

        yield '<script type="text/javascript" src="%s/extjs/examples/ux/statusbar/StatusBar.js"></script>' % self.media_url()
        
        if settings.LINO.use_tinymce:
            p = self.media_url() + '/tinymce'
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            yield '<script type="text/javascript" src="%s/tiny_mce.js"></script>' % p
            yield '<script type="text/javascript" src="%s/lino/tinymce/Ext.ux.TinyMCE.js"></script>' % self.media_url()
            yield '''<script language="javascript" type="text/javascript">
tinymce.init({
        theme : "advanced"
        // , mode : "textareas"
});
</script>'''

        yield '<script type="text/javascript" src="%s/lino/extjs/Ext.ux.form.DateTime.js"></script>' % self.media_url()

        if settings.LINO.use_gridfilters:
            #~ yield '<script type="text/javascript" src="%s/extjs/examples/ux/RowEditor.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/gridfilters/menu/RangeMenu.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/gridfilters/menu/ListMenu.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/gridfilters/GridFilters.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/gridfilters/filter/Filter.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/gridfilters/filter/StringFilter.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/gridfilters/filter/DateFilter.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/gridfilters/filter/ListFilter.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/gridfilters/filter/NumericFilter.js"></script>' % self.media_url()
            yield '<script type="text/javascript" src="%s/extjs/examples/ux/gridfilters/filter/BooleanFilter.js"></script>' % self.media_url()
            
        yield '<script type="text/javascript" src="%s/extjs/examples/ux/fileuploadfield/FileUploadField.js"></script>' % self.media_url()
        
        if settings.LINO.use_filterRow:
            p = self.media_url() + '/lino/filterRow'
            yield '<script type="text/javascript" src="%s/filterRow.js"></script>' % p
            
        if settings.LINO.use_vinylfox:
            p = self.media_url() + '/lino/vinylfox/'
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.MidasCommand.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.Divider.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.HR.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.Image.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.RemoveFormat.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.IndentOutdent.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.SubSuperScript.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.FindAndReplace.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.Table.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.Word.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.Link.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.SpecialCharacters.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.UndoRedo.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.Heading.js"></script>' % p
            yield '<script type="text/javascript" src="%s/src/Ext.ux.form.HtmlEditor.Plugins.js"></script>' % p
            
        if settings.LINO.use_awesome_uploader:
            p = self.media_url() + '/lino/AwesomeUploader/'
            #~ yield '<script type="text/javascript" src="Ext.ux.form.FileUploadField.js"></script>'
            yield '<script type="text/javascript" src="%s/Ext.ux.XHRUpload.js"></script>' % p
            yield '<script type="text/javascript" src="%s/swfupload.js"></script>' % p
            yield '<!-- <script type="text/javascript" src="%s/swfupload.swfobject.js"></script> -->' % p
            yield '<script type="text/javascript" src="%s/Ext.ux.AwesomeUploaderLocalization.js"></script>' % p
            yield '<script type="text/javascript" src="%s/Ext.ux.AwesomeUploader.js"></script>' % p

        #~ yield '<!-- overrides to library -->'
        #~ yield '<script type="text/javascript" src="%slino/extjs/lino.js"></script>' % self.media_url()
        yield '<script type="text/javascript" src="%s"></script>' % (
            #~ self.media_url() + "/".join(self.lino_js_parts()))
            self.media_url(*self.lino_js_parts()))

        #~ yield '<!-- page specific -->'
        yield '<script type="text/javascript">'

        yield 'Ext.onReady(function(){'
        #~ yield "console.time('onReady');"
        
        #~ yield "Lino.load_mask = new Ext.LoadMask(Ext.getBody(), {msg:'Immer mit der Ruhe...'});"
          
        if True:
            
            win = dict(
              layout='fit',
              #~ maximized=True,
              items=main,
              #~ closable=False,
              bbar=dict(xtype='toolbar',items=js_code('Lino.status_bar')),
              #~ title=self.site.title,
              tbar=settings.LINO.get_site_menu(self,request.user),
            )
            
            for ln in jsgen.declare_vars(win):
                yield ln
            yield '  new Ext.Viewport({layout:"fit",items:%s}).render("body");' % py2js(win)
        else:
          
            comps = [
              #~ ext_elems.Toolbar(
              dict(xtype='toolbar',
                items=settings.LINO.get_site_menu(request.user),
                region='north',height=29),
              main,
              #~ jsgen.Component("konsole",
              dict(
                #~ xtype="panel",
                split=True,
                collapsible=True,
                collapsed=True,
                autoScroll=True,
                title=_("Console"),
                id="konsole",
                #~ html=_('Console started'),
                height=100,
                region="south")
            ]  
            for ln in jsgen.declare_vars(comps):
                yield '  ' + ln
            yield '  var viewport = new Ext.Viewport({layout:"border",items:%s});' % py2js(comps)
            
        yield '  Ext.QuickTips.init();'
        
        for ln in on_ready:
            yield ln
        
        #~ yield "console.timeEnd('onReady');"
        yield "}); // end of onReady()"
        yield '</script></head><body id="body">'
        #~ yield '<div id="tbar"/>'
        #~ yield '<div id="main"/>'
        #~ yield '<div id="bbar"/>'
        #~ yield '<div id="konsole"></div>'
        yield "</body></html>"
        
    def lino_js_lines(self):
        yield """// lino.js --- generated %s by Lino version %s.""" % (time.ctime(),lino.__version__)
        yield "Ext.BLANK_IMAGE_URL = '%s/extjs/resources/images/default/s.gif';" % self.media_url()
        yield "LANGUAGE_CHOICES = %s;" % py2js(list(LANGUAGE_CHOICES))
        yield "STRENGTH_CHOICES = %s;" % py2js(list(STRENGTH_CHOICES))
        yield "KNOWLEDGE_CHOICES = %s;" % py2js(list(KNOWLEDGE_CHOICES))
        yield "MEDIA_URL = %r;" % (self.media_url())
        #~ yield "ROOT_URL = %r;" % settings.LINO.root_url
        yield "ROOT_URL = %r;" % self.root_url
        #~ yield "API_URL = %r;" % self.build_url('api')
        #~ yield "TEMPLATES_URL = %r;" % self.build_url('templates')
        #~ yield "Lino.status_bar = new Ext.ux.StatusBar({defaultText:'Lino version %s.'});" % lino.__version__
        
            

    def index_view(self, request,**kw):
        #~ from lino.lino_site import lino_site
        #~ kw.update(title=lino_site.title)
        #~ mnu = py2js(lino_site.get_site_menu(request.user))
        #~ print mnu
        #~ tbar=ext_elems.Toolbar(items=lino_site.get_site_menu(request.user),region='north',height=29)# renderTo='tbar')
        return HttpResponse(self.html_page(request,**kw))
        #~ html = '\n'.join(self.html_page(request,main,konsole,**kw))
        #~ return HttpResponse(html)


    def unused_menu_view(self,request):
        "used only by lino.modlib.dsbe.tests"
        #~ from lino.lino_site import lino_site
        #~ from lino import lino_site
        return json_response_kw(success=True,
          message=(_("Welcome on Lino server %(title)r, user %(user)s") % dict(
            title=settings.LINO.title,
            user=request.user)),
          load_menu=settings.LINO.get_site_menu(request.user))
        #~ s = py2js(lino_site.get_menu(request))
        #~ return HttpResponse(s, mimetype='text/html')

    def form2obj_and_save(self,request,rh,data,elem,is_new): # **kw2save):
        """
        """
        #~ logger.info('form2obj_and_save %r', data)
        #~ print 'form2obj_and_save %r' % data
        
        # store normal form data (POST or PUT)
        try:
            rh.store.form2obj(request,data,elem,is_new)
        except exceptions.ValidationError,e:
            #~ raise
            return error_response(e)
           #~ return error_response(e,_("There was a problem while validating your data : "))
        #~ logger.info('store.form2obj passed')
        
        if not is_new:
            dblogger.log_changes(request,elem)
            
        #~ if hasattr(elem,'before_save'): # see :doc:`/blog/2010/0804`, :doc:`/blog/2011/0226`
            #~ elem.before_save()
            
        #~ logger.info('elem.before_save() passed')
        
        #~ print '20101024a', elem.card_valid_from
        try:
            elem.full_clean()
        except exceptions.ValidationError, e:
        #~ except Exception, e:
            return error_response(e) #,_("There was a problem while validating your data : "))
            #~ return json_response_kw(success=False,msg="Failed to save %s : %s" % (elem,e))
            
        #~ logger.info('elem.full_clean() passed')
        #~ print '20101024b', elem.card_valid_from

        kw2save = {}
        #~ kw2resp = {}
        if is_new:
            kw2save.update(force_insert=True)
            #~ kw2resp.update(close=True)
        else:
            kw2save.update(force_update=True)
            #~ kw2resp.update(refresh=True)
            
        try:
            elem.save(**kw2save)
        except IntegrityError,e:
            #~ print unicode(elem)
            #~ logger.exception(e)
            return error_response(e) # ,_("There was a problem while saving your data : "))
            #~ return json_response_kw(success=False,
                  #~ msg=_("There was a problem while saving your data:\n%s") % e)
        
        if is_new:
            dblogger.log_created(request,elem)
            return self.success_response(_("%s has been created.") % obj2unicode(elem),record_id=elem.pk)
            
        return self.success_response(_("%s has been saved.") % obj2unicode(elem))
        #~ return self.success_response(_("%s has been saved.") % obj2str(elem),**kw2resp)


        
    def detail_config_view(self,request,app_label=None,actor=None):
        rpt = actors.get_actor2(app_label,actor)
        if not rpt.can_config.passes(request.user):
            msg = _("User %(user)s cannot configure %(report)s.") % dict(user=request.user,report=rpt)
            return http.HttpResponseForbidden(msg)
        if request.method == 'GET':
            tab = int(request.GET.get('tab','0'))
            return json_response_kw(success=True,tab=tab,desc=rpt.detail_layouts[tab]._desc)
        if request.method == 'PUT':
            PUT = http.QueryDict(request.raw_post_data)
            tab = int(PUT.get('tab',0))
            desc = PUT.get('desc',None)
            if desc is None:
                return json_response_kw(success=False,message="desc is mandatory")
            rh = rpt.get_handle(self)
            try:
                rh.update_detail(tab,desc)
            except Exception,e:
                logger.exception(e)
                return json_response_kw(success=False,message=unicode(e),alert=True)
            self.build_lino_js()
            return json_response_kw(success=True)
            #detail_layout
      
    def grid_config_view(self,request,app_label=None,actor=None):
        rpt = actors.get_actor2(app_label,actor)
        if request.method == 'PUT':
            if not rpt.can_config.passes(request.user):
                msg = _("User %(user)s cannot configure %(report)s.") % dict(
                    user=request.user,report=rpt)
                return error_response(None,msg)
            #~ return http.HttpResponseForbidden(msg)
            PUT = http.QueryDict(request.raw_post_data)
            gc = dict(
              widths=[int(x) for x in PUT.getlist('widths')],
              columns=[str(x) for x in PUT.getlist('columns')],
              hiddens=[(x == 'true') for x in PUT.getlist('hiddens')],
              #~ hidden_cols=[str(x) for x in PUT.getlist('hidden_cols')],
            )
            
            filter = PUT.get('filter',None)
            if filter is not None:
                filter = json.loads(filter)
                gc['filters'] = [ext_requests.dict2kw(flt) for flt in filter]
            
            name = PUT.get('name',None)
            if name is None:
                name = ext_elems.DEFAULT_GC_NAME                 
            else:
                name = int(name)
                
            gc.update(label=PUT.get('label',"Standard"))
            try:
                msg = rpt.save_grid_config(name,gc)
            except IOError,e:
                msg = _("Error while saving GC for %(report)s: %(error)s") % dict(
                    report=rpt,error=e)
                return error_response(None,msg)
            #~ logger.info(msg)
            self.build_lino_js()            
            return self.success_response(msg)
            #~ return json_response_kw(success=True)
            
        raise NotImplementedError
        
        
    def api_list_view(self,request,app_label=None,actor=None):
        """
        - GET : List the members of the collection. 
        - PUT : Replace the entire collection with another collection. 
        - POST : Create a new entry in the collection where the ID is assigned automatically by the collection. 
          The ID created is included as part of the data returned by this operation. 
        - DELETE : Delete the entire collection.
        
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        rpt = actors.get_actor2(app_label,actor)
        rh = rpt.get_handle(self)
        
        #~ if not rh.report.can_view.passes(request.user):
            #~ msg = _("User %(user)s cannot view %(report)s.") % dict(user=request.user,report=rpt)
            #~ return http.HttpResponseForbidden()
        if request.method == 'POST':
            #~ data = rh.store.get_from_form(request.POST)
            #~ instance = ar.create_instance(**data)
            #~ ar = ext_requests.ViewReportRequest(request,rh,rh.report.list_action)
            ar = ext_requests.ViewReportRequest(request,rh,rh.report.default_action)
            instance = ar.create_instance()
            # store uploaded files. 
            # html forms cannot send files with PUT or GET, only with POST
            if rh.report.handle_uploaded_files is not None:
                rh.report.handle_uploaded_files(request,instance)
            return self.form2obj_and_save(request,rh,request.POST,instance,True)
            
        if request.method == 'GET':
          
            action_name = request.GET.get('an','grid')
            a = rpt.get_action(action_name)
            if a is None:
                raise Http404("%s has no action %r" % (rpt,action_name))
                
            fmt = request.GET.get('fmt',a.default_format)
          
            #~ fmt = request.GET.get('fmt',None)
            #~ if fmt is None:
                #~ a = rpt.default_action
            #~ else:
                #~ a = rpt.get_action(fmt) 
            #~ if a is not None:
            ar = ext_requests.ViewReportRequest(request,rh,a)
            
            #~ print '20110714', a, fmt
            
            if fmt == 'html':
                kw = {}
                bp = self.request2kw(ar)
                
                params = dict(base_params=bp)
                
                if isinstance(a,reports.InsertRow):
                    elem = ar.create_instance()
                    #~ rec = elem2rec1(ar,rh,elem,title=ar.get_title())
                    rec = elem2rec_insert(ar,rh,elem)
                    rec.update(phantom=True)
                    params.update(data_record=rec)

                kw.update(on_ready=['Lino.%s(undefined,%s);' % (a,py2js(params))])
                #~ print '20110714 on_ready', params
                return HttpResponse(self.html_page(request,**kw))
            
            if fmt == 'csv':
                #~ response = HttpResponse(mimetype='text/csv')
                charset = settings.LINO.csv_params.get('encoding','utf-8')
                response = HttpResponse(content_type='text/csv;charset="%s"' % charset)
                if False:
                    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % ar.report
                else:
                    #~ response = HttpResponse(content_type='application/csv')
                    response['Content-Disposition'] = 'inline; filename="%s.csv"' % ar.report
                  
                #~ response['Content-Disposition'] = 'attachment; filename=%s.csv' % ar.get_base_filename()
                w = ucsv.UnicodeWriter(response,**settings.LINO.csv_params)
                w.writerow(ar.ah.store.column_names())
                for row in ar.queryset:
                    w.writerow([unicode(v) for v in ar.row2list(row)])
                return response
                
            if fmt == 'json':
                rows = [ ar.row2list(row) for row in ar.queryset ]
                #~ rows = [ ar.row2dict(row) for row in ar.queryset ]
                total_count = ar.total_count
                #logger.debug('%s.render_to_dict() total_count=%d extra=%d',self,total_count,self.extra)
                # add extra blank row(s):
                #~ for i in range(0,ar.extra):
                if ar.create_rows:
                    row = ar.create_instance()
                    d = ar.row2list(row)
                    #~ d = ar.row2dict(row)
                    #~ 20100706 d[rh.report.model._meta.pk.name] = -99999
                    rows.append(d)
                    total_count += 1
                return json_response_kw(count=total_count,
                  rows=rows,
                  title=unicode(ar.get_title()),
                  gc_choices=[gc.data for gc in rpt.grid_configs])
                    
            raise Http404("Format %r not supported for GET on %s" % (fmt,rpt))


        raise Http404("Method %s not supported for container %s" % (request.method,rh))
    
    
        
        
    def api_element_view(self,request,app_label=None,actor=None,pk=None):
        """
        GET : Retrieve a representation of the addressed member of the collection expressed in an appropriate MIME type.
        PUT : Update the addressed member of the collection or create it with the specified ID. 
        POST : Treats the addressed member as a collection and creates a new subordinate of it. 
        DELETE : Delete the addressed member of the collection. 
        
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        rpt = actors.get_actor2(app_label,actor)
        if rpt is None:
            model = models.get_model(app_label,actor,False)
            if model is None:
                raise Http404("No actor named '%s.%s'" % (app_label,actor))
            rpt = model._lino_model_report
        ah = rpt.get_handle(self)
        #~ if not ah.report.can_view.passes(request.user):
            #~ msg = "User %s cannot view %s." % (request.user,ah.report)
            #~ return http.HttpResponseForbidden()
            
        elem = None
        
        if pk != '-99999':
            try:
                elem = rpt.model.objects.get(pk=pk)
            except ValueError:
                msg = "Invalid primary key %r for %s.%s." % (pk,rpt.model._meta.app_label,rpt.model.__name__)
                raise Http404(msg)
            except rpt.model.DoesNotExist:
                raise Http404("%s %s does not exist." % (rpt,pk))
                
        if request.method == 'DELETE':
            #~ if rpt.disable_delete is not None:
            msg = rpt.disable_delete(elem,request)
            if msg is not None:
                return error_response(None,msg)
                    
            dblogger.log_deleted(request,elem)
            
            try:
                elem.delete()
            except Exception,e:
                dblogger.exception(e)
                msg = _("Failed to delete %(record)s : %(error)s.") % dict(record=obj2unicode(elem),error=e)
                #~ msg = "Failed to delete %s." % element_name(elem)
                return error_response(None,msg)
                #~ raise Http404(msg)
            return HttpResponseDeleted()
            
        if request.method == 'PUT':
            if elem is None:
                raise Http404('Tried to PUT on element -99999')
            #~ print 20110301, request.raw_post_data
            data = http.QueryDict(request.raw_post_data)
            #~ print 20110301, data
            #~ fmt = data.get('fmt',None)
            return self.form2obj_and_save(request,ah,data,elem,False) # force_update=True)
            
        if request.method == 'GET':
            #~ # before 20110713
            #~ ar = ext_requests.ViewReportRequest(request,ah,ah.report.default_action)
            
            #~ if pk == '-99999':
                #~ elem = ar.create_instance()
            
            #~ fmt = request.GET.get('fmt',None)
            #~ if pk == '-99999':
                #~ datarec = elem2rec_insert(ar,ah,elem)
            #~ else:
                #~ datarec = elem2rec_detailed(ar,ah,elem)
            #~ if fmt is None or fmt == 'json':
                #~ return json_response(datarec)
                    
            action_name = request.GET.get('an','detail')
            #~ if action_name is None:
                #~ a = rpt.default_action
            #~ else:
            a = rpt.get_action(action_name)
            if a is None:
                raise Http404("%s has no action %r" % (rpt,action_name))
                
            fmt = request.GET.get('fmt',a.default_format)
            #~ a = rpt.get_action(fmt)
                
            ar = ext_requests.ViewReportRequest(request,ah,a)
            
            #~ if fmt == 'json':
              
                #~ if isinstance(a,reports.InsertRow):
                    #~ elem = ar.create_instance()
                    #~ datarec = elem2rec_insert(ar,ah,elem)
                    #~ return json_response(datarec)
                    
                #~ if elem is None:
                    #~ raise Http404('Tried to GET element -99999')
                #~ datarec = elem2rec_detailed(ar,ah,elem)
                #~ return json_response(datarec)
                
                
            #~ if elem is None:
                #~ raise Http404('Tried to GET element -99999')

            if isinstance(a,actions.OpenWindowAction):
              
                if elem is None:
                    elem = ar.create_instance()
                    datarec = elem2rec_insert(ar,ah,elem)
                else:
                    datarec = elem2rec_detailed(ar,ah,elem)
                
                if fmt == 'json':
                    return json_response(datarec)
                    
                params = dict(data_record=datarec)
                bp = self.request2kw(ar)
                if a.window_wrapper.tabbed:
                    tab = request.GET.get(ext_requests.URL_PARAM_TAB,None)
                    if tab is not None: 
                        tab = int(tab)
                        params.update(active_tab=tab)
                params.update(base_params=bp)
                return HttpResponse(self.html_page(request,on_ready=['Lino.%s(undefined,%s);' % (a,py2js(params))]))
                
                
            if isinstance(a,actions.RedirectAction):
                target = a.get_target_url(elem)
                if target is None:
                    raise Http404("%s failed for %r" % (a,elem))
                return http.HttpResponseRedirect(target)
                
            if isinstance(a,reports.RowAction):
                #~ return a.run(ar,elem)
                try:
                    return a.run(ar,elem)
                except Exception,e:
                    logger.exception(e)
                    msg = _("Action %(action)s failed for %(record)s.") % dict(
                        action=a,
                        record=obj2unicode(elem))
                    msg += ' ' + _("An error report has been sent to the system administrator.")
                    logger.warning(msg)
                    return error_response(e,msg)
              
            raise NotImplementedError("Action %s is not implemented)" % a)
                
              
        return error_response(None,
            "Method %r not supported for elements of %s." % (
                request.method,ah.report))
        #~ raise Http404("Method %r not supported for elements of %s" % (request.method,ah.report))
        
        
    def error_response(self,*args,**kw):
        kw.update(success=False)
        return error_response(*args,**kw)
        
    def success_response(self,*args,**kw):
        kw.update(success=True)
        return json_response_kw(*args,**kw)
        
    def lino_js_parts(self):
    #~ def js_cache_name(self):
        #~ return ('cache','js','site.js')
        return ('cache','js','lino.js')
        
    def build_lino_js(self):
        """Generate the :xfile:`lino.js`.
        """
        #~ for app_label in site.
        fn = os.path.join(settings.MEDIA_ROOT,*self.lino_js_parts()) 
        #~ fn = r'c:\temp\dsbe.js'
        if False:
            # useful when debugging directly on the generated lino.js
            logger.info("NOT generating %s ...", fn)
            return 
        if not os.path.isdir(settings.MEDIA_ROOT):
            logger.warning("Directory '%s' (settings.MEDIA_ROOT) does not exist.", settings.MEDIA_ROOT)
            return
        
        logger.info("Generating %s ...", fn)
        
        f = codecs.open(fn,'w',encoding='utf-8')
        
        for ln in self.lino_js_lines():
            #~ js += ln + '\n'
            f.write(ln + '\n')
        
        libname = os.path.join(os.path.dirname(__file__),'linolib.js')
        tpl = CheetahTemplate(codecs.open(libname,encoding='utf-8').read())
        tpl.ui = self
            
        def mytranslate(s):
            settings.LINO.add_dummy_message(s)
            return _(s)
        tpl._ = mytranslate
        #~ tpl.user = request.user
        tpl.site = settings.LINO
        tpl.settings = settings
        tpl.lino = lino
        tpl.ext_requests = ext_requests
        for k in ext_requests.URL_PARAMS:
            setattr(tpl,k,getattr(ext_requests,k))
        f.write(jscompress(unicode(tpl)+'\n'))
        
        # the following takes a few seconds more time when using 
        # one big unicode string `js`.
        #~ js = u''
        for rpt in reports.master_reports + reports.slave_reports + reports.generic_slaves.values():
            rh = rpt.get_handle(self) # make sure that setup_handle is called (which adds the window_wrapper)
            #~ js += "Ext.namespace('Lino.%s')\n" % rpt
            f.write("Ext.namespace('Lino.%s')\n" % rpt)
            for a in rpt.get_actions():
                if a.window_wrapper is not None:
                    #~ print a, "..."
                    #~ f.write('Lino.%s = ' % a )
                    for ln in a.window_wrapper.js_render():
                        f.write(ln + '\n')
                        #~ js += ln + "\n"
                    #~ js += "\n"
                    f.write('\n')
                    
        #~ f.write(jscompress(js))
        f.close()
        logger.info("Wrote %s ...", fn)
        
        from lino.core.kernel import generate_dummy_messages
        generate_dummy_messages(settings.LINO)
        
    def templates_view(self,request,app_label=None,actor=None,pk=None,fldname=None,tplname=None,**kw):
      
        if request.method == 'GET':
            from lino.models import TextFieldTemplate
            if tplname:
                tft = TextFieldTemplate.objects.get(pk=int(tplname))
                return HttpResponse(tft.text)
                
            rpt = actors.get_actor2(app_label,actor)
            if rpt is None:
                model = models.get_model(app_label,actor,False)
                rpt = model._lino_model_report
            try:
                elem = rpt.model.objects.get(pk=pk)
            except ValueError:
                msg = "Invalid primary key %r for %s.%s." % (pk,rpt.model._meta.app_label,rpt.model.__name__)
                raise Http404(msg)
            except rpt.model.DoesNotExist:
                raise Http404("%s %s does not exist." % (rpt,pk))
                
            #~ TextFieldTemplate.templates
            m = getattr(elem,"%s_templates" % fldname,None)
            #~ m = getattr(rpt.model,"%s_templates" % fldname,None)
            if m is None:
                q = models.Q(user=request.user) | models.Q(user=None)
                #~ q = models.Q(user=request.user)
                qs = TextFieldTemplate.objects.filter(q).order_by('name')
            else:
                qs = m(request)
                
            templates = []
            for obj in qs:
                url = self.build_url('templates',app_label,actor,pk,fldname,unicode(obj.pk))
                templates.append([unicode(obj.name),url,unicode(obj.description)])
            js = "var tinyMCETemplateList = %s;" % py2js(templates)
            return HttpResponse(js,content_type='text/json')
        raise Http404("Method %r not supported" % request.method)
        
    def choices_view(self,request,app_label=None,rptname=None,fldname=None,**kw):
        rpt = actors.get_actor2(app_label,rptname)
        #~ rh = rpt.get_handle(self)
        field = rpt.model._meta.get_field(fldname)
        chooser = choosers.get_for_field(field)
        if chooser:
            qs = chooser.get_request_choices(request)
            assert qs is not None, "%s.%s_choices() returned None" % (rpt.model,fldname)
        elif field.choices:
            qs = field.choices
        elif isinstance(field,models.ForeignKey):
            m = field.rel.to
            cr = getattr(m,'_lino_choices_report',m._lino_model_report)
            qs = cr.request(self).get_queryset()
            #~ qs = mr.request(self,**mr.default_params).get_queryset()
            #~ qs = get_default_qs(field.rel.to)
            #~ qs = field.rel.to.objects.all()
        else:
            raise Http404("No choices for %s" % fldname)
        #~ for k,v in request.GET.items():
            #~ kw[str(k)] = v
        #~ chooser = rh.choosers[fldname]
        #~ qs = chooser.get_choices(**kw)
        quick_search = request.GET.get(ext_requests.URL_PARAM_FILTER,None)
        if quick_search is not None:
            qs = reports.add_quick_search_filter(qs,quick_search)
        if chooser:
            if chooser.simple_values:
                def row2dict(obj,d):
                    #~ d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                    d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
                    return d
            elif chooser.instance_values:
                # same code as for ForeignKey
                def row2dict(obj,d):
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                    d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                    return d
            else:
                def row2dict(obj,d):
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                    d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
                    return d
        elif isinstance(field,models.ForeignKey):
            def row2dict(obj,d):
                d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                return d
        else:
            def row2dict(obj,d):
                if type(obj) is list or type(obj) is tuple:
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                    d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
                else:
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                    d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
                return d
        rows = [ row2dict(row,{}) for row in qs ]
        return json_response_kw(count=len(rows),rows=rows,title=_('Choices for %s') % fldname)
        

    def unused_form_submit_view(self,request,**kw):
        kw['submit'] = True
        return self.json_report_view(request,**kw)

    def list_report_view(self,request,**kw):
        #kw['simple_list'] = True
        return self.json_report_view(request,**kw)
        
    #~ def csv_report_view(self,request,**kw):
        #~ kw['csv'] = True
        #~ return self.json_report_view(request,**kw)
        
    def json_report_view(self,request,app_label=None,rptname=None,**kw):
        rpt = actors.get_actor2(app_label,rptname)
        return self.json_report_view_(request,rpt,**kw)

    def json_report_view_(self,request,rpt,grid_action=None,colname=None,submit=None,choices_for_field=None,csv=False):
        if not rpt.can_view.passes(request):
            msg = "User %s cannot view %s." % (request.user,rpt)
            raise Http404(msg)
            #~ return json_response_kw(success=False,msg=msg)
                
        rh = rpt.get_handle(self)
        
        if grid_action:
            a = rpt.get_action(grid_action)
            assert a is not None, "No action %s in %s" % (grid_action,rh)
            ar = ext_requests.ViewReportRequest(request,rh,a)
            return json_response(ar.run())
            #~ return json_response(ar.run().as_dict())
                
        if choices_for_field:
            rptreq = ext_requests.ChoicesReportRequest(request,rh,choices_for_field)
        elif csv:
            rptreq = ext_requests.CSVReportRequest(request,rh,rpt.default_action)
            return rptreq.render_to_csv()
        else:
            rptreq = ext_requests.ViewReportRequest(request,rh,rpt.default_action)
            if submit:
                pk = request.POST.get(rh.store.pk.name) #,None)
                #~ if pk == reports.UNDEFINED:
                    #~ pk = None
                try:
                    data = rh.store.get_from_form(request.POST)
                    if pk in ('', None):
                        #return json_response(success=False,msg="No primary key was specified")
                        instance = rptreq.create_instance(**data)
                        instance.save(force_insert=True)
                    else:
                        instance = rpt.model.objects.get(pk=pk)
                        for k,v in data.items():
                            setattr(instance,k,v)
                        instance.save(force_update=True)
                    return json_response_kw(success=True,
                          message="%s has been saved" % instance)
                except Exception,e:
                    logger.exception(e)
                    #traceback.format_exc(e)
                    return error_response(e) #,_("There was a problem while saving your data : "))
                    #~ return error_response(e)
                    #~ return json_response_kw(success=False,msg="Exception occured: "+cgi.escape(str(e)))
        # otherwise it's a simple list:
        #~ print 20100406, rptreq
        d = rptreq.render_to_dict()
        return json_response(d)
        

    def get_choices_url(self,fke,**kw):
        return self.build_url("choices",
            fke.lh.rh.report.app_label,
            fke.lh.rh.report._actor_name,
            fke.field.name,**kw)
        
    def request2kw(self,rr,**kw):
        #~ if rr.known_values is not None:
            #~ for k,v in rr.known_values.items():
            #~ kw.update(rr.known_values)
            #~ # kw[ext_requests.URL_KNOWN_VALUES] = rr.known_values
        if rr.quick_search:
            kw[ext_requests.URL_PARAM_FILTER] = rr.quick_search
        if rr.master_instance is not None:
            kw[ext_requests.URL_PARAM_MASTER_PK] = rr.master_instance.pk
            mt = ContentType.objects.get_for_model(rr.master_instance.__class__).pk
            kw[ext_requests.URL_PARAM_MASTER_TYPE] = mt
        return kw
        
    def action_href(self,a,label=None,**params):
        if label is None:
            label = a.button_label
        onclick = 'Lino.%s(undefined,%s)' % (a,py2js(params))
        #~ print 20110120, onclick
        onclick = cgi.escape(onclick)
        onclick = onclick.replace('"','&quot;')
        #~ return '<input type="button" onclick="%s" value=" %s ">' % (onclick,label)
        #~ return '[<a href="#" onclick="%s">%s</a>]' % (onclick,label)
        return '[<a href="javascript:%s">%s</a>]' % (onclick,label)
        
        
    def quick_upload_buttons(self,rr):
        """
        Deserves more documentation.
        """
        if rr.total_count == 0:
            #~ return [dict(text="Upload",handler=js_code('Lino.%s' % rr.report.get_action('insert')))]
            a = rr.report.get_action('insert')
            if a is not None:
                #~ params = dict(base_params=self.request2kw(v))
                rec = rr.create_instance()
                #~ params = dict(data_record=elem2rec1(rr,rr.ah,rec))
                params = dict(data_record=elem2rec_insert(rr,rr.ah,rec))
                #~ params = dict(data_record=elem2rec_detailed(rr,rr.ah,rec))
                return self.action_href(a,_("Upload"),**params)
        if rr.total_count == 1:
            #~ return [dict(text="Show",handler=js_code('Lino.%s' % v.report.get_action('detail')))]
            #~ s = unicode(v[0]) + ':'
            s = ''
            s += ' [<a href="%s" target="_blank">show</a>]' % (self.media_url(rr[0].file.name))
            #~ s += ' [<a href="%s" target="_blank">edit</a>]' % (self.get_detail_url(rr[0],fmt='detail'))
            #~ params = dict(data_record=elem2rec1(rr,rr.ah,rr[0]))
            params = dict(data_record=elem2rec_detailed(rr,rr.ah,rr[0]))
            s += ' ' + self.action_href(rr.ah.report.detail_action,_("Edit"),**params)
            return s
        return '[?!]'
        
      
    def py2js_converter(self,v):
        if v is LANGUAGE_CHOICES:
            return js_code('LANGUAGE_CHOICES')
        if v is STRENGTH_CHOICES:
            return js_code('STRENGTH_CHOICES')
        if v is KNOWLEDGE_CHOICES:
            return js_code('KNOWLEDGE_CHOICES')
        if isinstance(v,babel.BabelChoice):
            #~ v = unicode(v)
            return v.value
        if isinstance(v,Exception):
            return unicode(v)
        if isinstance(v,menus.Menu):
            if v.parent is None:
                return v.items
                #kw.update(region='north',height=27,items=v.items)
                #return py2js(kw)
            return dict(text=prepare_label(v),menu=dict(items=v.items))
        if isinstance(v,menus.MenuItem):
            if v.href is not None:
                return dict(text=prepare_label(v),href=v.href)
            if True: 
                """
                20110129. In this case, the main menu uses permalinks instead of opening new windows each time.
                """
                if v.request is not None:
                    url = self.get_request_url(v.request)
                elif v.instance is not None:
                    #~ url = self.get_detail_url(v.instance,an='detail')
                    url = self.get_detail_url(v.instance)
                else:
                    url = self.get_action_url(v.action)
                    #~ url = self.build_url('api',v.action.actor.app_label,v.action.actor._actor_name,fmt=v.action.name)
                return dict(text=prepare_label(v),href=url)
            # no longer supported:
            handler = "function(btn,evt){Lino.%s(undefined,%s)}" % (v.action,py2js(v.params))
            return dict(text=prepare_label(v),handler=js_code(handler))
        return v
        

    def get_action_url(self,action,*args,**kw):
        #~ if not action is action.actor.default_action:
        if action != action.actor.default_action:
            kw.update(an=action.name)
        return self.build_url("api",action.actor.app_label,action.actor._actor_name,*args,**kw)
            
    def get_actor_url(self,actor,*args,**kw):
        return self.build_url("api",actor.app_label,actor._actor_name,*args,**kw)
        
    def get_request_url(self,rr,*args,**kw):
        kw = self.request2kw(rr,**kw)
        return self.build_url('api',rr.report.app_label,rr.report._actor_name,*args,**kw)
        
    def get_detail_url(self,obj,*args,**kw):
        #~ rpt = obj._lino_model_report
        #~ return self.build_url('api',rpt.app_label,rpt._actor_name,str(obj.pk),*args,**kw)
        return self.build_url('api',obj._meta.app_label,obj.__class__.__name__,str(obj.pk),*args,**kw)
        
    def href_to(self,obj,text=None):
        return self.href(
            self.get_detail_url(obj),
            text or cgi.escape(force_unicode(obj)))
        #~ return '<a href="%s" target="_blank">%s</a>' % (self.get_detail_url(obj,fmt='detail'),unicode(obj))

    def href(self,url,text):
        return '<a href="%s">%s</a>' % (url,text)
    
    #~ def detail_href(self,obj,**kw):
        #~ return '<a href="%s">%s</a>' % (self.get_detail_url(obj,fmt='detail'),cgi.escape(unicode(obj))))
        
    def action_window_wrapper(self,a,h):
        #~ if isinstance(a,actions.DeleteSelected): return ext_windows.DeleteRenderer(self,a)
        #~ if isinstance(a,actions.UpdateRowAction): return ext_windows.UpdateRowRenderer(self,a)
          
        if isinstance(a,reports.GridEdit):
            return ext_windows.GridMasterWrapper(h,a)
            
        if isinstance(a,reports.InsertRow):
            return ext_windows.InsertWrapper(h,a)
            
        if isinstance(a,reports.ShowDetailAction):
            return ext_windows.DetailWrapper(h,a)
            
    def setup_handle(self,h):
        #~ if isinstance(h,layouts.TabPanelHandle):
            #~ h._main = ext_elems.TabPanel([l.get_handle(self) for l in h.layouts])
          
        if isinstance(h,reports.ReportHandle):
            #~ logger.debug('ExtUI.setup_handle() %s',h.report)
            if h.report.model is None or h.report.model._meta.abstract:
                return
            #~ h.choosers = chooser.get_choosers_for_model(h.report.model,chooser.FormChooser)
            #~ h.report.add_action(ext_windows.SaveWindowConfig(h.report))
            h.store = ext_store.Store(h)
                    
            for a in h.get_actions():
                a.window_wrapper = self.action_window_wrapper(a,h)
                
            for de in h.data_elems():
                if de.name in self.reserved_names:
                    raise Exception(
                      "%s defines %r but that is a reserved name in lino.ui.extjs" % (
                      h.report,de.name))
                
    def source_dir(self):
        return os.path.abspath(os.path.dirname(__file__))
        
    def a2btn(self,a,**kw):
        if isinstance(a,reports.SubmitDetail):
            #~ kw.update(panel_btn_handler=js_code('Lino.submit_detail'))
            kw.update(handler=js_code('function() {ww.save()}'))
            #~ kw.update(handler=js_code('ww.save'),scope=js_code('ww'))
        elif isinstance(a,reports.SubmitInsert):
            kw.update(handler=js_code('function() {ww.save()}'))
            #~ kw.update(handler=js_code('ww.save'),scope=js_code('ww'))
            #~ kw.update(panel_btn_handler=js_code('Lino.submit_insert'))
        #~ elif isinstance(a,actions.UpdateRowAction):
            #~ kw.update(panel_btn_handler=js_code('Lino.update_row_handler(%r)' % a.name))
        elif isinstance(a,reports.ShowDetailAction):
            kw.update(panel_btn_handler=js_code('Lino.show_detail_handler'))
            #~ kw.update(panel_btn_handler=js_code('Lino.show_detail_handler()'))
            #~ kw.update(panel_btn_handler=js_code('function(panel){Lino.show_detail(panel)}'))
        elif isinstance(a,reports.InsertRow):
            kw.update(must_save=True)
            kw.update(panel_btn_handler=js_code(
                'function(panel){Lino.show_insert(panel)}'))
            #~ kw.update(panel_btn_handler=js_code("Lino.show_insert_handler(Lino.%s)" % a))
        elif isinstance(a,reports.DuplicateRow):
            kw.update(panel_btn_handler=js_code(
                'function(panel){Lino.show_insert_duplicate(panel)}'))
        elif isinstance(a,reports.DeleteSelected):
            kw.update(panel_btn_handler=js_code(
                "Lino.delete_selected" % a))
        #~ elif isinstance(a,actions.RedirectAction):
            #~ kw.update(panel_btn_handler=js_code("Lino.show_download_handler(%r)" % a.name))
        elif isinstance(a,reports.RowAction):
            kw.update(must_save=True)
            kw.update(panel_btn_handler=js_code("Lino.row_action_handler(%r)" % a.name))
        else:
            kw.update(panel_btn_handler=js_code("Lino.%s" % a))
        kw.update(
          text=unicode(a.label),
        )
        return kw
        
