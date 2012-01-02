## Copyright 2009-2012 Luc Saffre
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
import sys
#~ import imp
import codecs
#~ import collections
from UserDict import IterableUserDict

from django.db.models import loading
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.functional import LazyObject
from django.db import models
#from django.shortcuts import render_to_response 
#from django.contrib.auth.models import User


from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from django.utils.http import urlquote, base36_to_int
from django.utils.translation import ugettext as _

from django.conf.urls.defaults import patterns, url, include
#~ auth = models.get_app('auth')
#~ from django.contrib.auth import models as auth
#~ from lino.modlib.users import models as auth

from django.utils.safestring import mark_safe

import lino
        
from lino.core import table
from lino.utils import perms
from lino.utils import dblogger
#~ from lino.utils import babel
from lino.core import actors
from lino.core.coretools import app_labels # , data_elems # , get_unbound_meth
from lino.utils import get_class_attr, class_dict_items

from lino.tools import resolve_model, resolve_field, get_app, get_field, full_model_name
from lino.utils.config import load_config_files, find_config_file
from lino.utils import choosers
from lino import dd
#~ from lino.models import get_site_config
from lino.utils import babel

def analyze_models(self,make_messages):
    """
    This is a part of a Lino site setup.
    The Django Model definitions are done, now Lino analyzes them and does certain actions.
    The parameter `self` is the :class:`lino.Lino` instance 
    defined in `settings.LINO`.
    
    - Load .dtl files and install them into `_lino_detail_layouts`
    - Install a DisableDeleteHandler for each Model into  `_lino_ddh`
    
    """
    
    ## The following causes django.db.models.loading.cache to 
    ## be populated. This must be done before calling actors.discover() 
    ## or resolve_model().

    models_list = models.get_models() # trigger django.db.models.loading.cache._populate()

    #~ if settings.MODEL_DEBUG:
    if False:
        apps = app_labels()
        logger.debug("%d applications: %s.", len(apps),", ".join(apps))
        logger.debug("%d MODELS:",len(models_list))
        i = 0
        for model in models_list:
            i += 1
            logger.debug("  %2d: %s -> %r",i,full_model_name(model),model)
            #~ logger.debug("      data_elems : %s",' '.join([de.name for de in data_elems(model)]))
        logger.info("Analyzing Models...")
        

    #~ ddhdict = {}
    for model in models.get_models():
        model._lino_ddh = DisableDeleteHandler(model)
        if hasattr(model,'before_save'): 
            raise Exception(
              "%s has a method before_save! see :doc:`/blog/2010/0804`, :doc:`/blog/2011/0226`" % 
              model)
        
        
    for model in models.get_models():
      
        if hasattr(model,'site_setup'):
            model.site_setup(self)
    
        model._lino_detail_layouts = {}
            
        def loader(content,cd,filename):
            dtl = table.DetailLayout(content,filename,cd)
            head,tail = os.path.split(filename)
            model._lino_detail_layouts[tail] = dtl
            if make_messages:
                dtl.make_dummy_messages_file()
            
        load_config_files(loader,'*.dtl','%s/%s' 
            % (model._meta.app_label,model.__name__))
        
        #~ logger.debug("20110822 %s._lino_detail_layouts : %s",
            #~ full_model_name(model),
            #~ ' '.join(["%s=%s" % (k,dl.filename) for k,dl in model._lino_detail_layouts.items()]))
        
        for k,v in class_dict_items(model):
            if isinstance(v,dd.VirtualField):
                v.lino_kernel_setup(model,k)
            
        for f, m in model._meta.get_fields_with_model():
            if isinstance(f,models.CharField) and f.null:
                raise Exception("20110907 Nullable CharField %s in %s" % (f.name,model))
            if isinstance(f,models.ForeignKey):
                f.rel.to._lino_ddh.add_fk(model,f)
                if f.verbose_name == f.name.replace('_', ' '):
                    """
                    If verbose name was not set by user code, 
                    Django sets it to ``field.name.replace('_', ' ')``.
                    We replace this default value by
                    ``f.rel.to._meta.verbose_name``.
                    """
                    f.verbose_name = f.rel.to._meta.verbose_name
                    
    """
    Now another loop to convert `_lino_detail_layouts` to `_lino_detail`
    must be a separate loop because we cannot predict the sorting order of models
    Yield all detail tabs for this model.
    Each detail tab corresponds to a :xfile:`.dtl` file).
    Detail tabs of inherited models come *first*.
    Example: CouseProvider(Company) will yield first all 
    tabs found for Company, then those for CourseProvider.
    """
    
    
    for model in models.get_models():
        collector = {}
        def collect_details(m):
            #~ if model.__name__ == 'CourseProvider':
                #~ logger.debug("20111213 collect_details %s",m.__bases__)  
            #~ if m in self.hide_details: return
            for b in m.__bases__:
                if issubclass(b,models.Model) and b is not models.Model:
                    collect_details(b)
            for k,v in getattr(m,'_lino_detail_layouts',{}).items():
            #~ for k,v in m._lino_detail_layouts.items():
                collector[k] = v
        collect_details(model)
        #~ if model.__name__ == 'CourseProvider':
            #~ logger.debug("20111213 %s collector is %r",model,collector)  
        
        if collector:
            def by0(a,b):
                return cmp(a[0],b[0])
            collector = collector.items()
            collector.sort(by0)
            detail_layouts = [i[1] for i in collector]
            model._lino_detail = table.Detail(model,detail_layouts)
        else:
            model._lino_detail = None
            
    """ 
    And yet another loop to delete _lino_detail_layouts
    """
          
    for model in models.get_models():
      
        del model._lino_detail_layouts
        
        if get_class_attr(model,'summary_row') is None:
            if model._lino_detail:
                def f(obj,ui,rr,**kw):
                    return u'<a href="%s" target="_blank">%s</a>' % (
                      ui.get_detail_url(obj,fmt='detail'),
                      #~ rr.get_request_url(str(obj.pk),fmt='detail'),
                      unicode(obj))
            else:
                def f(obj,ui,rr,**kw):
                    return unicode(obj)
            model.summary_row = f
            #~ print '20101111 installed summary_row for ', model
            
        


class DisableDeleteHandler():
    """
    Used to find out whether a known object can be deleted or not.
    Lino's default behaviour is to forbit deletion if there is any other 
    object in the database that refers to this. To implement this, 
    Lino installs a DisableDeleteHandler instance on each model 
    during :func:`analyze_models`.
    """
    def __init__(self,model):
        self.model = model
        self.fklist = []
        
    def add_fk(self,model,fk):
        self.fklist.append((model,fk))
        
    def __str__(self):
        return ','.join([m.__name__+'.'+fk.name for m,fk in self.fklist])
        
    def disable_delete(self,obj,request):
        #~ print 20101104, "called %s.disable_delete(%s)" % (obj,self)
        h = getattr(self.model,'disable_delete',None)
        if h is not None:
            msg = h(obj,request)
            if msg is not None:
                return msg
        for m,fk in self.fklist:
            kw = {}
            kw[fk.name] = obj
            if not getattr(m,'allow_cascaded_delete',False):
                n = m.objects.filter(**kw).count()
                if n:
                    msg = _("Cannot delete %(self)s because %(count)d %(refs)s refer to it.") % dict(
                      self=obj,count=n,
                      refs=m._meta.verbose_name_plural or m._meta.verbose_name+'s')
                    #~ print msg
                    return msg
        return None
        

def setup_site(self,make_messages=False):
    """
    `self` is the Lino instance stored as :setting:`LINO` in your :xfile:`settings.py`.
    
    This is run once after Django has populated it's model cache, 
    and before any Lino Report can be used.
    Since Django has not "after startup" event, this is triggered 
    "automagically" when it is needed the first time. 
    For example on a mod_wsgi Web Server process it will be triggered 
    by the first request.
    
    """
    logger.info(lino.welcome_text())
    #~ raise Exception("20111229")

    if self._setup_done:
        #~ logger.warning("LinoSite setup already done ?!")
        return
    if self._setting_up:
        #~ logger.warning("LinoSite.setup() called recursively.")
        #~ return 
        raise Exception("LinoSite.setup() called recursively.")
    #~ try:
    self._setting_up = True
    
    #~ self.configure(get_site_config())
    #~ self._siteconfig = get_site_config()
  
    analyze_models(self,make_messages)
    #~ logger.debug("analyze_models() done")
    
    actors.discover()
    #~ logger.debug("actors.discover() done")
    
    table.discover()
    
    choosers.discover()
    
    #~ babel.discover() # would have to be called before model setup

    for a in actors.actors_list:
        a.setup()

    #~ if settings.MODEL_DEBUG:
    if False:
        logger.debug("ACTORS:")
        for k in sorted(actors.actors_dict.keys()):
            a = actors.actors_dict[k]
            #~ logger.debug("%s -> %r",k,a.__class__)
            logger.debug("%s -> %r",k,a.debug_summary())
            
    d = dict()
    for a in loading.get_apps():
        d[a.__name__.split('.')[-2]] = a
    self.modules = IterableUserDict(d)
    
    cls = type("Modules",tuple(),d)
    self.modules = cls()
    #~ logger.info("20120102 modules: %s",self.modules)
              
      
    self._setup_done = True
    self._setting_up = False
    
    dblogger.info("Lino Site %r started. Languages: %s", 
        self.title, ', '.join(babel.AVAILABLE_LANGUAGES))
    dblogger.info(lino.welcome_text())
    #~ except Exception,e:
        #~ logger.exception(e)
        #~ raise

def generate_dummy_messages(self):
    fn = os.path.join(self.source_dir,'dummy_messages.py')
    #~ fn = os.path.join(os.path.dirname(__file__),'dummy_messages.py')
    self.dummy_messages
    raise Exception("use write_message_file() instead!")
    
