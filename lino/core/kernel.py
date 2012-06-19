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
from lino.core import actions
#~ from lino.core import layouts
#~ from lino.utils import perms
#~ from lino.utils import dblogger
#~ from lino.utils import babel
from lino.core import actors
from lino.core.coretools import app_labels # , data_elems # , get_unbound_meth
from lino.utils import get_class_attr, class_dict_items
from lino.utils import ViewPermissionInstance

from lino.tools import resolve_model, resolve_field, get_field, full_model_name
from lino.tools import is_devserver
    
from lino.utils.config import load_config_files, find_config_file
from lino.utils import choosers
from lino.utils import choicelists
from lino.utils import codetime
from lino import dd
#~ from lino.models import get_site_config
from lino.utils import babel
from lino.utils import AttrDict


def analyze_models(self):
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
                    
    if settings.LINO.is_installed('contenttypes'):
      
        from django.db.utils import DatabaseError
        try:
            from lino.models import HelpText
            for ht in HelpText.objects.filter(help_text__isnull=False):
                resolve_field(unicode(ht)).help_text = ht.help_text
        except DatabaseError,e:
            logger.warning("No help texts : %s",e)
            pass
                    

        
def install_summary_rows():
  
    """ 
    Install a :modmeth:`summary_row` method to models that 
    don't have their own.
    """
          
    for model in models.get_models():
        m = get_class_attr(model,'summary_row') 
        if m is None:
            #~ if model._lino_default_table._lino_detail:
            if model._lino_default_table.detail_layout:
                def f(obj,ui,**kw):
                    return ui.ext_renderer.href_to(obj)
                    #~ return u'<a href="%s" target="_blank">%s</a>' % (
                      #~ ui.get_detail_url(obj,fmt='detail'),
                      #~ unicode(obj))
                logger.info('20120217 %s : installed clickable summary_row', model)
            else:
                def f(obj,ui,**kw):
                    return unicode(obj)
                #~ logger.info('20120217 %s : installed plain summary_row', model)
            model.summary_row = f
        else:
            logger.info('20120217 %s : use model summary_row defined in %s', model,m.__module__)
        


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
        
    def disable_delete(self,obj,ar):
        #~ print 20101104, "called %s.disable_delete(%s)" % (obj,self)
        h = getattr(self.model,'disable_delete',None)
        if h is not None:
            msg = h(obj,ar)
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
        



class Always(object):
  
    def allow(obj,user):
        return True
        
class Never(object):
  
    def allow(obj,user):
        return False
        
class RuleHandler(ViewPermissionInstance):
    """
    Lino creates one RuleHandler per model and state
    """
    
    def allow(self,obj,user):
        return self.get_view_permission(user)
        
        
class OwnedOnlyRuleHandler(RuleHandler):
    def allow(self,obj,user):
        if obj.user != user:
            return False
        return RuleHandler.allow(self,obj,user)
        

BLANK_STATE = ''


def load_workflows(self):
    """
    Each Actor receives the meta information about workflows.
    
    If JobProvider is an MTI child of Company, then the 
    Rules for Companies apply also for JobProviders 
    but may be overridden by adding an explicit 
    JobProviders Rule.
    """
    self.workflow_actors = {}
    for actor in actors.actors_list:
        #~ if a.model is not None and a.workflow_actions is not None:
        if actor.workflow_state_field is not None:
            if isinstance(actor.workflow_state_field,basestring):
                fld = actor.get_data_elem(actor.workflow_state_field)
                if fld is None:
                    continue # e.g. cal.Components
                actor.workflow_state_field = fld
                #~ a.workflow_state_field = a.model._meta.get_field(a.workflow_state_field)
            if isinstance(actor.workflow_owner_field,basestring):
                actor.workflow_owner_field = actor.get_data_elem(actor.workflow_owner_field)
                #~ a.workflow_owner_field = a.model._meta.get_field(a.workflow_owner_field)
            #~ for an in a.workflow_actions:
                #~ if not isinstance(an,basestring):
                    #~ raise Exception("Invalid action name %r in %s" % (an,a))
            l = []
            possible_states = actor.workflow_state_field.choicelist.items_dict.keys() + [BLANK_STATE]
            for action in actor._actions_list:
                if action.required_states is not None:
                    rs = []
                    for st in action.required_states:
                        if not st in possible_states:
                            raise Exception("Invalid state %r, must be one of %r" % (st,possible_states))
                        if isinstance(st,choicelists.BabelChoice):
                            st = st.value
                        rs.append(st)
                    l.append(action)
                    action.required_states = frozenset(rs)
                #~ if isinstance(an,basestring):
                    #~ l.append(an)
                #~ else:
                    #~ l.append(an.name)
            #~ a.workflow_actions = [getattr(a,an) for an in l]
            if len(l) == 0:
                continue
                
            actor.workflow_actions = l
            self.workflow_actors[str(actor)] = actor
                
            for a in actor.workflow_actions:
                a._rule_handlers = dict()
                if actor.workflow_owner_field is not None and a.owned_only:
                    rh = OwnedOnlyRuleHandler()
                else:
                    rh = RuleHandler()
                for k in possible_states:
                    a._rule_handlers[k] = rh # Never() # Always()
                
    if self.is_installed('workflows'):
        Rule = resolve_model('workflows.Rule')
        for rule in Rule.objects.all().order_by('seqno'):
            ruleactor = self.workflow_actors.get(rule.actor_name)
            if ruleactor is not None:
                if ruleactor.workflow_owner_field is not None and rule.owned_only:
                    rh = OwnedOnlyRuleHandler()
                else:
                    rh = RuleHandler()
                if rule.user_level:
                    rh.required_user_level = rule.user_level
                if rule.user_group:
                    rh.required_user_groups = [rule.user_group.value]
                    
                def apply_rule(action_names,states,actor):
                    for state in states:
                        for an in action_names:
                            a = getattr(actor,an)
                            a._rule_handlers[state] = rh
                
                if rule.action_name:
                    action_names = [ rule.action_name ]
                else:
                    action_names = [a.name for a in ruleactor.workflow_actions]
                if rule.state:
                    states = []
                else:
                    states = ruleactor.workflow_state_field.choicelist.items_dict.keys()
                    
                for actor in self.workflow_actors.values():
                    if actor is ruleactor or issubclass(actor,ruleactor):
                        apply_rule(action_names,states,actor)

                
    self.workflow_actor_choices = self.workflow_actors.items()
    def cmpfn(a,b):
        return cmp(a[0],b[0])
    self.workflow_actor_choices = self.workflow_actors.items()
    self.workflow_actor_choices.sort(cmpfn)
        
        
        
#~ import threading
#~ write_lock = threading.RLock()

#~ def setup_site(self,make_messages=False):
#~ def setup_site(self,no_site_cache=False):
def setup_site(self):
    """
    `self` is the Lino instance stored as :setting:`LINO` in your :xfile:`settings.py`.
    
    This is run once after Django has populated it's model cache, 
    and before any Lino actor can be used.
    Since Django has not "after startup" event, this is triggered 
    "automagically" when it is needed the first time. 
    For example on a mod_wsgi Web Server process it will be triggered 
    by the first incoming request.
    
    """
    if self._setup_done:
        #~ logger.warning("LinoSite setup already done ?!")
        return
        
    logger.info("Starting Lino...")
    
    """
    Set the site's default language
    """
    babel.set_language(None)
            
    self.mtime = codetime()
    #~ logger.info(lino.welcome_text())
    #~ raise Exception("20111229")
    
    if self.build_js_cache_on_startup is None:
        self.build_js_cache_on_startup = not is_devserver()
      


    #~ write_lock.acquire()
    try:
    
        if self._setting_up:
            #~ logger.warning("LinoSite.setup() called recursively.")
            #~ return 
            raise Exception("LinoSite.setup() called recursively.")
        #~ try:
        self._setting_up = True
        
        #~ self.configure(get_site_config())
        #~ self._siteconfig = get_site_config()
      
        analyze_models(self)
        
        if self.user_model:
            self.user_model = resolve_model(self.user_model)
        
        if self.person_model:
            self.person_model = resolve_model(self.person_model)
        
        if self.project_model:
            self.project_model = resolve_model(self.project_model)
        
        actors.discover()
        
        #~ logger.debug("analyze_models() done")
        
        # set _lino_default_table for all models:
        
        table.discover()
        
        choosers.discover()
        
        #~ load_details(make_messages)
        
        #~ logger.debug("actors.discover() done")
        
        #~ babel.discover() # would have to be called before model setup
        
        #~ self.modules = AttrDict()
        self.modules = actors.MODULES

        for a in models.get_apps():
            #~ for app_label,a in loading.cache.app_store.items():
            app_label = a.__name__.split('.')[-2]
            #~ logger.info("Installing %s = %s" ,app_label,a)
            
            for k,v in a.__dict__.items():
                #~ if isinstance(v,type)  and issubclass(v,dd.Module):
                    #~ logger.info("20120128 Found module %s",v)
                if k.startswith('setup_'):
                    self.modules.define(app_label,k,v)
        for m in models.get_models():
            if not m._meta.abstract:
                self.modules.define(m._meta.app_label,m.__name__,m)
                
        #~ for a in actors.actors_list:
            #~ self.modules.define(a.app_label,a.__name__,a)
            
        #~ layouts.setup_layouts()
        
        #~ for a in actors.actors_list:
            #~ if not hasattr(a,'_lino_detail'):
                #~ a._lino_detail = None
        
        
        #~ actors.setup_actors()
            
            
        #~ import pprint
        #~ logger.info("settings.LINO.modules is %s" ,pprint.pformat(self.modules))
        #~ logger.info("settings.LINO.modules['cal']['main'] is %r" ,self.modules['cal']['main'])
                    
        for a in models.get_apps():
            fn = getattr(a,'site_setup',None)
            if fn is not None:
                fn(self)
                
        """
        Actor.after_site_setup() is called after site_setup() on each actor.
        Example: pcsw.site_setup() adds a detail to properties.Properties, 
        the base class for properties.PropsByGroup. 
        The latter would not 
        install a detail_action during her after_site_setup() 
        and also would never get it later.
        """
        
        for a in actors.actors_list:
            #~ a.setup()
            a.after_site_setup()
                
        """
        `after_site_setup()` definitively collects actions of each actor.
        Now we can apply workflow rules.
        """
        load_workflows(self)
            
        #~ install_summary_rows()
        
        #~ if settings.MODEL_DEBUG:
        if False:
            logger.debug("ACTORS:")
            for k in sorted(actors.actors_dict.keys()):
                a = actors.actors_dict[k]
                #~ logger.debug("%s -> %r",k,a.__class__)
                logger.debug("%s -> %r",k,a.debug_summary())
                
        #~ cls = type("Modules",tuple(),d)
        #~ self.modules = cls()
        #~ logger.info("20120102 modules: %s",self.modules)
        
        
        logger.info("Lino Site %r started. Languages: %s. %s actors.", 
            self.title, ', '.join(babel.AVAILABLE_LANGUAGES),len(actors.actors_list))
        logger.info(lino.welcome_text())
    finally:
        #~ write_lock.release()
        self._setup_done = True
        self._setting_up = False
    
    #~ except Exception,e:
        #~ logger.exception(e)
        #~ raise

def unused_generate_dummy_messages(self):
    fn = os.path.join(self.source_dir,'dummy_messages.py')
    self.dummy_messages
    raise Exception("use write_message_file() instead!")
    
