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

import os
import logging
import cStringIO

from django.conf import settings
from django.template.loader import render_to_string, get_template, select_template, Context, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.translation import ugettext_lazy as _

try:
    import ho.pisa as pisa
    #pisa.showLogging()
except ImportError:
    pisa = None
    
import lino
from lino import actions

try:
    import appy
except ImportError:
    appy = None
    
#~ if False:
    #~ try:
        #~ from lino.utils import appy_pod
    #~ except ImportError:
        #~ appy_pod = None
        
class MultiTableBase:
  
    """
    Mixin for Models that use Multi-table inheritance[1].
    Subclassed by lino.modlib.journals.models.AbstractDocument
    
    [1] http://docs.djangoproject.com/en/dev/topics/db/models/#multi-table-inheritance)
    """
    
    class Meta:
        abstract = True
    
    def get_child_model(self):
        return self.__class__
        
    def get_child_instance(self):
        model = self.get_child_model()
        if model is self.__class__:
            return self
        related_name = model.__name__.lower()
        return getattr(self,related_name)
        
pm_dict = {}
pm_list = []
        
class PrintAction(actions.Action):
    #~ name = 'print'
    #~ needs_selection = True
    #~ label = _("Print")
    #~ format = 'pdf'
    def __init__(self,actor,pm):
        self.pm = pm
        self.name = pm.name
        self.label = pm.label
        actions.Action.__init__(self,actor)


class Printable:
    """
    Mixin for Models whose instances can "print" a document.
    """
    
  
    #~ @classmethod
    #~ def setup_report(cls,rpt):
        #~ rpt.add_actions(PdfAction)
        
    #~ def odt_template(self):
        # when using appy_pod
        #~ return self.filename_root() +'.odt'
        #~ return os.path.join(os.path.dirname(__file__),
                            #~ 'odt',self._meta.db_table)+'.odt'
    #~ def html_templates(self):
        # when using pisa
        #~ return [ self.filename_root() +'.pisa.html' ]
        #~ return [ '%s.%s.pisa.html' % (self._meta.app_label,self.__class__.__name__) ]

    #~ def rtf_templates(self):
        #~ return [ self.filename_root() +'.rtf' ]

    def filename_root(self):
        return self._meta.app_label + '.' + self.__class__.__name__
        
    def get_print_templates(self,pm):
        return [self.filename_root() + pm.template_ext]
          
    def get_target_parts(self,pm):
        return ['cache', pm.name, self.filename_root() + '-' + str(self.pk) + '.' + pm.target_format]
        
    #~ def rtf_target_parts(self):
        #~ return ['cache', 'rtf', self.filename_root(), str(self.pk)+'.rtf']

    #~ def pdf_target_path(self):
        #~ return os.path.join(settings.MEDIA_ROOT,*self.pdf_target_parts())
        
    #~ def pdf_target_url(self):
        #~ return settings.MEDIA_URL + "/".join(self.pdf_target_parts())
        
    def get_last_modified_time(self):
        return None
        
    def get_print_method(self):
        ## e.g. lino.modlib.notes.Note overrides this
        return 'pisa'
        

            
    #~ def view_pdf(self,request):
        #~ self.make_pdf()
        #~ s = open(self.pdf_path()).read()
        #~ return HttpResponse(s,mimetype='application/pdf')
        
    #~ def view_printable(self,request):
        #~ return HttpResponse(self.make_pisa_html())
        


class PrintMethod:
    name = None
    label = None
    target_format = None
    template_ext = None
    def __init__(self):
        if self.label is None:
            self.label = _(self.__class__.__name__)
            
    def __unicode__(self):
        return unicode(self.label)
            
    def build(self,elem):
        pass
        
    def get_target_name(self,elem):
        return os.path.join(settings.MEDIA_ROOT,*elem.get_target_parts(self))
        
    def get_target_url(self,elem):
        self.build(elem)
        return settings.MEDIA_URL + "/".join(elem.get_target_parts(self))
        
    def prepare_cache(self,elem):
        filename = self.get_target_name(elem)
        if not filename:
            return
        last_modified = elem.get_last_modified_time() 
        if last_modified is not None and os.path.exists(filename):
            mtime = os.path.getmtime(filename)
            #~ st = os.stat(filename)
            #~ mtime = st.st_mtime
            mtime = datetime.datetime.fromtimestamp(mtime)
            if mtime >= last_modified:
                lino.log.debug("%s : %s -> %s is up to date",self,elem,filename)
                return
            os.remove(filename)
        lino.log.debug("%s : %s -> %s", self,elem,filename)
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            if True:
                raise Exception("Please create yourself directory %s" % dirname)
            else:
                os.makedirs(dirname)
        return filename
        
    def get_template(self,elem):
        tpls = elem.get_print_templates(self)
        if len(tpls) == 0:
            raise Exception("No templates defined for %r" % elem)
        #~ lino.log.debug('make_pisa_html %s',tpls)
        try:
            return select_template(tpls)
        except TemplateDoesNotExist:
            raise Exception("No template found for %s" % tpls)

        
    def render_template(self,elem,tpl): # ,MEDIA_URL=settings.MEDIA_URL):
        url = settings.MEDIA_ROOT.replace('\\','/') + '/'
        context = dict(
          instance=elem,
          title = unicode(elem),
          MEDIA_URL = url,
        )
        return tpl.render(Context(context))
        

class PicturePrintMethod(PrintMethod):
    name = 'picture'
    def get_target_name(self,elem):
        return os.path.join(settings.MEDIA_ROOT,*elem.get_target_parts(self))
        
class AppyPrintMethod(PrintMethod):
    name = 'appy'
    target_format = 'odt'
    label = _("odt")
    template_ext = '.odt'  
    def build(self,elem):
        tpls = elem.get_print_templates(self)
        if len(tpls) == 0:
            raise Exception("No templates defined for %r" % elem)
        #~ tpl = self.get_template(elem) 
        tpl = os.path.join(settings.DATA_DIR,'templates',tpls[0])
        target = self.prepare_cache(elem)
        if target is None:
            return
        context = dict(instance=self)
        from appy.pod.renderer import Renderer
        renderer = Renderer(tpl, context, target)
        renderer.run()
        #~ appy_pod.process_pod(template,context,filename)
        
class PisaPrintMethod(PrintMethod):
    name = 'pisa'
    target_format = 'pdf'
    label = _("PDF")
    template_ext = '.pisa.html'  
    
    def build(self,elem):
        tpl = self.get_template(elem) 
        filename = self.prepare_cache(elem)
        if filename is None:
            return
        #~ url = settings.MEDIA_ROOT.replace('\\','/') + '/'
        html = self.render_template(elem,tpl) # ,MEDIA_URL=url)
        html = html.encode("ISO-8859-1")
        file(filename+'.html','w').write(html)
        result = cStringIO.StringIO()
        h = logging.FileHandler(filename+'.log','w')
        pisa.log.addHandler(h)
        pdf = pisa.pisaDocument(cStringIO.StringIO(html), result)
        pisa.log.removeHandler(h)
        h.close()
        file(filename,'wb').write(result.getvalue())
        if pdf.err:
            raise Exception("pisa.pisaDocument.err is %r" % pdf.err)
        
        
class RtfPrintMethod(PrintMethod):
  
    name = 'rtf'
    label = _("RTF")
    target_format = 'rtf'
    template_ext = '.rtf'  
    
    def build(self,elem):
        tpl = self.get_template(elem) 
        filename = self.prepare_cache(elem)
        if filename is None:
            return
        result = self.render_template(elem,tpl) # ,MEDIA_URL=url)
        file(filename,'wb').write(result)
        
    
def register_print_method(pm):
    pm_dict[pm.name] = pm
    pm_list.append(pm)
    

if pisa:
    register_print_method(PisaPrintMethod())
if appy:
    register_print_method(AppyPrintMethod())
register_print_method(RtfPrintMethod())
register_print_method(PicturePrintMethod())

def print_method_choices():
  return [ (pm.name,unicode(pm.label) ) for pm in pm_list]

def get_print_method(name):
    return pm_dict.get(name)
