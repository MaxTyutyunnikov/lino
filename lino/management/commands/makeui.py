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
from optparse import make_option 
import codecs

#~ from Cheetah.Template import Template as CheetahTemplate

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
from lino import reports
from lino.core.coretools import app_labels
from lino.utils import confirm
from lino.utils.config import find_config_file
from lino.utils import rstgen 
from lino.utils import babel
from lino.utils.menus import Menu, MenuItem
from lino.utils.jsgen import py2js

class Command(BaseCommand):
    help = """Writes files (.js, .html, .css) for this Site.
    """
    
    args = "output_dir"
    
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', 
            dest='interactive', default=True,
            help='Do not prompt for input of any kind.'),
        make_option('--overwrite', action='store_true', 
            dest='overwrite', default=False,
            help='Overwrite existing files.'),
    ) 
    
    #~ def handle(self, *args, **options):
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("No output_dir specified.")
        
        self.output_dir = os.path.abspath(args[0])
        #~ self.overwrite
        #~ self.output_dir = os.path.abspath(output_dir)
        self.generated_count = 0
        self.options = options
        settings.LINO.setup()
        #~ from lino.ui.qx.urls import ui
        
        logger.info("Running Lino makeui to %s.", self.output_dir)
        self.generate('Application',application_lines(self))
        for rpt in reports.master_reports + reports.slave_reports + reports.generic_slaves.values():
            #~ rh = rpt.get_handle(ui) 
            #~ js += "Ext.namespace('Lino.%s')\n" % rpt
            #~ f.write("Ext.namespace('Lino.%s')\n" % rpt)
            for a in rpt.get_actions():
                if isinstance(a,reports.GridEdit):
                    self.generate(str(a),action_lines(self,a))
        
        logger.info("Generated %s files",self.generated_count)

    def generate(self,fn,lines):
        fn = fn.replace('.',os.path.sep)
        fn += '.js'
        fn = os.path.join(self.output_dir,fn)
        #~ os.makedirs(os.path.dirname(fn))
        fd = codecs.open(fn,'w',encoding='UTF-8')
        for ln in lines:
            fd.write(ln + "\n")
        fd.close()
        self.generated_count += 1
        

        
def item2js(mi):
  if mi.href:
      return """window.location.href = '%s';""" % mi.href
  return "this.showWindow(new lino.%s(this));" % mi.action # CountriesCitiesTable

def action_lines(self,action):
    yield "/* generated by Lino makeui */"
    yield "#asset(lino/*)"
    yield """qx.Class.define("lino.%s",{""" % action
    yield """\
  extend : lino.TableWindow,
  members : {
    content_type : 9,
    before_row_edit : function(record){}, 
    createTable : function() {
      var tm = new lino.RemoteTableModel(this,'/api/countries/Cities');
      tm.setColumns(
        ["Land",'Name','PLZ','ID'],
        [1,2,3,4]
        //~ ["country",'name','zip_code','id']
      ); // columnNameArr, columnIdArr
      tm.setColumnSortable(0,true);
      tm.setColumnEditable(0,true);
      // todo:
      // filter ? 
      // width ?
      // renderer
      // editor
      // hidden
      // lino.CountriesCitiesInsert
      
      //~ var custom = {
        //~ tableColumnModel : function(obj) { 
          //~ var cm = new qx.ui.table.columnmodel.Basic(obj);
          //~ return cm;
        //~ }
      //~ };      
      //~ var table = new qx.ui.table.Table(tm,custom);
      var table = new qx.ui.table.Table(tm);
      var cm = table.getTableColumnModel();
      cm.setDataCellRenderer(0,new lino.ForeignKeyCellRenderer(0));
      return table;
    },
    setupToolbar: function(bar)
    {
      var btn = new qx.ui.toolbar.Button('Detail');
      btn.addListener('execute',function(){
        //~ this.showWindow(lino.CountriesCitiesDetail);
        alert("TODO : how to referencethe app? want to open new window...");
      }, this);
      bar.add(btn);
    //~ "ls_bbar_actions": [ 
      //~ { "text": "Detail", "panel_btn_handler": Lino.show_detail_handler }, 
      //~ { "text": "Einf\u00fcgen", "must_save": true, "panel_btn_handler": function(panel){Lino.show_insert(panel)} }, 
      //~ { "text": "L\u00f6schen", "panel_btn_handler": Lino.delete_selected } 
    //~ ], 

    }
  }
"""
    
    yield """});"""
  
def application_lines(self):
    yield "/* generated by Lino makeui */"
    yield "#asset(lino/*)"
    yield """qx.Class.define("lino.Application","""
    yield """\
{
  extend : qx.application.Standalone,
  members :
  {
    main : function()
    {
      this.base(arguments);
      if (qx.core.Variant.isSet("qx.debug", "on"))
      {
        qx.log.appender.Native;
        qx.log.appender.Console;
      }

      /*
      -------------------------------------------------------------------------
        Below is your actual application code...
      -------------------------------------------------------------------------
      */
      this.setupMainMenu();
    },
    showWindow : function(win) {
      //~ console.log('showWindow',cls);
      //~ var win = new cls(this);
      //~ win.__app = this;
      win.open();
      this.getRoot().add(win, {left: 50, top: 10});
    },
    
    setupMainMenu : function() {
      var toolBar = new qx.ui.toolbar.ToolBar();
      this.getRoot().add(toolBar, {
        left: 0,
        top: 0,
        right: 0
      });
"""     
    for m in settings.LINO._menu.items:
        if isinstance(m,Menu):
            yield """\
      var mb = new qx.ui.toolbar.MenuButton(%s);  toolBar.add(mb);""" % py2js(m.label)
            yield """\
      var m = new qx.ui.menu.Menu(); mb.setMenu(m);"""
            for mi in m.items:
                yield """\
      var b = new qx.ui.menu.Button(%s);  m.add(b);""" % py2js(mi.label)
                yield """\
      b.addListener('execute',function(){%s},this);""" % (item2js(mi))
      
    yield """\
    }
  }
});
"""

