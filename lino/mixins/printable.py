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

"""
See :doc:`/admin/printable`

"""
import logging
logger = logging.getLogger(__name__)

import os
import sys
import logging
import traceback
import cStringIO
import glob
from fnmatch import fnmatch

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string, get_template, select_template, Context, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.encoding import force_unicode

try:
    import ho.pisa as pisa
    #pisa.showLogging()
except ImportError:
    pisa = None

try:
    import appy
except ImportError:
    appy = None
    
try:
    import pyratemp
except ImportError:
    pyratemp = None
        
import lino
from lino import reports
from lino import fields
#~ from lino import actions

from lino.utils import iif
from lino.utils import babel 
from lino.utils.choosers import chooser
from lino.utils.appy_pod import setup_renderer


bm_dict = {}
bm_list = []


class BuildMethod:
    """
    Base class for all build methods.
    A build method encapsulates the process of generating a 
    "printable document" that inserts data from the database 
    into a template, using a given combination of a template 
    parser and post-processor.
    """
    name = None
    label = None
    target_ext = None
    template_ext = None
    #~ button_label = None
    label = None
    templates_name = None
    cache_name = 'cache'
    webdav = False
    
    def __init__(self):
        if self.label is None:
            self.label = _(self.__class__.__name__)
        #~ self.templates_dir = os.path.join(settings.PROJECT_DIR,'templates',self.name)
        #~ if self.templates_name is None:
            #~ self.templates_name = self.name
        #~ self.templates_dir = os.path.join(settings.PROJECT_DIR,'doctemplates',self.templates_name or self.name)
        if self.templates_name is None:
            self.templates_name = self.name
        self.templates_dir = os.path.join(settings.LINO.webdav_root,'doctemplates',self.templates_name)
        #~ self.templates_dir = os.path.join(settings.MEDIA_ROOT,'webdav','doctemplates',self.templates_name)
        self.templates_url = settings.LINO.webdav_url + '/'.join(('doctemplates',self.templates_name))
        #~ self.templates_url = settings.MEDIA_URL + '/'.join(('webdav','doctemplates',self.templates_name))
        

            
    def __unicode__(self):
        return unicode(self.label)
        
    def get_target_parts(self,action,elem):
        "used by `get_target_name`"
        return [self.cache_name, self.name, action.filename_root(elem) + '-' + str(elem.pk) + self.target_ext]
        
    def get_target_name(self,action,elem):
        "return the output filename to generate on the server"
        if self.webdav:
            return os.path.join(settings.LINO.webdav_root,*self.get_target_parts(action,elem))
        return os.path.join(settings.MEDIA_ROOT,*self.get_target_parts(action,elem))
        
    def get_target_url(self,action,elem):
        "return the url that points to the generated filename on the server"
        if self.webdav:
            return settings.LINO.webdav_url + "/".join(self.get_target_parts(action,elem))
        return settings.MEDIA_URL + "/".join(self.get_target_parts(action,elem))
            
    def build(self,action,elem):
        raise NotImplementedError
        
    def get_template_url(self,action,elem):
        raise NotImplementedError
        
class DjangoBuildMethod(BuildMethod):

    def get_template(self,action,elem):
        tpls = action.get_print_templates(self,elem)
        if len(tpls) == 0:
            raise Exception("No templates defined for %r" % elem)
        #~ logger.debug('make_pisa_html %s',tpls)
        try:
            return select_template(tpls)
        except TemplateDoesNotExist,e:
            raise Exception("No template found for %s (%s)" % (e,tpls))

    def render_template(self,elem,tpl): # ,MEDIA_URL=settings.MEDIA_URL):
        context = dict(
          instance=elem,
          title = unicode(elem),
          MEDIA_URL = settings.MEDIA_ROOT.replace('\\','/') + '/',
        )
        return tpl.render(Context(context))
        
class PisaBuildMethod(DjangoBuildMethod):
    """
    Generates .pdf files from .html templates.
    """
    name = 'pisa'
    target_ext = '.pdf'
    #~ button_label = _("PDF")
    template_ext = '.pisa.html'  
    
    def build(self,action,elem):
        tpl = self.get_template(elem) 
        filename = action.before_build(self,elem)
        if filename is None:
            return
        html = self.render_template(elem,tpl) # ,MEDIA_URL=url)
        html = html.encode("utf-8")
        file(filename+'.html','w').write(html)
        
        result = cStringIO.StringIO()
        h = logging.FileHandler(filename+'.log','w')
        pisa.log.addHandler(h)
        pdf = pisa.pisaDocument(cStringIO.StringIO(html), result,encoding='utf-8')
        pisa.log.removeHandler(h)
        h.close()
        file(filename,'wb').write(result.getvalue())
        if pdf.err:
            raise Exception("pisa.pisaDocument.err is %r" % pdf.err)
        

class SimpleBuildMethod(BuildMethod):
  
    def get_template_leaf(self,action,elem):
        tpls = action.get_print_templates(self,elem)
        #~ if not tpls:
            #~ return
        if len(tpls) != 1:
            raise Exception(
              "%s.get_print_templates() must return exactly 1 template (got %r)" % (
                elem.__class__.__name__,tpls))
        tpl_leaf = tpls[0]
        lang = elem.get_print_language(self)
        if lang != babel.DEFAULT_LANGUAGE:
            tplfile = os.path.normpath(os.path.join(self.templates_dir,tpl_leaf))
            if not os.path.exists(tplfile):
                lang = babel.DEFAULT_LANGUAGE
                #~ tpl = os.path.normpath(os.path.join(self.templates_dir,default_language(),tpl_leaf))
        return lang + '/' + tpl_leaf
        
    def get_template_url(self,action,elem):
        tpl = self.get_template_leaf(action,elem)
        return self.templates_url + '/' + tpl
        
    def build(self,action,elem):
        target = action.before_build(self,elem)
        if not target:
            return
        tpl_leaf = self.get_template_leaf(action,elem)
        tplfile = os.path.normpath(os.path.join(self.templates_dir,tpl_leaf))
        self.simple_build(elem,tplfile,target)
        
    def simple_build(self,elem,tpl,target):
        raise NotImplementedError
        
class AppyBuildMethod(SimpleBuildMethod):
    """
    Base class for Build Methods that use `.odt` templates designed
    for :term:`appy.pod`.
    
    http://appyframework.org/podRenderingTemplates.html
    """
    
    template_ext = '.odt'  
    templates_name = 'appy' # subclasses use the same templates directory
    
    def simple_build(self,elem,tpl,target):
        from lino.models import get_site_config
        from appy.pod.renderer import Renderer
        renderer = None
        context = dict(self=elem,
            dtos=babel.dtos,
            dtosl=babel.dtosl,
            dtomy=babel.dtomy,
            babelattr=babel.babelattr,
            babelitem=babel.babelitem,
            tr=babel.babelitem,
            iif=iif,
            settings=settings,
            #~ restify=restify,
            site_config = get_site_config(),
            _ = _,
            #~ knowledge_text=fields.knowledge_text,
            )
        lang = str(elem.get_print_language(self))
        logger.info(u"appy.pod render %s -> %s (language=%r,params=%s",
            tpl,target,lang,settings.LINO.appy_params)
        savelang = babel.get_language()
        babel.set_language(lang)
        #~ locale.setlocale(locale.LC_ALL,ls)
        #~ Error: unsupported locale setting
        renderer = Renderer(tpl, context, target,**settings.LINO.appy_params)
        setup_renderer(renderer)
        #~ renderer.context.update(restify=debug_restify)
        renderer.run()
        babel.set_language(savelang)
        

class AppyOdtBuildMethod(AppyBuildMethod):
    """
    Generates .odt files from .odt templates.
    
    This method doesn't require OpenOffice nor the 
    Python UNO bridge installed
    (except in some cases like updating fields).
    """
    name = 'appyodt'
    target_ext = '.odt'
    cache_name = 'userdocs'
    #~ cache_name = 'webdav'
    webdav = True

class AppyPdfBuildMethod(AppyBuildMethod):
    """
    Generates .pdf files from .odt templates.
    """
    name = 'appypdf'
    target_ext = '.pdf'

class AppyRtfBuildMethod(AppyBuildMethod):
    """
    Generates .rtf files from .odt templates.
    """
    name = 'appyrtf'
    target_ext = '.rtf'
    cache_name = 'userdocs'
    #~ cache_name = 'webdav'
    webdav = True

class AppyDocBuildMethod(AppyBuildMethod):
    """
    Generates .doc files from .odt templates.
    """
    name = 'appydoc'
    target_ext = '.doc'
    cache_name = 'userdocs'
    #~ cache_name = 'webdav'
    webdav = True

        
class LatexBuildMethod(BuildMethod):
    """
    Generates .pdf files from .tex templates.
    """
    name = 'latex'
    target_ext = '.pdf'
    template_ext = '.tex'  
    
    def simple_build(self,elem,tpl,target):
        context = dict(instance=elem)
        raise NotImplementedError
            
class RtfBuildMethod(SimpleBuildMethod):
    """
    Generates .rtf files from .rtf templates.
    """
  
    name = 'rtf'
    #~ button_label = _("RTF")
    target_ext = '.rtf'
    template_ext = '.rtf'  
    cache_name = 'userdocs'
    #~ cache_name = 'webdav'
    
    def simple_build(self,elem,tpl,target):
        context = dict(instance=elem)
        t = pyratemp.Template(filename=tpl)
        try:
            result = t(**context)
        except pyratemp.TemplateRenderError,e:
            raise Exception(u"%s in %s" % (e,tpl))
        file(target,'wb').write(result)
        


def register_build_method(pm):
    bm_dict[pm.name] = pm
    bm_list.append(pm)
    

register_build_method(AppyOdtBuildMethod())
register_build_method(AppyPdfBuildMethod())
register_build_method(AppyRtfBuildMethod())   
register_build_method(LatexBuildMethod())
register_build_method(PisaBuildMethod())
register_build_method(RtfBuildMethod())

#~ print "%d build methods:" % len(bm_list)
#~ for bm in bm_list:
    #~ print bm


def build_method_choices():
    return [ (pm.name,pm.label) for pm in bm_list]

    
    
def get_template_choices(group,bmname):
    """
    :param:bmname: the name of a build method.
    """
    pm = bm_dict.get(bmname,None)
    #~ pm = get_build_method(build_method)
    if pm is None:
        raise Exception("%r : invalid print method name." % bmname)
    #~ glob_spec = os.path.join(pm.templates_dir,'*'+pm.template_ext)
    top = os.path.join(pm.templates_dir,babel.DEFAULT_LANGUAGE,group)
    l = []
    for dirpath, dirs, files in os.walk(top):
        for fn in files:
            if fnmatch(fn,'*'+pm.template_ext):
                if len(dirpath) > len(top):
                    fn = os.path.join(dirpath[len(top)+1:],fn)
                l.append(fn.decode(sys.getfilesystemencoding()))
    if not l:
        logger.warning("get_template_choices() : no matches for (%r,%r) in %s",group,bmname,top)
    return l
            
    
def get_build_method(elem):
    bmname = elem.get_build_method()
    if not bmname:
        raise Exception("%s has no build method" % elem)
    bm = bm_dict.get(bmname,None)
    if bm is None:
        raise Exception("Build method %r doesn't exist. Requested by %r." % (bmname,elem))
    return bm
        

#~ class PrintAction(actions.RedirectAction):
class BasePrintAction(reports.RowAction):
  
    def before_build(self,bm,elem):
        """Return the target filename if a document needs to be built,
        otherwise return ``None``.
        """
        filename = bm.get_target_name(self,elem)
        if not filename:
            return
        if os.path.exists(filename):
            #~ if not elem.must_rebuild_target(filename,self):
                #~ logger.debug("%s : %s -> %s is up to date",self,elem,filename)
                #~ return
            logger.info(u"%s %s -> overwrite existing %s.",bm,elem,filename)
            os.remove(filename)
        else:
            dirname = os.path.dirname(filename)
            if not os.path.isdir(dirname):
                if True:
                    raise Exception("Please create yourself directory %s" % dirname)
                else:
                    os.makedirs(dirname)
        logger.debug(u"%s : %s -> %s", bm,elem,filename)
        return filename
        
        
class PrintAction(BasePrintAction):
    """Note that this action should rather be called 
    'Open a printable document' than 'Print'.
    For the user they are synonyms as long as Lino doesn't support server-side printing.
    """
    name = 'print'
    label = _('Print')
    callable_from = None
    #~ needs_selection = True
    
    def before_build(self,bm,elem):
        if not elem.must_build:
            return
        return BasePrintAction.before_build(self,bm,elem)
            
    def get_print_templates(self,bm,elem):
        return elem.get_print_templates(bm,self)
        
    def filename_root(self,elem):
        return elem._meta.app_label + '.' + elem.__class__.__name__
        
    def run_(self,elem,**kw):
        bm = get_build_method(elem)
        if elem.must_build:
            bm.build(self,elem)
            elem.must_build = False
            elem.save()
            kw.update(refresh=True)
            kw.update(message="%s printable has been built." % elem)
        else:
            kw.update(message="Reused %s printable from cache." % elem)
        kw.update(open_url=bm.get_target_url(self,elem))
        return kw
        #~ return rr.ui.success_response(open_url=target,**kw)
        
    def run(self,rr,elem,**kw):
        kw = self.run_(elem,**kw)
        return rr.ui.success_response(**kw)
      
class DirectPrintAction(BasePrintAction):
    #~ def __init__(self,rpt,name,label,bmname,tplname):
    def __init__(self,name,label,tplname,build_method=None):
        BasePrintAction.__init__(self,name,label)
        #~ self.bm =  bm_dict.get(build_method or settings.LINO.preferred_build_method)
        self.build_method = build_method
        self.tplname = tplname
        
    def get_print_templates(self,bm,elem):
        #~ assert bm is self.bm
        return [ self.tplname ]
        
    def filename_root(self,elem):
        return elem._meta.app_label + '.' + elem.__class__.__name__
        #~ return self.actor.model._meta.app_label + '.' + self.actor.model.__name__
        
    def run(self,rr,elem,**kw):
        bm =  bm_dict.get(self.build_method or settings.LINO.config.default_build_method)
        if not self.tplname.endswith(bm.template_ext):
            raise Exception("Invalid template for build method %r" % bm.name)
        bm.build(self,elem)
        #~ target = settings.MEDIA_URL + "/".join(bm.get_target_parts(self,elem))
        #~ return rr.ui.success_response(open_url=target,**kw)
        kw.update(open_url=bm.get_target_url(self,elem))
        return rr.ui.success_response(**kw)
    
class EditTemplateAction(reports.RowAction):
    name = 'tpledit'
    label = _('Edit template')
    
    def run(self,rr,elem,**kw):
        bm = get_build_method(elem)
        target = bm.get_template_url(self,elem)
        return rr.ui.success_response(open_url=target,**kw)
    
class ClearCacheAction(reports.RowAction):
#~ class ClearCacheAction(actions.UpdateRowAction):
    name = 'clear'
    label = _('Clear cache')
    
    def run(self,rr,elem):
        elem.must_build = True
        elem.save()
        return rr.ui.success_response("%s printable cache has been cleared." % elem,refresh=True)

class PrintableType(models.Model):
    """
    Base class for models that specify the :attr:`TypedPrintable.type`.
    """
    
    templates_group = None
    """
    Default value for `templates_group` is the model's `app_label`.
    """
    
    class Meta:
        abstract = True
        
    build_method = models.CharField(max_length=20,
      verbose_name=_("Build method"),
      choices=build_method_choices(),blank=True)
    """
    The name of the build method to be used.
    The list of choices for this field is static, but depends on 
    which additional packages are installed.
    """
    
    template = models.CharField(max_length=200,
      verbose_name=_("Template"),
      blank=True)
    """
    The name of the file to be used as template.
    The list of choices for this field depend on the :attr:`build_method`.
    Ending must correspond to the :attr:`build_method`.
    """
    
    #~ build_method = models.CharField(max_length=20,choices=mixins.build_method_choices())
    #~ template = models.CharField(max_length=200)
    
    @classmethod
    def get_templates_group(cls):
        return cls.templates_group or cls._meta.app_label
        
    @chooser(simple_values=True)
    def template_choices(cls,build_method):
        if not build_method:
            build_method = settings.LINO.config.default_build_method 
        #~ print cls, 'template_choices for method' ,build_method
        #~ bm = bm_dict[build_method]
        return get_template_choices(cls.get_templates_group(),build_method)
        #~ return get_template_choices(TEMPLATE_GROUP,build_method)
    #~ template_choices.simple_values = True
    #~ template_choices = classmethod(template_choices)
    
class Printable(models.Model):
    """
    Mixin for Models whose instances can "print" (generate a printable document).
    """
    
    must_build = models.BooleanField(_("must build"),default=True,editable=False)
    """
    For internal use. Users don't need to see this.
    """
    
    class Meta:
        abstract = True
        
    @classmethod
    def setup_report(cls,rpt):
        rpt.add_action(PrintAction())
        rpt.add_action(ClearCacheAction())
        #~ rpt.add_action(EditTemplateAction(rpt))
        #~ super(Printable,cls).setup_report(rpt)

    def get_print_language(self,pm):
        return babel.DEFAULT_LANGUAGE
        
    def get_print_templates(self,bm,action):
        """Return a list of filenames of templates for the specified build method.
        Returning an empty list means that this item is not printable. 
        For subclasses of :class:`SimpleBuildMethod` the returned list 
        may not contain more than 1 element.
        """
        return [ action.filename_root(self) + bm.template_ext ]
          
    def unused_get_last_modified_time(self):
        """Return a model-specific timestamp that expresses when 
        this model instance has been last updated. 
        Default is to return None which means that existing target 
        files never get overwritten.
        
        """
        return None
        
    def unused_must_rebuild_target(self,filename,pm):
        """When the target document already exists, 
        return True if it should be built again (overriding the existing file. 
        The default implementation is to call :meth:`get_last_modified_time` 
        and return True if it is newer than the timestamp of the file.
        """
        last_modified = self.get_last_modified_time()
        if last_modified is None:
            return False
        mtime = os.path.getmtime(filename)
        #~ st = os.stat(filename)
        #~ mtime = st.st_mtime
        mtime = datetime.datetime.fromtimestamp(mtime)
        if mtime >= last_modified:
            return False
        return True
      
    def get_build_method(self):
        # TypedPrintable  overrides this
        #~ return 'rtf'
        return settings.LINO.config.default_build_method 
        #~ return settings.LINO.preferred_build_method 
        #~ return 'pisa'
        

class TypedPrintable(Printable):
    """
    A TypedPrintable model must define itself a field `type` which is a ForeignKey 
    to a Model that implements :class:`PrintableType`.
    
    Alternatively you can override :meth:`get_printable_type` 
    if you want to name the field differently. An example of 
    this is :attr:`lino.modlib.sales.models.SalesDocument.imode`.
    """
    
    type = NotImplementedError
    """
    Override this by a ForeignKey field.
    """
  
    class Meta:
        abstract = True
        
    def get_printable_type(self):
        return self.type
        
    def get_build_method(self):
        ptype = self.get_printable_type()
        if ptype is None:
            return super(TypedPrintable,self).get_build_method()
        if ptype.build_method:
            return ptype.build_method
        return settings.LINO.config.default_build_method 
        
    def get_print_templates(self,bm,action):
        ptype = self.get_printable_type()
        if ptype is None:
            return super(TypedPrintable,self).get_print_templates(bm,action)
        if not ptype.template.endswith(bm.template_ext):
            raise Exception(
              "Invalid template configured for %s %r. Expected filename ending with %r." %
              (ptype.__class__.__name__,unicode(ptype),bm.template_ext))
        return [ ptype.get_templates_group() + '/' + ptype.template ]
        
    def get_print_language(self,bm):
        return self.language


#~ class PrintableTypes(reports.Report):
    #~ column_names = 'name build_method template *'


#~ class VolatileModel(models.Model):
  
    #~ class Meta:
        #~ abstract = True
    
    #~ def save(self,*args,**kw):
        #~ raise Exception("This is a VolatileModel!")

  
import cgi


class Listing(Printable):
    
    class Meta:
        abstract = True
    
    date = models.DateField(
        blank=True,null=True,
        verbose_name=_("Date"))
        
    #~ title = models.CharField(max_length=200,
      #~ verbose_name=_("Title"),
      #~ blank=True)
    #~ """
    #~ The title of the listing.
    #~ """
    
    @classmethod
    def setup_report(model,rpt):
        u"""
        """
        #~ rpt.get_action('listing').label = model.__name__
        rpt.add_action(DirectPrintAction('print',_("Print"),'Listing.odt'))
        #~ rpt.add_action(InititateListing('listing',_("Print"),'listing.odt'))
        
    def __unicode__(self):
        return force_unicode(self.title)
        #~ return self.get_title()
        
    def get_title(self):
        return self._meta.verbose_name # "Untitled Listing"
    title = property(get_title)
        
    def header(self):
        return '<p align="center"><b>%s</b></p>' % cgi.escape(self.title)
        
    def footer(self):
        html = '<td align="left">%s</td>' % 'left footer'
        html += '<td align="right">Page X of Y</td>'
        html = '<table width="100%%"><tr>%s</tr></table>' % html
        return html
        
    def body(self):
        raise NotImplementedError
        
    #~ def preview(self,request):
        #~ return self.header() + self.body() + self.footer()
    #~ preview.return_type = fields.HtmlBox(_("Preview"))
    
    def get_preview(self,request):
        return self.header() + self.body() + self.footer()
    preview = fields.VirtualField(fields.HtmlBox(_("Preview")),get_preview)
    
    
class InitiateListing(reports.InsertRow):
    callable_from = tuple()
    name = 'listing'
    #~ label = _("Insert")
    key = None
    
    def get_action_title(self,rh):
        return u"Initiate Listing «%s»" % self.actor.model._meta.verbose_name
  
        
class Listings(reports.Report):
    model = Listing
    
    def setup_actions(self):
        #~ print 'lino.mixins.printable.Listings.setup_actions : ', self.model
        alist = []
        #~ if len(self.detail_layouts) > 0:
        if True:
            self.detail_action = reports.ShowDetailAction(self)
            alist.append(self.detail_action)
            alist.append(reports.SubmitDetail())
            alist.append(InitiateListing(self,label=self.model._meta.verbose_name)) # replaces InsertRow
            alist.append(reports.SubmitInsert())
        alist.append(reports.DeleteSelected())
        self.set_actions(alist)
        
    