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

import traceback
#~ from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.conf import settings
from django import http
from django.db import models


import lino
from lino.utils import AttrDict
from lino.utils import curry
from lino.utils import babel
from lino.utils import Warning

from lino.ui import requests as ext_requests

from lino.core.modeltools import resolve_model

#~ from lino.core.perms import UserLevels
#~ from lino.core import perms 


class VirtualRow(object):
    def __init__(self,**kw):
        self.update(**kw)
        
    def update(self,**kw):
        for k,v in kw.items():
            setattr(self,k,v)

    def get_row_permission(self,user,state,action):
        if action.readonly:
            return True
        return False 
            

class PhantomRow(VirtualRow):
    def __init__(self,request,**kw):
        self._ar = request
        VirtualRow.__init__(self,**kw)
        
    def __unicode__(self):
        return unicode(self._ar.get_action_title())
        
class EmptyTableRow(VirtualRow):
    """
    Base class for virtual rows of an :class:`EmptyTable`.
    """
    def __init__(self,table,**kw):
        self._table = table
        VirtualRow.__init__(self,**kw)
        
    def __unicode__(self):
        return unicode(self._table.label)
        
    def get_print_language(self,pm):
        return babel.DEFAULT_LANGUAGE
        
    def get_templates_group(self):
        return self._table.app_label + '/' + self._table.__name__
    
    def filename_root(self):
        return self._table.app_label + '.' + self._table.__name__









class Hotkey:
    keycode = None
    shift = False
    ctrl = False
    alt = False
    inheritable = ('keycode','shift','ctrl','alt')
    def __init__(self,**kw):
        for k,v in kw.items():
            setattr(self,k,v)
            
    def __call__(self,**kw):
        for n in self.inheritable:
            if not kw.has_key(n):
                kw[n] = getattr(self,n)
            return Hotkey(**kw)
      
# ExtJS src/core/EventManager-more.js
RETURN = Hotkey(keycode=13)
ESCAPE = Hotkey(keycode=27)
PAGE_UP  = Hotkey(keycode=33)
PAGE_DOWN = Hotkey(keycode=34)
INSERT = Hotkey(keycode=44)
DELETE = Hotkey(keycode=46)
    
    
class ConfirmationRequired(Exception):
    """
    This is the special exception risen when an Action calls 
    :meth:`ActionRequest.confirm`.
    """
    def __init__(self,step,messages):
        self.step = step
        self.messages = messages
        Exception.__init__(self)
        
class DialogRequired(Exception):
    """
    This is the special exception risen when an Action calls 
    :meth:`ActionRequest.dialog`.
    """
    def __init__(self,step,dlg):
        self.step = step
        self.dialog = dlg
        Exception.__init__(self)
        
class Parametrizable(object):        
  
    parameters = None
    """
    User-definable parameter fields for this table.
    Set this to a `dict` of `name = models.XyzField()` pairs.
    """
    
    #~ params_template = None # no longer used
    
    params_layout = None
    """
    If this table has parameters, specify here how they should be 
    laid out in the parameters panel.
    """
    
    @classmethod
    def register_params(cls):
        if cls.parameters:
            for k,v in cls.parameters.items():
                v.set_attributes_from_name(k)
                v.table = cls
                
    @classmethod
    def after_site_setup(self,site):
        if self.parameters:
            from lino.utils.choosers import check_for_chooser
            for k,v in self.parameters.items():
                if isinstance(v,models.ForeignKey):
                    v.rel.to = resolve_model(v.rel.to)
                check_for_chooser(self,v)
        
    @classmethod
    def get_param_elem(self,name):
        if self.parameters:
            return self.parameters.get(name,None)
        #~ for pf in self.params:
            #~ if pf.name == name:  return pf
        return None
      
        


class Action(Parametrizable):
    """
    Abstract base class for all Actions
    """
    
    sort_index = 90
    """
    
    Predefined sort_index values are:
    
    ===== =================================
    value action
    ===== =================================
    20    :class:`Insert <InsertRow>`
    30    :class:`Delete <DeleteSelected>`
    50    :class:`Print <lino.mixins.printable.BasePrintAction>`
    60    :attr:`Duplicate <lino.mixins.duplicable.Duplicable.duplicate_row>`
    90    default for all custom row actions created using :func:`@dd.action <action>`
    ===== =================================
    
    """
    
    label = None
    """
    The text to appear on the button.
    """
    
    help_text = None
    """
    A help text that shortly explains what this action does.
    ExtJS uses this as tooltip text.
    """
    
    auto_save = True
    """
    What to do when this action is being called while the user is on a dirty record.
    
    - `False` means: forget any changes in current record and run the action.
    - `True` means: save any changes in current record before running the action.
    - `None` means: ask the user.
    """
    
    required = {}
    """
    A dict with permission requirements.
    See :func:`lino.core.perms.make_permission_handler`.
    """
    
    name = None
    """
    Internally used to store the name of this action within the Actor's namespace.
    """
    
    url_action_name = None
    """
    """
    
    use_param_panel = False
    """
    Used internally. This is True for window actions whose window 
    use the parameter panel: grid and emptytable (but not showdetail)
    """
    
    
    actor = None
    """
    Internally used to store the :class:`lino.core.actors.Actor` 
    who owns this action.
    """
    
    key = None
    """
    The hotkey. Currently not used.
    """
    
    callable_from = None
    """
    Either `None`(default) or a tuple of class 
    objects (subclasses of :class:`Action`).
    If specified, this action is available only within a window 
    that has been opened by one of the given actions.
    """
    
    default_format = 'html'
    """
    Used internally.
    """
    
    readonly = True
    """
    Whether this action possibly modifies data *in the given object*.
    
    This means that :class:`InsertRow` is a `readonly` action.
    Actions like :class:`InsertRow` and :class:`Duplicable <lino.mixins.duplicable.Duplicate>` 
    which do not modify the given object but *do* modify the database,
    must override their `get_action_permission`::
    
      def get_action_permission(self,user,obj,state):
          if user.profile.readonly: 
              return False
          return super(Duplicate,self).get_action_permission(user,obj,state)
        
    
    """
    
    opens_a_window = False
    """
    Used internally to say whether this action opens a window.
    """
    
    hide_top_toolbar = False
    """
    Used internally if :attr:`opens_a_window` to say whether 
    the window has a top toolbar.
    """
    
    hide_navigator = False
    """
    Used internally if :attr:`opens_a_window` to say whether the window has a navigator.
    """
    
    show_in_bbar = True
    """
    Used internally.
    Whether this action should be displayed as a button in the bottom toolbar and the context menu.
    """
    
    show_in_workflow = False
    """
    Used internally.
    Whether this action should be displayed 
    as the :meth:`workflow_buttons <lino.core.actors.Actor.workflow_buttons>`.
    """
    
    custom_handler = False
    """
    Whether this action is implemented as Javascript function call.
    (...)
    """
    
    
    #~ def __init__(self,label=None,url_action_name=None,required={},**kw):
    def __init__(self,label=None,**kw):
        """
        The first argument is the optional `label`,
        other arguments should be specified as keywords and can be 
        any of the existing class attributes.
        """
        #~ if url_action_name is not None:
            #~ if not isinstance(url_action_name,basestring):
                #~ raise Exception("%s name %r is not a string" % (self.__class__,url_action_name))
            #~ self.url_action_name = url_action_name
        if label is not None:
            self.label = label
            
        #~ if label is None:
            #~ label = self.label or self.url_action_name 
        for k,v in kw.items():
            if not hasattr(self,k):
                raise Exception("Invalid keyword %s" % k)
            setattr(self,k,v)
        self.set_required()
        #~ self.set_required(**required)
        assert self.callable_from is None or isinstance(
            self.callable_from,(tuple,type)), "%s" % self
            
        self.register_params()

        
    def set_required(self,**kw):
        """
        Override existing permission requirements.
        Arguments: see :func:`lino.core.perms.make_permission_handler`.
        """
        #~ logger.info("20120628 set_required %s(%s)",self,kw)
        new = dict()
        new.update(self.required)
        new.update(kw)
        self.required = new
        #~ if isinstance(self,StateAction):
        if self.required.has_key('states'):
            self.show_in_workflow = True
            self.custom_handler = True
            self.show_in_bbar = False
        else:
            self.show_in_workflow = False
            self.show_in_bbar = True
        
    def __str__(self):
        #~ raise Exception("Must use action2str(actor,action)")
        if self.actor is None:
            #~ raise Exception("tried to call str() on general action %s" % self.name)
            return repr(self)
            #~ raise Exception("Tried to call str() on shared action %r" % self)
        if self.name is None:
            return repr(self)
        return str(self.actor) + '.' + self.name
        
    #~ def set_permissions(self,*args,**kw)
        #~ self.permission = perms.factory(*args,**kw)
        
    def attach_to_actor(self,actor,name):
        if self.name is not None:
            raise Exception("%s tried to attach named action %s" % (actor,self))
        if self.actor is not None:
            raise Exception("%s tried to attach action %s of %s" % (actor,name,self.actor))
        self.name = name
        self.actor = actor
        if self.label is None:
            self.label = name
        if actor.hide_top_toolbar:
            self.hide_top_toolbar = True
        if self.help_text is None and self is actor.default_action:
            self.help_text  = actor.help_text
        #~ if name == 'default_action':
            #~ print 20120527, self
            
    #~ def contribute_to_class(self,model,name):
        #~ ma = model.__dict__.get('_lino_model_actions',None)
        #~ if ma is None:
            #~ ma = dict()
            #~ model._lino_model_actions = ma
            #~ # model.__dict__.set('_lino_model_actions',ma)
        #~ ma[name] = self
        #~ self.name = name
        #~ # model.__dict__['_lino_model_actions'] = d
        
    def __unicode__(self):
        return force_unicode(self.label)
        
    #~ def get_view_permission(self,user):
        #~ """
        #~ E.g. DispatchAction is not available for a User with empty partner
        #~ """
        #~ return True
        
    def get_button_label(self):
        if self.actor is None:
            return self.label 
        if self is self.actor.default_action:
            return self.label 
        else:
            return u"%s %s" % (self.label,self.actor.label)
            
    def get_action_permission(self,user,obj,state):
        """
        The default implementation simply calls this action's 
        permission handler.
        Derived Action classes may override this to add vetos.
        E.g. DispatchAction is not available for a User with empty partner.
        """
        return self.allow(user,obj,state)
        
    #~ def run(self,elem,ar,**kw):
        #~ raise NotImplementedError("%s has no run() method" % self.__class__)

    def request(self,*args,**kw):
        kw.update(action=self)
        return self.actor.request(*args,**kw)
        

class TableAction(Action):
    """
    TODO: get_action_permission and required_states 
    are needed here because `disabled_actions` also asks InsertRow whether 
    it's permitted on that row. It's in fact not correct to ask this for 
    the Insert button. Has to do with the fact that the Insert button is 
    in the bottom toolbar though it should be in the top toolbar...
    """
  
    #~ required_states = None
    
    def get_action_title(self,rr):
        return rr.get_title()
        

class RowAction(Action):
    """
    Base class for actions that are executed on an individual row.
    """
    
    def run(self,row,ar,**kw):
        """
        Execute the action on the given `row`. `ar` is an :class:`ActionRequest` 
        object representing the context where the action is running.
        """
        raise NotImplementedError("%s has no run() method" % self.__class__)

    #~ def get_action_permission(self,user,obj):
        #~ return self.actor.get_row_permission(self,user,obj)
            
    def attach_to_actor(self,actor,name):
        super(RowAction,self).attach_to_actor(actor,name)
        if not self.url_action_name:
            self.url_action_name = name 



class RedirectAction(Action):
    
    def get_target_url(self,elem):
        raise NotImplementedError
        



class GridEdit(TableAction):
  
    use_param_panel = True
    show_in_workflow = False
    opens_a_window = True

    callable_from = tuple()
    url_action_name = 'grid'
    
    def attach_to_actor(self,actor,name):
        #~ self.label = actor.button_label or actor.label
        self.label = actor.label
        super(GridEdit,self).attach_to_actor(actor,name)

    def get_window_layout(self):
        #~ return self.actor.list_layout
        return None


class ShowDetailAction(RowAction):
    """
    An action that opens the Detail Window of its actor.
    """
    opens_a_window = True
    show_in_workflow = False
    
    #~ sort_index = 1
    callable_from = (GridEdit,)
    #~ show_in_detail = False
    #~ needs_selection = True
    url_action_name = 'detail'
    label = _("Detail")
    
    def get_window_layout(self):
        return self.actor.detail_layout
        
    #~ def get_elem_title(self,elem):
        #~ return _("%s (Detail)")  % unicode(elem)
        

RowAction.callable_from = (GridEdit,ShowDetailAction)

class InsertRow(TableAction):
    """
    Opens the Insert window filled with a blank row. 
    The new row will be actually created only when this 
    window gets submitted.
    """
    label = _("New")
    show_in_workflow = False
    opens_a_window = True
    hide_navigator = True
    sort_index = 20
    hide_top_toolbar = True
    #~ readonly = False # see blog/2012/0726
    required = dict(user_level='user')
    callable_from = (GridEdit,ShowDetailAction)
    url_action_name = 'insert'
    #~ label = _("Insert")
    key = INSERT # (ctrl=True)
    #~ needs_selection = False
    
    def get_action_title(self,rr):
        return _("Insert into %s") % force_unicode(rr.get_title())
        
    def get_window_layout(self):
        return self.actor.insert_layout or self.actor.detail_layout

    def get_action_permission(self,user,obj,state):
        # see blog/2012/0726
        if user.profile.readonly: 
            return False
        return super(InsertRow,self).get_action_permission(user,obj,state)




class DuplicateRow(RowAction):
    opens_a_window = True
  
    readonly = False
    required = dict(user_level='user')
    callable_from = (GridEdit,ShowDetailAction)
    url_action_name = 'duplicate'
    label = _("Duplicate")


class ShowEmptyTable(ShowDetailAction):
    use_param_panel = True
    callable_from = tuple()
    url_action_name = 'show' 
    default_format = 'html'
    #~ hide_top_toolbar = True
    hide_navigator = True
    
    def attach_to_actor(self,actor,name):
        self.label = actor.label
        ShowDetailAction.attach_to_actor(self,actor,name)
        #~ print 20120523, actor, name, 'setup', unicode(self.label)
        
    def get_action_title(self,rr):
        return rr.get_title()
    #~ def __str__(self):
        #~ return str(self.actor)+'.'+self.name
        
    

class UpdateRowAction(RowAction):
    show_in_workflow = False
    readonly = False
    required = dict(user_level='user')
    

class ListAction(Action):
    """
    Base class for actions that are executed server-side on an individual row.
    """
    callable_from = (GridEdit,)
    

class DeleteSelected(RowAction):
    """
    Delete the row.
    """
    auto_save = False
    sort_index = 30
    readonly = False
    show_in_workflow = False
    required = dict(user_level='user')
    callable_from = (GridEdit,ShowDetailAction)
    #~ needs_selection = True
    label = _("Delete")
    url_action_name = 'delete'
    key = DELETE # (ctrl=True)
    #~ client_side = True
    
        
class SubmitDetail(RowAction):
    label = _("Save")
    auto_save = False
    show_in_workflow = False
    #~ show_in_bbar = True
    readonly = False
    required = dict(user_level='user')
    #~ url_action_name = 'SubmitDetail'
    callable_from = (ShowDetailAction,)
    
class SubmitInsert(SubmitDetail):
    #~ url_action_name = 'SubmitInsert'
    label = _("Create")
    #~ label = _("Insert")
    callable_from = (InsertRow,)




class ActionRequest(object):
    """
    Holds information about an indivitual web request and provides methods like

    - :meth:`get_user <lino.core.actions.ActionRequest.get_user>`
    - :meth:`confirm <lino.core.actions.ActionRequest.confirm>`
    - :meth:`success_response <lino.ui.base.UI.success_response>`
    - :meth:`error_response <lino.ui.base.UI.error_response>`
    - :meth:`spawn <lino.core.actions.ActionRequest.spawn>`

    
    """
    create_kw = None
    renderer = None
    
    offset = None
    limit = None
    order_by = None
    
    def __init__(self,ui,actor,request=None,action=None,renderer=None,param_values=None,**kw):
        """
        An ActionRequest is instantiated from different shortcut methods:
        
        - :meth:`lino.core.actors.Actor.request`
        - :meth:`lino.core.actions.Action.request`
        
        """
        #~ ActionRequest.__init__(self,ui,action)
        if ui is None:
            ui = settings.LINO.ui
            #~ from lino.ui.extjs3 import ui
        self.ui = ui
        self.error_response = ui.error_response
        self.success_response = ui.success_response
        if renderer is None:
            renderer = ui.text_renderer
        self.renderer = renderer
        self.action = action or actor.default_action
        self.step = 0 # confirmation counter
        #~ self.report = actor
        self.actor = actor
        self.request = request
        if request is not None:
            if request.method == 'PUT':
                rqdata = http.QueryDict(request.raw_post_data)
            else:
                rqdata = request.REQUEST
            kw = self.parse_req(request,rqdata,**kw)
        #~ 20120605 self.ah = actor.get_handle(ui)
        self.setup(**kw)
        self.ah = actor.get_request_handle(self)
        """
        See 20120825
        """
        if self.actor.parameters is None:
            if param_values is not None:
                raise Exception("Cannot request param_values on %s" % self.actor)
        else:
            pv = self.actor.param_defaults(self)
            
            """
            New since 20120913.
            E.g. newcomers.Newcomers is a simple pcsw.Clients with known_values=dict(client_state=newcomer)
            and since there is a parameter `client_state`, we override that parameter's default value.
            """
            for k,v in self.known_values.items():
                if pv.has_key(k):
                    pv[k] = v
            """
            New since 20120914.
            MyClientsByGroup has a known group, this 
            must also appear as `group` parameter value.
            Lino now understands tables where the master_key is also a parameter.
            """
            if self.actor.master_key is not None:
                if pv.has_key(self.actor.master_key):
                    pv[self.actor.master_key] = self.master_instance
                
            if request is not None:
                pv.update(self.ui.parse_params(self.ah,request))
                
            if param_values is not None:
                for k in param_values.keys(): 
                    if not pv.has_key(k):
                        raise Exception("Invalid key %r in param_values" % k)
                pv.update(param_values)
                
            self.param_values = AttrDict(**pv)
            
            #~ if param_values:
                #~ # logger.info("20120608 param_values is %s",param_values)
                #~ for k,v in param_values.items():
                    #~ self.param_values.define(k,v)
                
        
    def parse_req(self,request,rqdata,**kw): 
        #~ if self.actor.parameters:
            #~ kw.update(param_values=self.ui.parse_params(self.ah,request))
        kw.update(user=request.user)
        kw.update(subst_user=request.subst_user)
        kw.update(requesting_panel=request.requesting_panel)
        #~ if settings.LINO.user_model:
            #~ username = rqdata.get(ext_requests.URL_PARAM_SUBST_USER,None)
            #~ if username:
                #~ try:
                    #~ kw.update(subst_user=settings.LINO.user_model.objects.get(username=username))
                #~ except settings.LINO.user_model.DoesNotExist, e:
                    #~ pass
        #~ logger.info("20120723 ActionRequest.parse_req() --> %s",kw)
        return kw
      
    def setup(self,
            user=None,
            subst_user=None,
            #~ param_values={},
            known_values=None,
            requesting_panel=None,
            renderer=None,
            **kw):
        self.requesting_panel = requesting_panel
        self.user = user
        if renderer is not None:
            self.renderer = renderer
        #~ if self.actor.parameters:
            #~ self.param_values = AttrDict(**param_values)
        self.subst_user = subst_user
        #~ 20120111 
        #~ self.known_values = known_values or self.report.known_values
        #~ if self.report.known_values:
        #~ d = dict(self.report.known_values)
        for k,v in self.actor.known_values.items():
            kw.setdefault(k,v)
        if known_values:
            kw.update(known_values)
        self.known_values = kw
        
        
    def dialog(self,dlg):
        self.step += 1
        if int(self.request.REQUEST.get(ext_requests.URL_PARAM_ACTION_STEP,'0')) >= self.step:
            return
        raise DialogRequired(self.step,dlg)
        
    def confirm(self,*messages):
        """
        Calling this from an Action's :meth:`Action.run` method will
        interrupt the execution, send the specified message(s) back to 
        the user, waiting for confirmation before continuing.
        
        Note that this is implemented without any server sessions 
        and cookies. While this system is genial, it has one drawback 
        which you should be aware of: the code execution does not 
        *continue* after the call to `confirm` but starts again at the 
        beginning (with the difference that the client this time calls it with 
        an internal `step` parameter that tells Lino that this `confirm()` 
        has been answered and should no longer raise stop execution.
        """
        assert len(messages) > 0 and messages[0], "At least one non-empty message required"
        self.step += 1
        if int(self.request.REQUEST.get(ext_requests.URL_PARAM_ACTION_STEP,'0')) >= self.step:
            return
        raise ConfirmationRequired(self.step,messages)
        
    def create_phantom_rows(self,**kw):
        if self.create_kw is None or not self.actor.editable or not self.actor.allow_create:
            #~ logger.info('20120519 %s.create_phantom_row(), %r', self,self.create_kw)
            return 
        #~ if not self.actor.get_permission(self.get_user(),self.actor.create_action):
        #~ if not self.actor.allow_create(self.get_user(),None,None):
        if self.actor.create_action is not None:
            if not self.actor.create_action.allow(self.get_user(),None,None):
                return
        yield PhantomRow(self,**kw)
      
    def create_instance(self,**kw):
        if self.create_kw:
            kw.update(self.create_kw)
        #logger.debug('%s.create_instance(%r)',self,kw)
        if self.known_values:
            kw.update(self.known_values)
        #~ print "20120527 create_instance", self, kw
        obj = self.actor.create_instance(self,**kw)
        #~ print 20120630, self.actor, 'actions.TableRequest.create_instance'
        #~ if self.known_values is not None:
            #~ self.ah.store.form2obj(self.known_values,obj,True)
            #~ for k,v in self.known_values:
                #~ field = self.model._meta.get_field(k) ...hier
                #~ kw[k] = v
        return obj
        
    def get_data_iterator(self):
        raise NotImplementedError
        
    def get_base_filename(self):
        return str(self.actor)
        #~ s = self.get_title()
        #~ return s.encode('us-ascii','replace')
        
    def get_user(self):
        """
        Return the :class:`User <lino.modlib.users.models.User>` 
        instance of the user who issued the request.
        If the authenticated user is acting as somebody else, 
        return that :class:`User <lino.modlib.users.models.User>` instance.
        """
        return self.subst_user or self.user
        
    def get_action_title(self):
        return self.action.get_action_title(self)
        
    def get_title(self):
        return self.actor.get_title(self)
        
    def render_to_dict(self):
        return self.action.render_to_dict(self)
        
    def get_request_url(self,*args,**kw):
        return self.ui.get_request_url(self,*args,**kw)

    def get_status(self,ui,**kw):
        if self.actor.parameters:
            kw.update(param_values=self.ah.store.pv2dict(ui,self.param_values))
        bp = kw.setdefault('base_params',{})
        if self.subst_user is not None:
            #~ bp[ext_requests.URL_PARAM_SUBST_USER] = self.subst_user.username
            bp[ext_requests.URL_PARAM_SUBST_USER] = self.subst_user.id
        #~ if self.actor.__name__ == 'MyClients':
            #~ print "20120918 actions.get_status", kw
        return kw
        

    def spawn(self,actor=None,**kw):
        """
        Create a new ActionRequest, taking default values from this one.
        """
        kw.setdefault('user',self.user)
        kw.setdefault('subst_user',self.subst_user)
        kw.setdefault('requesting_panel',self.requesting_panel)
        kw.setdefault('renderer',self.renderer)
        #~ kw.setdefault('request',self.request) 
        # removed 20120702 because i don't want to inherit quick_search from spawning request
        # and because i couldn't remember why 'request' was passed to the spawned request.
        if actor is None:
            actor = self.actor
        return self.ui.request(actor,**kw)
        
    def href_to(self,*args,**kw): return self.renderer.href_to(self,*args,**kw)
    def pk2url(self,*args,**kw): return self.renderer.pk2url(self,*args,**kw)
    def get_request_url(self,*args,**kw): return self.renderer.get_request_url(self,*args,**kw)
        
    def absolute_uri(self,*args,**kw):
        ar = self.spawn(*args,**kw)
        location = ar.renderer.get_request_url(ar)
        return self.request.build_absolute_uri(location)
        

def action(*args,**kw):
    """
    Decorator to define custom actions.
    Same signature as :meth:`Action.__init__`.
    In practice you'll possibly use:
    :attr:`label <Action.label>`,
    :attr:`help_text <Action.help_text>` and
    :attr:`required <Action.required>`
    """
    def decorator(fn):
        kw.setdefault('custom_handler',True)
        a = RowAction(*args,**kw)
        #~ a.run = curry(fn,a)
        a.run = fn
        return a
    return decorator
    
#~ def action2str(actor,action):
    #~ return str(actor) + '.' + action.name
