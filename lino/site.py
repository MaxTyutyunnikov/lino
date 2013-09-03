# -*- coding: UTF-8 -*-
## Copyright 2002-2013 Luc Saffre
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

from __future__ import unicode_literals

import os
import sys
import cgi
import inspect
import datetime

from os.path import join, abspath, dirname, normpath, isdir
from decimal import Decimal

from lino.utils.xmlgen import html as xghtml
from lino.utils import AttrDict

#~ from lino import SETUP_INFO

from north import Site


class Site(Site):
    """
    This is the base for :class:`lino.ui.site.Site`.
    """
    
    user_model = None
    "See :attr:`lino.ui.Lino.user_model`."
    
    project_model = None
    "See :attr:`lino.ui.Lino.project_model`."
    
    override_modlib_models = set()
    "See :attr:`lino.ui.Site.override_modlib_models`."
    
    
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
    
    help_url = "http://code.google.com/p/lino"
    #~ site_url = 
    #~ index_html = "This is the main page."
    #~ title = None
    title = "Unnamed Lino site"
    #~ domain = "www.example.com"
    
    
    catch_layout_exceptions = True
    """
    Lino usually catches any exception during 
    :meth:`lino.ui.extjs3.ExtUI.create_layout_element`
    to report errors of style 
    "Unknown element "postings.PostingsByController ('postings')" 
    referred in layout <PageDetail on pages.Pages>."
    
    Setting this to `False` is
    useful when there's some problem *within* the framework.
    
    """
    
    
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
    
    appy_params = dict(ooPort=8100)
    """
    Used by :class:`lino.mixins.printable.AppyBuildMethod`.
    """
    
    
    modules = AttrDict() 
    # this is explained in the polls tutorial
    # cannot use autodoc for this attribute 
    # because autodoc shows the "default" value
    
    
    #~ decimal_separator = '.'
    decimal_separator = ','
    """
    Set this to either ``'.'`` or ``','`` to define wether to use 
    comma or dot as decimal point separator when entering 
    a `DecimalField`.
    """
    
    #~ decimal_group_separator = ','
    decimal_group_separator = ' '
    """
    Decimal group separator for :func:`lino.utils.moneyfmt`.
    """

    
    time_format_strftime = '%H:%M'
    """
    Format (in strftime syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_time`.
    """
    
    date_format_strftime = '%d.%m.%Y'
    """
    Format (in strftime syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.
    """
    
    #~ date_format_regex = "/^[0123]\d\.[01]\d\.-?\d+$/"
    date_format_regex = "/^[0123]?\d\.[01]?\d\.-?\d+$/"
    """
    Format (in Javascript regex syntax) to use for displaying dates to the user.
    If you change this setting, you also need to override :meth:`parse_date`.
    """
    
    datetime_format_strftime = '%Y-%m-%dT%H:%M:%S'
    """
    Format (in strftime syntax) to use for formatting timestamps in AJAX responses.
    If you change this setting, you also need to override :meth:`parse_datetime`.
    """
    
    datetime_format_extjs = 'Y-m-d\TH:i:s'
    """
    Format (in ExtJS syntax) to use for formatting timestamps in AJAX calls.
    If you change this setting, you also need to override :meth:`parse_datetime`.
    """
    
    
    
    
    def init_before_local(self,*args):
        super(Site,self).init_before_local(*args)
        
        self.GFK_LIST = []
        self.VIRTUAL_FIELDS = []
        
        self.update_settings(
            LOGGING_CONFIG='lino.utils.log.configure',
            LOGGING=dict(filename=None,
                level='INFO',
                logger_names='djangosite north lino',
                disable_existing_loggers=True, # Django >= 1.5
                ),
            )
        
        
    def parse_date(self,s):
        """
        Convert a string formatted using 
        :attr:`date_format_strftime` or  :attr:`date_format_extjs` 
        into a `(y,m,d)` tuple (not a `datetime.date` instance).
        See `/blog/2010/1130`.
        """
        ymd = tuple(reversed(map(int,s.split('.'))))
        assert len(ymd) == 3
        return ymd
        #~ return datetime.date(*ymd)
        
    def parse_time(self,s):
        """
        Convert a string formatted using 
        :attr:`time_format_strftime` or  :attr:`time_format_extjs` 
        into a datetime.time instance.
        """
        hms = map(int,s.split(':'))
        return datetime.time(*hms)
        
    def parse_datetime(self,s):
        """
        Convert a string formatted using
        :attr:`datetime_format_strftime` or  :attr:`datetime_format_extjs` 
        into a datetime.datetime instance.
        """
        #~ print "20110701 parse_datetime(%r)" % s
        #~ s2 = s.split()
        s2 = s.split('T')
        if len(s2) != 2:
            raise Exception("Invalid datetime string %r" % s)
        ymd = map(int,s2[0].split('-'))
        hms = map(int,s2[1].split(':'))
        return datetime.datetime(*(ymd+hms))
        #~ d = datetime.date(*self.parse_date(s[0]))
        #~ return datetime.combine(d,t)

    ignore_dates_before = datetime.date.today() + datetime.timedelta(days=-7)
    """
    Ignore dates before the gived date. 
    Set this to None if you want no limit.
    """
    
    #~ def get_user_model(self):
        #~ if 'django.contrib.auth' in self.django_settings['INSTALLED_APPS']:
            #~ from django.contrib.auth.models import User
            #~ return 'auth.User'
        #~ else:
            #~ from lino.modlib.users.models import User
        #~ return User
        #~ return 'users.User'
      
        

    #~ def add_dummy_message(self,s):
        #~ self.dummy_messages.add(s)

    #~ def get_app_source_file(self):
        #~ "Override this in each application"
        #~ return __file__
        
    #~ def analyze_models(self):
        #~ from lino.core.kernel import analyze_models
        #~ analyze_models()
        
    def resolve_virtual_fields(self):
        #~ print "20130827 resolve_virtual_fields", len(self.VIRTUAL_FIELDS)
        #~ global VIRTUAL_FIELDS
        for vf in self.VIRTUAL_FIELDS: 
            vf.lino_resolve_type()
        #~ VIRTUAL_FIELDS = None
        self.VIRTUAL_FIELDS = []
      
        
    def register_virtual_field(self,vf):
        #~ print "20130827 register_virtual_field", vf
        self.VIRTUAL_FIELDS.append(vf)
        
        
    def do_site_startup(self):
        """
        Start the Lino instance (the object stored as :setting:`LINO` in 
        your :xfile:`settings.py`).
        This is called exactly once from :mod:`lino.models` 
        when Django has has populated it's model cache.
        
        This code can run several times at once when running e.g. under mod_wsgi: 
        another thread has started and not yet finished `startup_site()`.
        
        """
        super(Site,self).do_site_startup()
        from lino.core.kernel import startup_site
        startup_site(self)
        
    #~ def shutdown(self):
        #~ return super(Site,self).shutdown()
        #~ from lino.core.kernel import shutdown_site
        #~ shutdown_site(self)
#~ 
        
    def setup_workflows(self):
        self.on_each_app('setup_workflows')
        
    def setup_choicelists(self):
        """
        Redefine application-specific Choice Lists.
        
        Especially used to define application-specific
        :class:`UserProfiles <lino.core.perms.UserProfiles>`.
        
        Lino by default has two user profiles "User" 
        and "Administrator", defined in :mod:`lino.core.perms`.
        
        Application developers who use group-based requirements 
        must override this in their application's :xfile:`settings.py` 
        to provide a default list of user profiles for their 
        application.
        
        See the source code of :mod:`lino.projects.presto` 
        or :mod:`lino.projects.pcsw` for a usage example.
        
        Local site administrators may again override this in their 
        :xfile:`settings.py`.
        
        Note that you may not specify values longer 
        than `max_length` when redefining your choicelists.
        This limitation is because these redefinitions happen at a 
        moment where database fields have already been instantiated, 
        so it is too late to change their max_length.        
        Not that this limitation is only for the *values*, not for the names 
        or texts of choices.
        
        """
        from lino.utils import dblogger as logger
        #~ raise Exception("20130302 setup_choicelists()")
        #~ logger.info("20130302 setup_choicelists()")
        from django.utils.translation import ugettext_lazy as _
        from lino import dd
        dd.UserProfiles.reset()
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"), name='anonymous', level=None,
            #~ readonly=True,
            authenticated=False)
        add('100', _("User"), name='user', level='user')
        add('900', _("Administrator"), name='admin', level='admin')
        
        
    def add_user_field(self,name,fld):
        if self.user_model:
            from lino import dd
            #~ User = dd.resolve_model(self.user_model)            
            dd.inject_field(self.user_model,name,fld)
            #~ if profile:
                #~ self.user_profile_fields.append(name)


    def get_generic_related(self,obj):
        """
        Yield all database objects in database which have a GenericForeignKey 
        that points to the object `obj`.
        """
        from django.contrib.contenttypes.models import ContentType
        for gfk in self.GFK_LIST:
            ct = ContentType.objects.get_for_model(gfk.model)
            kw = dict()
            kw[gfk.fk_field] = obj.pk
            yield gfk, ct.get_all_objects_for_this_type(**kw)
            

    def using(self,ui=None):
        """
        Adds Lino, Jinja, Spinx, dateutil, ...
        """
        import lino
        yield ("Lino",lino.SETUP_INFO['version'],lino.SETUP_INFO['url'])
        
        import jinja2
        version = getattr(jinja2,'__version__','')
        yield ("Jinja",version,"http://jinja.pocoo.org/")
        
        import sphinx
        version = getattr(sphinx,'__version__','')
        yield ("Sphinx",version,"http://sphinx-doc.org/")
        
        import dateutil
        version = getattr(dateutil,'__version__','')
        yield ("python-dateutil",version,"http://labix.org/python-dateutil")
        
        #~ try:
            #~ import Cheetah
            #~ version = Cheetah.Version 
            #~ yield ("Cheetah",version ,"http://cheetahtemplate.org/")
        #~ except ImportError:
            #~ pass

        try:
            from odf import opendocument
            version = opendocument.__version__
        except ImportError:
            version = self.not_found_msg
        yield ("OdfPy",version ,"http://pypi.python.org/pypi/odfpy")

        try:
            import docutils
            version = docutils.__version__
        except ImportError:
            version = self.not_found_msg
        yield ("docutils",version ,"http://docutils.sourceforge.net/")

        try:
            import suds
            version = suds.__version__
        except ImportError:
            version = self.not_found_msg
        yield ("suds",version ,"https://fedorahosted.org/suds/")

        import yaml
        version = getattr(yaml,'__version__','')
        yield ("PyYaml",version,"http://pyyaml.org/")
        
        if False:
            try:
                import pyratemp
                version = getattr(pyratemp,'__version__','')
            except ImportError:
                version = self.not_found_msg
            yield ("pyratemp",version,"http://www.simple-is-better.org/template/pyratemp.html")
        
        if False:
            try:
                import ho.pisa as pisa
                version = getattr(pisa,'__version__','')
                yield ("xhtml2pdf",version,"http://www.xhtml2pdf.com")
            except ImportError:
                pass

            try:
                import reportlab
                version = reportlab.Version
            except ImportError:
                version = self.not_found_msg
            yield ("ReportLab",version,"http://www.reportlab.org/rl_toolkit.html")
                   
        try:
            #~ import appy
            from appy import version
            version = version.verbose
        except ImportError:
            version = self.not_found_msg
        yield ("Appy",version ,"http://appyframework.org/pod.html")
        
        for u in super(Site,self).using(ui): yield u

    def get_db_overview_rst(self):
        """
        Returns a reStructredText-formatted "database overview" report.
        Used by the :mod:`diag <lino.management.commands.diag>` command 
        and in test cases.
        """
        from atelier import rstgen
        from lino.core.dbutils import obj2str, full_model_name, sorted_models_list, app_labels
        
        #~ writeln("Lino %s" % lino.__version__)
        #~ yield (settings.SITE.verbose_name, settings.SITE.version)
        #~ writeln(settings.SITE.title)
        models_list = sorted_models_list()

        apps = app_labels()
        s = "%d applications: %s." % (len(apps), ", ".join(apps))
        s += "\n%d models:\n" % len(models_list)
        i = 0
        headers = [
            #~ "No.",
            "Name",
            #~ "Class",
            #~ "M",
            "#fields",
            "#rows",
            #~ ,"first","last"
            ]
        rows = []
        for model in models_list:
          if model._meta.managed:
            i += 1
            cells = []
            #~ cells.append(str(i))
            cells.append(full_model_name(model))
            #~ cells.append(str(model))
            #~ if model._meta.managed:
                #~ cells.append('X')
            #~ else:
                #~ cells.append('')
            cells.append(str(len(model._meta.fields)))
            #~ qs = model.objects.all()
            qs = model.objects.order_by('pk')
            n = qs.count()
            cells.append(str(n))
            #~ if n:
                #~ cells.append(obj2str(qs[0]))
                #~ cells.append(obj2str(qs[n-1]))
            #~ else:
                #~ cells.append('')
                #~ cells.append('')
                
            rows.append(cells)
        s += rstgen.table(headers,rows)
        return s
        
        
#~ class Site(BaseSite):
  
    #~ def __init__(self,*args,**kwargs):
        #~ super(Site,self).__init__(*args)
        #~ self.run_djangosite_local(**kwargs)