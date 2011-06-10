## Copyright 2002-2011 Luc Saffre
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
Lino is a Python package to be used on Django sites.
See :doc:`/admin/install` on how to use it.

"""

import os
import sys
import datetime
from tempfile import gettempdir
from os.path import join, abspath, dirname, normpath
import logging

__version__ = "1.1.14+"
"""
Lino version number. 
The latest released version is :doc:`/releases/20110610`.
"""

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

__url__ = "http://lino.saffre-rumma.net"
#~ __url__ = "http://code.google.com/p/lino/"

__copyright__ = """\
Copyright (c) 2002-2011 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""


if False: 
    """
    subprocess.Popen() took very long and even got stuck on Windows XP.
    I didn't yet explore this phenomen more.
    """
    # Copied from Sphinx <http://sphinx.pocoo.org>
    from os import path
    package_dir = path.abspath(path.dirname(__file__))
    if '+' in __version__ or 'pre' in __version__:
        # try to find out the changeset hash if checked out from hg, and append
        # it to __version__ (since we use this value from setup.py, it gets
        # automatically propagated to an installed copy as well)
        try:
            import subprocess
            p = subprocess.Popen(['hg', 'id', '-i', '-R',
                                  path.join(package_dir, '..', '..')],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if out:
                __version__ += ' (Hg ' + out.strip() +')'
            #~ if err:
                #~ print err
        except Exception:
            pass


NOT_FOUND_MSG = '(not installed)'

def using():
    """
    Yields a list of third-party software descriptors used by Lino.
    Each descriptor is a tuple (name, version, url).
    
    """
    import sys
    version = "%d.%d.%d" % sys.version_info[:3]
    yield ("Python",version,"http://www.python.org/")
    
    import django
    yield ("Django",django.get_version(),"http://www.djangoproject.com")
    
    import dateutil
    version = getattr(dateutil,'__version__','')
    yield ("python-dateutil",version,"http://labix.org/python-dateutil")
    
    try:
        import Cheetah
        version = Cheetah.Version 
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("Cheetah",version ,"http://cheetahtemplate.org/")

    try:
        import docutils
        version = docutils.__version__
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("docutils",version ,"http://docutils.sourceforge.net/")

    import yaml
    version = getattr(yaml,'__version__','')
    yield ("PyYaml",version,"http://pyyaml.org/")
    
    if False:
        try:
            import pyratemp
            version = getattr(pyratemp,'__version__','')
        except ImportError:
            version = NOT_FOUND_MSG
        yield ("pyratemp",version,"http://www.simple-is-better.org/template/pyratemp.html")
    
    try:
        import ho.pisa as pisa
        version = getattr(pisa,'__version__','')
        yield ("xhtml2pdf",version,"http://www.xhtml2pdf.com")
    except ImportError:
        pass

    import reportlab
    yield ("ReportLab Toolkit",reportlab.Version, "http://www.reportlab.org/rl_toolkit.html")
               
    try:
        #~ import appy
        from appy import version
        version = version.verbose
    except ImportError:
        version = NOT_FOUND_MSG
    yield ("appy.pod",version ,"http://appyframework.org/pod.html")


def welcome_text():
    return "Lino version %s using %s" % (
      __version__, 
      ', '.join(["%s %s" % (n,v) for n,v,u in using()]))

def welcome_html():
    return "Lino version %s using %s" % (
      __version__,
      ', '.join(['<a href="%s" target="_blank">%s</a> %s' % (u,n,v) for n,v,u in using()]))


class Lino(object):
    """
    Base class for the Lino Application instance stored in :setting:`LINO`.
    
    Subclasses of this can be defined and instantiated in Django settings files.
    
    This class is first defined in :mod:`lino`, then subclassed by 
    :mod:`lino.apps.dsbe.settings` or 
    :mod:`lino.apps.igen.settings`,
    which is imported into your local :xfile:`settings.py`,
    where you may subclass it another time.
    
    """
    
    help_url = "http://code.google.com/p/lino"
    #~ index_html = "This is the main page."
    title = "Base Lino Application"
    domain = "www.example.com"
    
    #~ bypass_perms = False
    
    use_awesome_uploader = False
    """
    Whether to use AwesomeUploader. 
    This feature was experimental and doesn't yet work (and maybe never will).
    """
    
    textfield_format = 'plain'
    """
    The default format for text fields. 
    Valid choices are currently 'plain' and 'html'.
    
    Text fields are either Django's `models.TextField` 
    or :class:`lino.fields.RichTextField`.
    
    You'll probably better leave the global option as 'plain', 
    and specify explicitly the fields you want as html by declaring 
    them::
    
      foo = fields.RichTextField(...,format='html')
    
    We even recommend that you declare your *plain* text fields also 
    using `fields.RichTextField` and not `models.TextField`::
    
      foo = fields.RichTextField()
    
    Because that gives subclasses of your application the possibility to 
    make that specific field html-formatted::
    
       resolve_field('Bar.foo').set_format('html')
       
    """
    
    use_tinymce = True
    """
    Whether to use TinyMCE instead of Ext.form.HtmlEditor. 
    See :doc:`/blog/2011/0523`
    """
    
    use_vinylfox = False
    """
    Whether to use VinylFox extensions for HtmlEditor. 
    This feature was experimental and doesn't yet work (and maybe never will).
    See :doc:`/blog/2011/0523`.
    """
    
    
    date_format_strftime = '%d.%m.%Y'
    date_format_extjs = 'd.m.Y'
    
    def parse_date(self,s):
        """Convert a string formatted using :attr:`date_format_xxx` to a datetime.date instance.
        See :doc:`/blog/2010/1130`.
        """
        ymd = reversed(map(int,s.split('.')))
        return datetime.date(*ymd)

    alt_date_formats_extjs = 'd/m/Y|Y-m-d'



    
    
    #~ preferred_build_method = 'pisa'
    #~ preferred_build_method = 'appypdf'
    
    csv_params = dict()
    """
    Site-wide default parameters for CSV generation.
    This must be a dictionary that will be used 
    as keyword parameters to Python `csv.writer()
    <http://docs.python.org/library/csv.html#csv.writer>`_
    
    Possible keys include:
    
    - encoding : 
      the charset to use when responding to a CSV request.
      See 
      http://docs.python.org/library/codecs.html#standard-encodings
      for a list of available values.
      
    - many more allowed keys are explained in
      `Dialects and Formatting Parameters
      <http://docs.python.org/library/csv.html#csv-fmt-params>`_.
    
    """
    
    propvalue_max_length = 200
    """
    Used by :mod:`lino.modlib.properties`.
    """
    
    appy_params = dict(ooPort=8100)
    """
    Used by :class:`lino.mixins.printable.AppyBuildMethod`.
    """
    
    source_dir = os.path.dirname(__file__)
    source_name = os.path.split(source_dir)[-1]
    
    def __init__(self,project_file): # ,settings_dict=None):
        #self.django_settings = settings
        #~ self.init_site_config = lambda sc: sc
        self.project_dir = normpath(dirname(project_file))
        self.project_name = os.path.split(self.project_dir)[-1]
        self.qooxdoo_prefix = '/media/qooxdoo/lino_apps/' + self.project_name + '/build/'
        self.dummy_messages = set()
        self._setting_up = False
        self._setup_done = False
        self.root_path = '/lino/'
        self._response = None
        
        #~ self.appy_params.update(pythonWithUnoPath=r'C:\PROGRA~1\LIBREO~1\program\python.exe')
        #~ APPY_PARAMS.update(pythonWithUnoPath=r'C:\PROGRA~1\OPENOF~1.ORG\program\python.exe')
        #~ APPY_PARAMS.update(pythonWithUnoPath='/usr/bin/libreoffice')
        #~ APPY_PARAMS.update(pythonWithUnoPath='/etc/openoffice.org3/program/python')
    
        #~ if settings_dict: 
            #~ self.install_settings(settings_dict)
            
    #~ def install_settings(self,s):
        #~ s.update(DATABASES= {
              #~ 'default': {
                  #~ 'ENGINE': 'django.db.backends.sqlite3',
                  #~ 'NAME': join(LINO.project_dir,'test.db')
              #~ }
            #~ })
        
        
        #~ self.source_name = os.path.split(self.source_dir)[-1]
        #~ # find the first base class that is defined in the Lino source tree
        #~ # this is to find out the source_name and the source_dir
        #~ for cl in self.__class__.__mro__:
            #~ if cl.__module__.startswith('lino.apps.'):
                #~ self.source_dir = os.path.dirname(__file__)
                #~ self.source_name = self.source_dir
                #~ os.path.split(_source_dir,
              
            
        # ImportError: Settings cannot be imported, because environment variable DJANGO_SETTINGS_MODULE is undefined.
        #~ from lino.models import get_site_config
        #~ self.config = get_site_config()
        

    def add_dummy_message(self,s):
        self.dummy_messages.add(s)

    def setup_main_menu(self):
        pass

    def configure(self,sc):
        self.config = sc
        
    def setup(self):
        """
        This is called for example from :mod:`lino.ui.extjs3.urls`. 
        It is not defined here because it uses Django modules 
        which we would need to import locally.
        """
        from lino.core.kernel import setup_site
        setup_site(self)

        
    def add_menu(self,*args,**kw):
        return self.main_menu.add_menu(*args,**kw)

    def context(self,request,**kw):
        d = dict(
          main_menu = menus.MenuRenderer(self.main_menu,request),
          root_path = self.root_path,
          lino = self,
          settings = settings,
          debug = True,
          #skin = self.skin,
          request = request
        )
        d.update(kw)
        return d
        
    def select_ui_view(self,request):
        html = '<html><body>'
        html += 'Please select a user interface: <ul>'
        for ui in self.uis:
            html += '<li><a href="%s">%s</a></li>' % (ui.name,ui.verbose_name)
        html += '</ul></body></html>'
        return HttpResponse(html)
        
        
    def get_site_menu(self,user):
        #~ self.setup()
        assert self._setup_done
        return self.main_menu.menu_request(user)
        
