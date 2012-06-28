# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
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
import errno
import sys
from optparse import make_option 
from os.path import join

from Cheetah.Template import Template as CheetahTemplate

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode 
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import loading
#~ from django.db import models
#~ from django.contrib.contenttypes.models import ContentType
#~ from lino.core import actors
#~ from lino.utils import get_class_attr

import re
import lino
from lino.core.modeltools import app_labels
from lino.utils import confirm, curry
from lino.utils.config import find_config_file
from lino.utils import rstgen 
from lino.utils import babel
from lino.core import table

from lino.core.modeltools import makedirs_if_missing, full_model_name

# Copied from doctest:

# This regular expression finds the indentation of every non-blank
# line in a string.
_INDENT_RE = re.compile('^([ ]*)(?=\S)', re.MULTILINE)

def min_indent(s):
    "Return the minimum indentation of any non-blank line in `s`"
    indents = [len(indent) for indent in _INDENT_RE.findall(s)]
    if len(indents) > 0:
        return min(indents)
    else:
        return 0
        
def doc2rst(s):
    if s is None:
        return ''
    s = s.expandtabs()
    # If all lines begin with the same indentation, then strip it.
    mi = min_indent(s)
    if mi > 0:
        s = '\n'.join([l[mi:] for l in s.split('\n')])
    return s


def abstract(o,indent=0):
    s = doc2rst(o.__doc__).strip()
    if not s: return '(no docstring)'
    paras = s.split('\n\n',1)
    par = paras[0]
    if indent:
        par = (' '*indent).join(par.splitlines())
    return par
    
def fieldtype(f):
    if isinstance(f,models.ForeignKey):
        return f.__class__.__name__ + " to " + refto(f.rel.to)
    return f.__class__.__name__
        
def report_ref(rpt):
    return settings.LINO.source_name + '.' + str(rpt)
    #~ return ":ref:`%s.%s`" % (settings.LINO.source_name,str(rpt))  
    
def model_ref(model):
    return settings.LINO.source_name + '.' + model._meta.app_label + '.' + model.__name__
    
    
def refto(x):
    if x is None: 
        return '`None`'
    if issubclass(x,models.Model):
        return ':doc:`' + x.__name__ + ' <' + full_model_name(x) + '>`'
    #~ if isinstance(x,Field):
    return ':ref:`' + x.verbose_name + ' <' + settings.LINO.source_name \
        + '.' + full_model_name(x.model) + '.' + x.name + '>`'
    

def model_overview(model):
    headers = ["name","type"]
    #~ formatters = [
      #~ lambda f: f.name,
      #~ lambda f: f.__class__.__name__,
    #~ ]
    headers.append("verbose name")
    #~ for lng in babel.AVAILABLE_LANGUAGES:
        #~ headers.append("verbose name (" + lng + ")")
    #~ headers.append("help text")
    #~ formatters.append(lambda f: f.help_text)
    def verbose_name(f):
        babel.set_language(babel.DEFAULT_LANGUAGE)
        label_en = force_unicode(_(f.verbose_name))
        babel_labels = []
        for lng in babel.AVAILABLE_LANGUAGES:
            if lng != babel.DEFAULT_LANGUAGE:
                babel.set_language(lng)
                label = force_unicode(_(f.verbose_name))
                if label != label_en:
                    babel_labels.append(label)
        if babel_labels:
            label_en += " (%s)" % ",".join(babel_labels)
        return label_en
        
    def rowfmt(f):
        cells = [
          f.name,
          fieldtype(f),
          verbose_name(f)
        ]
        #~ for lng in babel.AVAILABLE_LANGUAGES:
            #~ babel.set_language(lng)
            #~ cells.append(force_unicode(_(f.verbose_name)))
        #~ cells.append(f.help_text)
        return cells
    rows = [ rowfmt(f) for f in model._meta.fields ]
    s = rstgen.table(headers,rows)
    
    model_reports = [r for r in table.master_reports if r.model is model]
    if model_reports:
        s += '\n\nMaster tables: %s\n\n' % rptlist(model_reports)
    if getattr(model,'_lino_slaves',None):
        s += '\n\nSlave tables: %s\n\n' % rptlist(model._lino_slaves.values())
        #~ s += '\n\nSlave reports: ' 
        #~ s += ', '.join([name for name,rpt in model._lino_slaves.items()])
        #~ s += '\n\n' 
    return s
    
def rptlist(l):
    return ', '.join([
        ":ref:`%s (%s) <%s>`" % (str(rpt),force_unicode(rpt.label),report_ref(rpt)) 
        for rpt in l])

def model_referenced_from(model):
    #~ headers = ["name","description"]
    #~ rows = []
    def ddhfmt(ddh):
        return ', '.join([':ref:`%s.%s`' % (model_ref(model),fk.name) 
            for model,fk in ddh.fklist])
    return ddhfmt(model._lino_ddh)
    #~ rows.append(['_lino_ddh',ddhfmt(model._lino_ddh)])
    #~ return rstgen.table(headers,rows)
    
  

class GeneratingCommand(BaseCommand):
    tmpl_dir = ''
    args = "output_dir"
    
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', 
            dest='interactive', default=True,
            help='Do not prompt for input of any kind.'),
        #~ make_option('--overwrite', action='store_true', 
            #~ dest='overwrite', default=False,
            #~ help='Overwrite existing files.'),
    ) 
    
    def create_parser(self, prog_name, subcommand):
        self.subcommand = subcommand
        return super(GeneratingCommand,self).create_parser(prog_name, subcommand)
        
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("No output_dir specified.")
            
        self.output_dir = os.path.abspath(args[0])
        if not os.path.exists(self.output_dir):
            raise CommandError("Specified output_dir %s does not exist." % self.output_dir)
        #~ self.overwrite
        #~ self.output_dir = os.path.abspath(output_dir)
        self.generated_count = 0
        self.options = options
        
        logger.info("Running %s to %s.", self, self.output_dir)
        self.generate_files()
        logger.info("Generated %s files",self.generated_count)
        
    def generate(self,tplname,fn,**context):
        #~ if self.tmpl_dir:
            #~ tplname = join(self.tmpl_dir,tplname)
        #~ tplname = self.subcommand + '/' + tplname
        tpl_filename = find_config_file(tplname,self.tmpl_dir)
        if tpl_filename is None:
            raise Exception("No file %s found" % tplname)
        if isinstance(tpl_filename,unicode):
            tpl_filename = tpl_filename.encode(sys.getfilesystemencoding())
        tpl_filename = os.path.abspath(tpl_filename)
        fn = join(self.output_dir,fn)
        
        #~ if os.path.exists(fn):
            #~ if not self.options.get('overwrite'):
                #~ if not confirm("Overwrite existing file %s (y/n) ?" % fn):
                    #~ logger.info("Skipping %s because file exists.",fn)
                    #~ return 
        #~ else:
            #~ mkdir_if(os.path.dirname(fn))
            
        makedirs_if_missing(os.path.dirname(fn))
        
        logger.info("Generating %s",fn)
        #~ logger.info("Generating %s from %s",fn,tpl_filename)
        context.update(
          lino=lino,
          #~ models=models,
          settings=settings,
          app_labels=app_labels)
        #~ d = dict(site=site)
        #~ print 20110223, [m for m in models.get_models()]
        #~ print 20110315, context
        tpl = CheetahTemplate(file=tpl_filename,namespaces=[context])
        #~ tpl = CheetahTemplate(file(tpl_filename).read(),namespaces=[context])
        s = unicode(tpl)
        #~ print s
        file(fn,'w').write(s.encode('utf-8'))
        self.generated_count += 1
        
        
class Command(GeneratingCommand):
    help = """Writes a Sphinx documentation tree about models on this Site.
    """
    tmpl_dir = 'makedocs'
    
    def generate_files(self):
      
        from lino.ui.extjs3 import UI
        #~ UI = settings.LINO.get_ui_class
        ui = UI(make_messages=True)
        #~ # install Lino urls under root location (`/`)
        #~ ui = urlpatterns = ui.get_patterns()
        #~ settings.LINO.setup()
        ui.make_linolib_messages()
            
        context = dict(
          header=rstgen.header,
          h1=curry(rstgen.header,1),
          table=rstgen.table,
          doc=doc2rst,
          loading=loading,
          models=models,
          abstract=abstract,
          refto=refto,
          #~ py2rst=rstgen.py2rst,
          full_model_name=full_model_name,
          model_overview=model_overview,
          model_referenced_from=model_referenced_from,
          model_ref=model_ref,
        )
        self.generate('index.rst.tmpl','index.rst',**context)
        for a in loading.get_apps():
            app_label = a.__name__.split('.')[-2]
            app_models = models.get_models(a,include_auto_created=True)
            context.update(
                app=a, 
                app_label=app_label, 
                app_models=app_models
                )
            self.generate('app.rst.tmpl','%s.rst' % app_label, **context)
            for model in app_models:
                context.update(
                    model=model, 
                    )
                self.generate('model.rst.tmpl','%s.rst' % 
                    full_model_name(model), **context)
            
