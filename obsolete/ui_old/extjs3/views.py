# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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

from django import http
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.views.generic import View
#~ from django.utils import simplejson as json
import json
from django.core import exceptions
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode

from lino import dd
#~ from lino.core.signals import pre_ui_delete

from lino.utils.xmlgen import html as xghtml
E = xghtml.E

from lino.utils.jsgen import py2js, js_code, id2js
from lino.utils.config import find_config_file
from lino.utils import ucsv
from lino.utils import choosers
from lino.utils import babel
from lino.utils import isiterable
from lino.utils import dblogger
from lino.utils import auth

from lino.core import actions
from lino.core import actors
from lino.core import dbtables
#~ from lino.core import changes
from lino.core import web

from lino.core.modeltools import obj2str, obj2unicode
from lino.core.modeltools import makedirs_if_missing

from lino.ui import requests as ext_requests
from lino.ui.extjs3 import ext_elems

MAX_ROW_COUNT = 300

E = xghtml.E

pages = dd.resolve_app('pages')

class HttpResponseDeleted(http.HttpResponse):
    status_code = 204
    

def requested_actor(app_label,actor):
    x = getattr(settings.LINO.modules,app_label)
    cl = getattr(x,actor)
    if issubclass(cl,dd.Model):
        return cl._lino_default_table
    return cl
    
#~ class Http403(Exception):
    #~ pass
    
def action_request(app_label,actor,request,rqdata,is_list,**kw):
    rpt = requested_actor(app_label,actor)
    action_name = rqdata.get(ext_requests.URL_PARAM_ACTION_NAME,None)
    if action_name is None:
        if is_list: 
            action_name = rpt.default_list_action_name
        else:
            action_name = rpt.default_elem_action_name
    a = rpt.get_url_action(action_name)
    if a is None:
        raise http.Http404("%s has no url action %r (possible values are %s)" % (
            rpt,action_name,rpt.get_url_action_names()))
    user = request.subst_user or request.user
    if not a.get_view_permission(user.profile):
        #~ raise Http403(_("As %s you have no permission to run this action.") % user.profile)
        raise exceptions.PermissionDenied(
            _("As %s you have no permission to run this action.") % user.profile)
        #~ return http.HttpResponseForbidden(_("As %s you have no permission to run this action.") % user.profile)
    ar = rpt.request(settings.LINO.ui,request,a,**kw)
    #~ ar.renderer = settings.LINO.ui.ext_renderer
    return ar
    
def run_action(ar,elem):
    try:
        rv = ar.bound_action.action.run(elem,ar)
        if rv is None:
            rv  = ui.success()
        return ar.ui.action_response(rv)
        #~ return rv
    #~ except actions.ConfirmationRequired,e:
        #~ r = dict(
          #~ success=True,
          #~ confirm_message='\n'.join([unicode(m) for m in e.messages]),
          #~ step=e.step)
        #~ return ar.ui.action_response(r)
    #~ except actions.DialogRequired,e:
        #~ r = dict(
          #~ success=True,
          #~ dialog_fn=e.dialog,
          #~ step=e.step)
        #~ return ar.ui.action_response(r)
    #~ except actions.DecisionRequired,e:
        #~ r = dict(
          #~ success=True,
          #~ message=unicode(e),
          #~ decide_id=ar.ui.add_decision(e))
        #~ return ar.ui.action_response(r)
    except Warning as e:
        r = dict(
          success=False,
          message=unicode(e),
          alert=True)
        return ar.ui.action_response(r)
    except Exception as e:
        if elem is None:
            msg = unicode(e)
        else:
            msg = _(
              "Action \"%(action)s\" failed for %(record)s:") % dict(
              action=ar.bound_action.full_name(),
              record=obj2unicode(elem))
            msg += "\n" + unicode(e)
        msg += '.\n' + _(
          "An error report has been sent to the system administrator.")
        logger.warning(msg)
        logger.exception(e)
        r = ar.ui.error(e,msg,alert=_("Oops!"))
        return ar.ui.action_response(r)
          
    
  
    
        
def json_response_kw(**kw):
    return json_response(kw)
    
def json_response(x,content_type='application/json'):
    s = py2js(x)
    """
    Theroretically we should send content_type='application/json'
    (http://stackoverflow.com/questions/477816/the-right-json-content-type),
    but "File uploads are not performed using Ajax submission, 
    that is they are not performed using XMLHttpRequests. (...) 
    If the server is using JSON to send the return object, then 
    the Content-Type header must be set to "text/html" in order 
    to tell the browser to insert the text unchanged into the 
    document body." 
    (http://docs.sencha.com/ext-js/3-4/#!/api/Ext.form.BasicForm)
    See 20120209.
    """
    return http.HttpResponse(s, content_type=content_type)
    #~ return HttpResponse(s, content_type='text/html')
    #~ return HttpResponse(s, content_type='application/json')
    #~ return HttpResponse(s, content_type='text/json')
    
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
    rec.update(phantom=True)
    #~ rec.update(id=elem.pk) or -99999)
    return rec

def elem2rec_empty(ar,ah,elem,**rec):
    """
    Returns a dict of this record, designed for usage by an EmptyTable.
    """
    #~ rec.update(data=rh.store.row2dict(ar,elem))
    rec.update(data=elem._data)
    #~ rec = elem2rec1(ar,ah,elem)
    #~ rec.update(title=_("Insert into %s...") % ar.get_title())
    rec.update(title=ar.get_action_title())
    rec.update(id=-99998)
    #~ rec.update(id=elem.pk) or -99999)
    if ar.actor.parameters:
        #~ rec.update(param_values=ar.ah.store.pv2dict(ar.ui,ar.param_values))
        rec.update(param_values=ar.actor.params_layout.params_store.pv2dict(ar.ui,ar.param_values))
    return rec

def elem2rec_detailed(ar,elem,**rec):
    """
    Adds additional information for this record, used only by detail views.
    
    The "navigation information" is a set of pointers to the next, previous, 
    first and last record relative to this record in this report. 
    (This information can be relatively expensive for records that are towards 
    the end of the report. 
    See `/blog/2010/0716`,
    `/blog/2010/0721`,
    `/blog/2010/1116`,
    `/blog/2010/1207`.)
    
    recno 0 means "the requested element exists but is not contained in the requested queryset".
    This can happen after changing the quick filter (search_change) of a detail view.
    
    """
    rh = ar.ah
    rec = elem2rec1(ar,rh,elem,**rec)
    if ar.actor.hide_top_toolbar:
        rec.update(title=unicode(elem))
    else:
        #~ print(ar.get_title())
        #~ print(obj2str(elem))
        #~ print(repr(unicode(elem)))
        rec.update(title=ar.get_title() + u" » " + unicode(elem))
    rec.update(id=elem.pk)
    rec.update(disable_delete=rh.actor.disable_delete(elem,ar))
    if rh.actor.show_detail_navigator:
        rec.update(navinfo=navinfo(ar,elem))
    return rec
            
    

def navinfo(ar,elem):
    first = None
    prev = None
    next = None
    last = None
    recno = 0
    message = None
    LEN = ar.get_total_count()
    if LEN > 0:
        # this algorithm is clearly quicker on queries with a few thousand rows
        id_list = list(ar.data_iterator.values_list('pk',flat=True))
        """
        Uncommented the following assert because it failed in certain circumstances 
        (see `/blog/2011/1220`)
        """
        #~ assert len(id_list) == ar.total_count, \
            #~ "len(id_list) is %d while ar.total_count is %d" % (len(id_list),ar.total_count)
        #~ print 20111220, id_list
        try:
            i = id_list.index(elem.pk)
        except ValueError:
            pass
        else:
            recno = i + 1
            first = id_list[0]
            last = id_list[-1]
            if i > 0:
                prev = id_list[i-1]
            if i < len(id_list) - 1:
                next = id_list[i+1]
            message = _("Row %(rowid)d of %(rowcount)d") % dict(rowid=recno,rowcount=LEN)
    if message is None:
        message = _("No navigation")
    return dict(
        first=first,prev=prev,next=next,last=last,recno=recno,
        message=message)
  
    
    


def delete_element(ar,elem):
    assert elem is not None
    msg = ar.actor.disable_delete(elem,ar)
    if msg is not None:
        rv = ar.ui.error(None,msg,alert=True)
        return ar.ui.action_response(rv)
            
    #~ dblogger.log_deleted(ar.request,elem)
    
    #~ changes.log_delete(ar.request,elem)
    
    dd.pre_ui_delete.send(sender=elem,request=ar.request)
    
    try:
        elem.delete()
    except Exception,e:
        dblogger.exception(e)
        msg = _("Failed to delete %(record)s : %(error)s."
            ) % dict(record=obj2unicode(elem),error=e)
        #~ msg = "Failed to delete %s." % element_name(elem)
        rv = ar.ui.error(None,msg)
        return ar.ui.action_response(rv)
        #~ raise Http404(msg)
        
    
    return HttpResponseDeleted()
    
CATCHED_AJAX_EXCEPTIONS = (Warning,IntegrityError,exceptions.ValidationError)

def ajax_error(e,**kw):
    """
    Utility function that converts a catched exception 
    to a user-friendly error message.
    """
    if isinstance(e,exceptions.ValidationError):
        e = '<br>'.join(e.messages)
    kw = settings.LINO.ui.error(e,alert=True,**kw)
    return json_response(kw)

#~ def form2obj_and_save(self,request,rh,data,elem,is_new,include_rows): # **kw2save):
def form2obj_and_save(ar,data,elem,is_new,restful,file_upload=False): # **kw2save):
    """
    Parses the data from HttpRequest to the model instance and saves it.
    """
    #~ self = settings.LINO.ui
    request = ar.request
    rh = ar.ah
    #~ logger.info('20120814 form2obj_and_save %r', data)
    #~ print 'form2obj_and_save %r' % data
    
    #~ logger.info('20120228 before store.form2obj , elem is %s' % obj2str(elem))
    # store normal form data (POST or PUT)
    #~ original_state = dict(elem.__dict__)
    if not is_new:
        watcher = dd.ChangeWatcher(elem)
    try:
        rh.store.form2obj(ar,data,elem,is_new)
        elem.full_clean()
    except CATCHED_AJAX_EXCEPTIONS as e:
        return ajax_error(e)
        
    kw = dict(success=True)
    
    #~ except exceptions.ValidationError, e:
        #~ kw = settings.LINO.ui.error(e) 
        #~ return json_response(kw)
    
    #~ dirty = False
    #~ missing = object()
    #~ for k, v in original_state.iteritems():
        #~ if v != elem.__dict__.get(k, missing):
            #~ dirty = True
    #~ if not dirty:
    if is_new or watcher.is_dirty():
      
        elem.before_ui_save(ar)
        
        #~ if not is_new:
            #~ dblogger.log_changes(request,elem)
            
            
        kw2save = {}
        if is_new:
            kw2save.update(force_insert=True)
        else:
            kw2save.update(force_update=True)
            
        try:
            elem.save(**kw2save)
        except CATCHED_AJAX_EXCEPTIONS,e:
            return ajax_error(e)
            #~ return views.json_response_kw(success=False,
                  #~ msg=_("There was a problem while saving your data:\n%s") % e)
                  
        if is_new:
            dd.pre_ui_create.send(elem,request=request)
            #~ changes.log_create(request,elem)
            kw.update(
                message=_("%s has been created.") % obj2unicode(elem))
                #~ record_id=elem.pk)
        else:
            watcher.send_update(request)
            #~ watcher.log_diff(request)
            kw.update(message=_("%s has been updated.") % obj2unicode(elem))
        
    else:
    
        kw.update(message=_("%s : nothing to save.") % obj2unicode(elem))
        
    kw = elem.after_ui_save(ar,**kw)
        
    if restful:
        # restful mode (used only for Ext.ensible) needs list_fields, not detail_fields
        kw.update(rows=[rh.store.row2dict(ar,elem,rh.store.list_fields)])
    elif file_upload:
        kw.update(record_id=elem.pk)
        return json_response(kw,content_type='text/html')
    else: # 20120814 
        #~ logger.info("20120816 %r", ar.action)
        #~ if isinstance(ar.bound_action.action,actions.GridEdit):
        #~ if ar.bound_action.action.action_name in ('put','post'): # grid.on_afteredit
            #~ kw.update(rows=[rh.store.row2list(ar,elem)])
        #~ else:
            #~ kw.update(data_record=elem2rec_detailed(ar,elem))
        """
        TODO: in fact we need *either* `rows` (when this was called from a Grid) 
        *or* `data_record` (when this was called from a form). 
        But how to find out which one is needed?
        """
        kw.update(rows=[rh.store.row2list(ar,elem)])
        kw.update(data_record=elem2rec_detailed(ar,elem))
    #~ logger.info("20120208 form2obj_and_save --> %r",kw)
    return json_response(kw)
            





        

class AdminIndex(View):
    """
    Similar to PlainIndex
    """
    def get(self, request, *args, **kw):
        ui = settings.LINO.ui
        if settings.LINO.user_model is not None:
            user = request.subst_user or request.user
            a = settings.LINO.get_main_action(user)
            if a is not None and a.get_view_permission(user.profile):
                kw.update(on_ready=ui.ext_renderer.action_call(request,a,{}))
        return http.HttpResponse(ui.html_page(request,**kw))

class MainHtml(View):
    def get(self, request, *args, **kw):
        ui = settings.LINO.ui
        rv = ui.success(html=settings.LINO.get_main_html(request))
        return ui.action_response(rv)
        
class Authenticate(View):
  
    def get(self, request, *args, **kw):
        action_name = request.GET.get(ext_requests.URL_PARAM_ACTION_NAME)
        if action_name == 'logout':
            username = request.session['username'] 
            del request.session['username'] 
            del request.session['password']
            rv = dict(success=True,message="%r has been logged out" % username)
            return settings.LINO.ui.action_response(rv)
            

    def post(self, request, *args, **kw):
        from lino.utils import auth
        #~ from django.contrib.sessions.backends.db import SessionStore
        #~ ss = SessionStore()
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username,password)
        if user is None:
            rv = settings.LINO.ui.error("Could not authenticate %r" % username)
            return settings.LINO.ui.action_response(rv)
        request.session['username'] = username
        request.session['password'] = password
        #~ request.session['password'] = request.GET.get('password')
        #~ auth.login(request,request.GET.get('username'), request.GET.get('password'))
        #~ ss.save()
        rv = settings.LINO.ui.success("Now logged in as %r" % username)
        #~ rv = dict(success=True,message="Now logged in as %r" % username)
        return settings.LINO.ui.action_response(rv)
      

class RunJasmine(View):
    """
    """
    def get(self, request, *args, **kw):
        ui = settings.LINO.ui
        return http.HttpResponse(ui.html_page(request,run_jasmine=True))

class EidAppletService(View):
    """
    """
    def post(self, request, *args, **kw):
        ui = settings.LINO.ui
        return ui.success(html='Hallo?')


class Callbacks(View):
    def get(self,request,thread_id,button_id):
        return settings.LINO.ui.callback_get(request,thread_id,button_id)
        

class Templates(View):
  
    #~ def templates_view(self,request,
    def get(self,request,
        app_label=None,actor=None,pk=None,fldname=None,tplname=None,**kw):
      
        if request.method == 'GET':
            from lino.models import TextFieldTemplate
            if tplname:
                tft = TextFieldTemplate.objects.get(pk=int(tplname))
                return http.HttpResponse(tft.text)
                
            rpt = requested_actor(app_label,actor)
                
            elem = rpt.get_row_by_pk(pk)

                
            if elem is None:
                raise http.Http404("%s %s does not exist." % (rpt,pk))
                
            #~ TextFieldTemplate.templates
            m = getattr(elem,"%s_templates" % fldname,None)
            if m is None:
                q = models.Q(user=request.user) | models.Q(user=None)
                #~ q = models.Q(user=request.user)
                qs = TextFieldTemplate.objects.filter(q).order_by('name')
            else:
                qs = m(request)
                
            templates = []
            for obj in qs:
                url = settings.LINO.build_admin_url('templates',
                    app_label,actor,pk,fldname,unicode(obj.pk))
                templates.append([
                    unicode(obj.name),url,unicode(obj.description)])
            js = "var tinyMCETemplateList = %s;" % py2js(templates)
            return http.HttpResponse(js,content_type='text/json')
        raise http.Http404("Method %r not supported" % request.method)



def choices_for_field(request,rpt,field):
    #~ logger.info("20120202 %r",field)
    chooser = choosers.get_for_field(field)
    if chooser:
        #~ logger.info('20120710 choices_view() : has chooser')
        qs = chooser.get_request_choices(request,rpt)
        #~ qs = list(chooser.get_request_choices(ar,rpt))
        #~ logger.info("20120213 %s",qs)
        #~ if qs is None:
            #~ qs = []
        assert isiterable(qs), \
              "%s.%s_choices() returned %r which is not iterable." % (
              rpt.model,field.name,qs)
        if chooser.simple_values:
            def row2dict(obj,d):
                d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                #~ 20130117 : 'int' object has no attribute 'get_choices_text'
                d[ext_requests.CHOICES_VALUE_FIELD] = obj
                return d
        elif chooser.instance_values:
            # same code as for ForeignKey
            def row2dict(obj,d):
                d[ext_requests.CHOICES_TEXT_FIELD] = obj.get_choices_text(request,rpt,field)
                d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk
                return d
        else:
            def row2dict(obj,d):
                d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                #~ d[ext_requests.CHOICES_TEXT_FIELD] = obj[1].get_choices_text(request,rpt,field)
                d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
                return d
    elif field.choices:
        qs = field.choices
        def row2dict(obj,d):
            if type(obj) is list or type(obj) is tuple:
                d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
            else:
                d[ext_requests.CHOICES_TEXT_FIELD] = obj.get_choices_text(request,rpt,field)
                d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
            return d
        
    elif isinstance(field,models.ForeignKey):
        m = field.rel.to
        t = getattr(m,'_lino_choices_table',m._lino_default_table)
        qs = t.request(settings.LINO.ui,request).data_iterator
        #~ logger.info('20120710 choices_view(FK) %s --> %s',t,qs)
        def row2dict(obj,d):
            d[ext_requests.CHOICES_TEXT_FIELD] = obj.get_choices_text(request,rpt,field)
            d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk 
            return d
    else:
        raise http.Http404("No choices for %s" % fldname)
    return (qs,row2dict)
        

def choices_response(request,qs,row2dict,emptyValue):
    quick_search = request.GET.get(ext_requests.URL_PARAM_FILTER,None)
    if quick_search is not None:
        qs = dbtables.add_quick_search_filter(qs,quick_search)
        
    count = len(qs)
        
    offset = request.GET.get(ext_requests.URL_PARAM_START,None)
    if offset:
        qs = qs[int(offset):]
        #~ kw.update(offset=int(offset))
    limit = request.GET.get(ext_requests.URL_PARAM_LIMIT,None)
    if limit:
        #~ kw.update(limit=int(limit))
        qs = qs[:int(limit)]
        
    rows = [ row2dict(row,{}) for row in qs ]
    if emptyValue is not None: # 20121203
        empty = dict()
        empty[ext_requests.CHOICES_TEXT_FIELD] = emptyValue
        empty[ext_requests.CHOICES_VALUE_FIELD] = None
        rows.insert(0,empty)
    return json_response_kw(count=count,rows=rows) 
    #~ return json_response_kw(count=len(rows),rows=rows) 
    #~ return json_response_kw(count=len(rows),rows=rows,title=_('Choices for %s') % fldname)




  
class ActionParamChoices(View):
  
    def get(self,request,app_label=None,actor=None,an=None,field=None,**kw):
        actor = requested_actor(app_label,actor)
        ba = actor.get_url_action(an)
        if ba is None:
            raise Exception("Unknown action %r for %s" % (an,actor))
        field = ba.action.get_param_elem(field)
        qs, row2dict = choices_for_field(request,actor,field)
        if field.blank:
            emptyValue = '<br/>'
        else:
            emptyValue = None
        return choices_response(request,qs,row2dict,emptyValue)
      
class Choices(View):
  
    #~ def choices_view(self,request,app_label=None,rptname=None,fldname=None,**kw):
    def get(self,request,app_label=None,rptname=None,fldname=None,**kw):
        """
        Return a JSON object with two attributes `count` and `rows`,
        where `rows` is a list of `(display_text,value)` tuples.
        Used by ComboBoxes or similar widgets.
        If `fldname` is not specified, returns the choices for 
        the `record_selector` widget.
        """
        rpt = requested_actor(app_label,rptname)
        emptyValue = None
        if fldname is None:
            ar = rpt.request(settings.LINO.ui,request) # ,rpt.default_action)
            #~ rh = rpt.get_handle(self)
            #~ ar = ViewReportRequest(request,rh,rpt.default_action)
            #~ ar = dbtables.TableRequest(self,rpt,request,rpt.default_action)
            #~ rh = ar.ah
            #~ qs = ar.get_data_iterator()
            qs = ar.data_iterator
            #~ qs = rpt.request(self).get_queryset()
            def row2dict(obj,d):
                d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                return d
        else:
            """
            NOTE: if you define a *parameter* with the same name 
            as some existing *data element* name, then the parameter 
            will override the data element. At least here in choices view.
            """
            #~ field = find_field(rpt.model,fldname)
            field = rpt.get_param_elem(fldname)
            if field is None:
                field = rpt.get_data_elem(fldname)
            if field.blank:
                #~ logger.info("views.Choices: %r is blank",field)
                emptyValue = '<br/>'
            qs, row2dict = choices_for_field(request,rpt,field)
            
        return choices_response(request,qs,row2dict,emptyValue)
        
  
class Restful(View):
    """
    Used to collaborate with a restful Ext.data.Store.
    """
  
    def post(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_actor(app_label,actor)
        #~ a = rpt.default_action
        if pk is None:
            elem = None
        else:
            elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(ui,request)
            
        instance = ar.create_instance()
        # store uploaded files. 
        # html forms cannot send files with PUT or GET, only with POST
        if ar.actor.handle_uploaded_files is not None:
            ar.actor.handle_uploaded_files(instance,request)
            
        data = request.POST.get('rows')
        #~ logger.info("20111217 Got POST %r",data)
        data = json.loads(data)
        #~ data = self.rest2form(request,rh,data)
        return form2obj_and_save(ar,data,instance,True,True)
            
        
      
    def delete(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_actor(app_label,actor)
        #~ a = rpt.default_action
        elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(ui,request)
        return delete_element(ar,elem)
      
    def get(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_actor(app_label,actor)
        #~ a = rpt.default_action
        assert pk is None, 20120814
        #~ if pk is None:
            #~ elem = None
        #~ else:
            #~ elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(ui,request)
        rh = ar.ah
        rows = [ 
          rh.store.row2dict(ar,row,rh.store.list_fields) 
            for row in ar.sliced_data_iterator ]
        return json_response_kw(count=ar.get_total_count(),rows=rows)
        
    def put(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_actor(app_label,actor)
        #~ a = rpt.default_action
        elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(ui,request)
        rh = ar.ah
            
        data = http.QueryDict(request.body).get('rows') # raw_post_data before Django 1.4
        data = json.loads(data)
        a = rpt.get_url_action(rpt.default_list_action_name)
        ar = rpt.request(ui,request,a)
        ar.renderer = ui.ext_renderer
        return form2obj_and_save(ar,data,elem,False,True) # force_update=True)
          
  
  
class ApiElement(View):
    #~ def api_element_view(self,request,app_label=None,actor=None,pk=None):
    def get(self,request,app_label=None,actor=None,pk=None):
        """
        GET : Retrieve a representation of the addressed member of the collection expressed in an appropriate MIME type.
        PUT : Update the addressed member of the collection or create it with the specified ID. 
        POST : Treats the addressed member as a collection and creates a new subordinate of it. 
        DELETE : Delete the addressed member of the collection. 
        
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        ui = settings.LINO.ui
        rpt = requested_actor(app_label,actor)
        #~ if not ah.actor.can_view.passes(request.user):
            #~ msg = "User %s cannot view %s." % (request.user,ah.actor)
            #~ return http.HttpResponseForbidden()
        
        if pk and pk != '-99999' and pk != '-99998':
            elem = rpt.get_row_by_pk(pk)
            if elem is None:
                raise http.Http404("%s has no row with primary key %r" % (rpt,pk))
                #~ raise Exception("20120327 %s.get_row_by_pk(%r)" % (rpt,pk))
        else:
            elem = None
        
        action_name = request.GET.get(ext_requests.URL_PARAM_ACTION_NAME,
          rpt.default_elem_action_name)
        ba = rpt.get_url_action(action_name)
        if ba is None:
            raise http.Http404("%s has no action %r" % (rpt,action_name))
            
        #~ ar = rpt.request(ui,request,a)
        ar = ba.request(ui,request)
        ar.renderer = ui.ext_renderer
        ah = ar.ah
        
        fmt = request.GET.get(ext_requests.URL_PARAM_FORMAT,ba.action.default_format)

        #~ if isinstance(a,actions.OpenWindowAction):
        if ba.action.opens_a_window:
          
            if fmt == ext_requests.URL_FORMAT_JSON:
                if pk == '-99999':
                    assert elem is None
                    elem = ar.create_instance()
                    datarec = elem2rec_insert(ar,ah,elem)
                elif pk == '-99998':
                    assert elem is None
                    elem = ar.create_instance()
                    datarec = elem2rec_empty(ar,ah,elem)
                else:
                    datarec = elem2rec_detailed(ar,elem)
                
                return json_response(datarec)
                
            after_show = ar.get_status(ui,record_id=pk)
            
            tab = request.GET.get(ext_requests.URL_PARAM_TAB,None)
            if tab is not None: 
                tab = int(tab)
                after_show.update(active_tab=tab)
            
            return http.HttpResponse(ui.html_page(request,ba.action.label,
              on_ready=ui.ext_renderer.action_call(request,ba,after_show)))
            
        if isinstance(ba.action,actions.RedirectAction):
            target = ba.action.get_target_url(elem)
            if target is None:
                raise http.Http404("%s failed for %r" % (ba,elem))
            return http.HttpResponseRedirect(target)
            
        if isinstance(ba.action,actions.RowAction):
            if pk == '-99998':
                assert elem is None
                elem = ar.create_instance()
            return run_action(ar,elem)
        raise NotImplementedError("Action %s is not implemented)" % ba)
                
        
    def post(self,request,app_label=None,actor=None,pk=None):
        ar = action_request(app_label,actor,request,request.POST,True)
        ar.renderer = settings.LINO.ui.ext_renderer
        elem = ar.actor.get_row_by_pk(pk)
        if elem is None:
            raise http.Http404("%s has no row with primary key %r" % (ar.actor,pk))
        if isinstance(ar.bound_action.action,actions.RowAction):
            if pk == '-99998':
                assert elem is None
                elem = ar.create_instance()
            return run_action(ar,elem)
        raise NotImplementedError("Action %s is not implemented)" % ar)
        
    def put(self,request,app_label=None,actor=None,pk=None):
        data = http.QueryDict(request.body) # raw_post_data before Django 1.4
        ar = action_request(app_label,actor,request,data,False)
        ar.renderer = settings.LINO.ui.ext_renderer
        elem = ar.actor.get_row_by_pk(pk)
        if elem is None:
            raise http.Http404("%s has no row with primary key %r" % (rpt,pk))
        return form2obj_and_save(ar,data,elem,False,False) # force_update=True)
            
    def delete(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_actor(app_label,actor)
        elem = rpt.get_row_by_pk(pk)
        if elem is None:
            raise http.Http404("%s has no row with primary key %r" % (rpt,pk))
        ar = rpt.request(ui,request)
        return delete_element(ar,elem)
        

        
  
class ApiList(View):
    """
    - GET : List the members of the collection. 
    - PUT : Replace the entire collection with another collection. 
    - POST : Create a new entry in the collection where the ID is assigned automatically by the collection. 
      The ID created is included as part of the data returned by this operation. 
    - DELETE : Delete the entire collection.
    
    (Source: http://en.wikipedia.org/wiki/Restful)
    """

    def post(self,request,app_label=None,actor=None):
        #~ ui = settings.LINO.ui
        #~ rpt = requested_actor(app_label,actor)
        
        #~ action_name = request.POST.get(
            #~ ext_requests.URL_PARAM_ACTION_NAME,
            #~ rpt.default_list_action_name)
        #~ a = rpt.get_url_action(action_name)
        #~ if a is None:
            #~ raise http.Http404("%s has no url action %r" % (rpt,action_name))
        #~ ar = rpt.request(ui,request,a)
        
        ar = action_request(app_label,actor,request,request.POST,True)
        ar.renderer = settings.LINO.ui.ext_renderer
        #~ print 20121116, ar.bound_action.action.action_name
        if ar.bound_action.action.action_name in ['duplicate_row','post','poststay','insert']:
        #~ if isinstance(ar.bound_action.action,(
              #~ actions.InsertRow,
              #~ actions.DuplicateAction,
              #~ actions.SubmitInsert)):
            rh = ar.ah
            elem = ar.create_instance()
            if rh.actor.handle_uploaded_files is not None:
                rh.actor.handle_uploaded_files(elem,request)
                file_upload = True
            else:
                file_upload = False
            return form2obj_and_save(ar,request.POST,elem,True,False,file_upload)
        return run_action(ar,None)
        #~ rv = ar.bound_action.action.run(ar)
        #~ return rv
      
    def get(self,request,app_label=None,actor=None):
        #~ ar = action_request(app_label,actor,request,request.GET,limit=PLAIN_PAGE_LENGTH)
        ar = action_request(app_label,actor,request,request.GET,True)
        ar.renderer = settings.LINO.ui.ext_renderer
        rh = ar.ah
        
        #~ print 20120630, 'api_list_view'
        fmt = request.GET.get(
            ext_requests.URL_PARAM_FORMAT,
            ar.bound_action.action.default_format)
            
        #~ logger.info("20121203 views.ApiList.get() %s",ar.bound_action.full_name())
      
        if fmt == ext_requests.URL_FORMAT_JSON:
            #~ ar.renderer = ui.ext_renderer
            rows = [ rh.store.row2list(ar,row) for row in ar.sliced_data_iterator]
            #~ return json_response_kw(msg="20120124")
            #~ total_count = len(ar.data_iterator)
            total_count = ar.get_total_count()
            #~ if ar.create_rows:
            for row in ar.create_phantom_rows():
                d = rh.store.row2list(ar,row)
                rows.append(d)
                total_count += 1
            #~ 20120918
            kw = dict(count=total_count,
              rows=rows,
              success=True,
              no_data_text=ar.no_data_text, 
              #~ status=ar.get_status(ar.ui),
              title=unicode(ar.get_title()))
              #~ disabled_actions=rpt.disabled_actions(ar,None),
              #~ gc_choices=[gc.data for gc in ar.actor.grid_configs])
            if ar.actor.parameters:
                #~ kw.update(param_values=ar.ah.store.pv2dict(ar.ui,ar.param_values))
                kw.update(param_values=ar.actor.params_layout.params_store.pv2dict(ar.ui,ar.param_values))
            return json_response(kw) 
                
        if fmt == ext_requests.URL_FORMAT_HTML:
            #~ ar.renderer = ui.ext_renderer
            after_show = ar.get_status(ar.ui)
            if isinstance(ar.bound_action.action,actions.InsertRow):
                elem = ar.create_instance()
                #~ print 20120630
                #~ print elem.national_id
                rec = elem2rec_insert(ar,rh,elem)
                after_show.update(data_record=rec)

            kw = dict(on_ready=
                ar.renderer.action_call(ar.request,ar.bound_action,after_show))
                #~ ui.ext_renderer.action_call(ar.request,ar.action,after_show))
            #~ print '20110714 on_ready', params
            kw.update(title=ar.get_title())
            return http.HttpResponse(ar.ui.html_page(request,**kw))
        
        if fmt == 'csv':
            #~ response = HttpResponse(mimetype='text/csv')
            charset = settings.LINO.csv_params.get('encoding','utf-8')
            response = http.HttpResponse(
              content_type='text/csv;charset="%s"' % charset)
            if False:
                response['Content-Disposition'] = \
                    'attachment; filename="%s.csv"' % ar.actor
            else:
                #~ response = HttpResponse(content_type='application/csv')
                response['Content-Disposition'] = \
                    'inline; filename="%s.csv"' % ar.actor
              
            #~ response['Content-Disposition'] = 'attachment; filename=%s.csv' % ar.get_base_filename()
            w = ucsv.UnicodeWriter(response,**settings.LINO.csv_params)
            w.writerow(ar.ah.store.column_names())
            for row in ar.data_iterator:
                w.writerow([unicode(v) for v in rh.store.row2list(ar,row)])
            return response
            
        if fmt in (ext_requests.URL_FORMAT_PDF,ext_requests.URL_FORMAT_ODT):
            if ar.get_total_count() > MAX_ROW_COUNT:
                raise Exception(_("List contains more than %d rows") % MAX_ROW_COUNT)
        
            from lino.utils.appy_pod import Renderer
            
            tpl_leaf = "Table.odt" 
            tplgroup = None
            tplfile = find_config_file(tpl_leaf,tplgroup)
            if not tplfile:
                raise Exception("No file %s / %s" % (tplgroup,tpl_leaf))
                
            ip = ar.request.META.get('REMOTE_ADDR','unknown_ip')
            target_parts = ['cache', 'appypdf', ip, str(ar.actor) + '.' + fmt]
            target_file = os.path.join(settings.MEDIA_ROOT,*target_parts)
            makedirs_if_missing(os.path.dirname(target_file))
            target_url = settings.LINO.build_media_url(*target_parts)
            ar.renderer = ar.ui.ext_renderer # 20120624
            """
            [NOTE] `/blog/2012/0211`
            
            """
            context = dict(
                ar=ar,
                title=unicode(ar.get_title()),
                dtos=babel.dtos,
                dtosl=babel.dtosl,
                dtomy=babel.dtomy,
                babelattr=babel.babelattr,
                babelitem=babel.babelitem,
                tr=babel.babelitem,
                settings=settings,
                _ = _,
                #~ knowledge_text=fields.knowledge_text,
                )
            if os.path.exists(target_file):
                os.remove(target_file)
            logger.info(u"appy.pod render %s -> %s (params=%s",
                tplfile,target_file,settings.LINO.appy_params)
            renderer = Renderer(tplfile, context, target_file,**settings.LINO.appy_params)
            renderer.run()
            return http.HttpResponseRedirect(target_url)
            
        if fmt == ext_requests.URL_FORMAT_PRINTER:
            if ar.get_total_count() > MAX_ROW_COUNT:
                raise Exception(_("List contains more than %d rows") % MAX_ROW_COUNT)
            #~ ar.renderer = ui.ext_renderer
            response = http.HttpResponse(content_type='text/html;charset="utf-8"')
            doc = xghtml.Document(force_unicode(ar.get_title()))
            doc.body.append(xghtml.E.h1(doc.title))
            t = doc.add_table()
            ar.ui.ar2html(ar,t,ar.data_iterator)
            doc.write(response,encoding='utf-8')
            return response
            
        raise http.Http404("Format %r not supported for GET on %s" % (fmt,ar.actor))

      
class GridConfig(View):

    #~ def grid_config_view(self,request,app_label=None,actor=None):
    def put(self,request,app_label=None,actor=None):
        ui = settings.LINO.ui
        rpt = requested_actor(app_label,actor)
        #~ rpt = actors.get_actor2(app_label,actor)
        PUT = http.QueryDict(request.body) # raw_post_data before Django 1.4
        gc = dict(
          widths = [int(x) for x in PUT.getlist(ext_requests.URL_PARAM_WIDTHS)],
          columns = [str(x) for x in PUT.getlist(ext_requests.URL_PARAM_COLUMNS)],
          hiddens=[(x == 'true') for x in PUT.getlist(ext_requests.URL_PARAM_HIDDENS)],
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
            msg = _("Error while saving GC for %(table)s: %(error)s") % dict(
                table=rpt,error=e)
            return settings.LINO.ui.error(None,msg,alert=True)
        #~ logger.info(msg)
        settings.LINO.ui.build_site_cache(True)            
        return settings.LINO.ui.success(msg)
        
MENUS = dict()        


def plain_response(ui,request,tplname,context):        
    u = request.subst_user or request.user
    menu = MENUS.get(u.profile,None)
    if menu is None:
        menu = settings.LINO.get_site_menu(ui,u.profile)
        url = settings.LINO.plain_prefix + '/'
        menu.add_url_button(url,label=_("Home"))
        menu = menu.as_html(ui,request)
        menu = E.tostring(menu)
        MENUS[u.profile] = menu
    context.update(menu=menu,E=E)
    web.extend_context(context)
    template = settings.LINO.jinja_env.get_template(tplname)
    
    response = http.HttpResponse(
        template.render(**context),
        content_type='text/html;charset="utf-8"')
    
    return response
            

  
class PlainList(View):
  
    def get(self,request,app_label=None,actor=None):
        ar = action_request(app_label,actor,request,request.GET,True)
        ar.renderer = ar.ui.plain_renderer
        context = dict(
          title=ar.get_title(),
          heading=ar.get_title(),
          #~ tbar = buttons,
          main=ar.as_html(),
        )
        return plain_response(ar.ui,request,'table.html',context)
        
        

class PlainElement(View):
  
    def get(self,request,app_label=None,actor=None,pk=None):
        """
        GET : Retrieve a representation of the addressed member of the collection expressed in an appropriate MIME type.
        PUT : Update the addressed member of the collection or create it with the specified ID. 
        POST : Treats the addressed member as a collection and creates a new subordinate of it. 
        DELETE : Delete the addressed member of the collection. 
        
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        ui = settings.LINO.ui
        ar = action_request(app_label,actor,request,request.GET,False)
        ar.renderer = ui.plain_renderer
        
        context = dict(
          title=ar.get_action_title(),
          #~ menu = E.tostring(menu),
          #~ tbar = buttons,
          main = ar.as_html(pk),
        )
        #~ template = web.jinja_env.get_template('detail.html')
        
        return plain_response(ui,request,'detail.html',context)
        
        
class PlainIndex(View):
    """
    This is not a docstring
    Similar to AdminIndex
    """
    def get(self, request, *args, **kw):
        ui = settings.LINO.ui
        context = dict(
          title = settings.LINO.title,
          main = '',
        )
        if settings.LINO.user_model is not None:
            user = request.subst_user or request.user
        else:
            user = auth.AnonymousUser.instance()
        a = settings.LINO.get_main_action(user)
        if a is not None:
            if not a.get_view_permission(user.profile):
                raise PermissionDenied("Action not allowed for %s" % user)
            ar = a.request(settings.LINO.ui,request,**kw)
            ar.renderer = ui.plain_renderer
            context.update(title=ar.get_title())
            # TODO: let ar generate main
            # context.update(main=ui.plain_renderer.action_call(request,a,{}))
        return plain_response(ui,request,'plain_index.html',context)
