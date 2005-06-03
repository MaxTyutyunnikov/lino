## Copyright 2003-2005 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
import types

from lino.misc.descr import Describable
from lino.misc.attrdict import AttrDict
#from lino.ui import console
from lino.console import syscon
from lino.console.application import Application

#from lino.adamo.forms import Form
from lino.adamo.table import Table, LinkTable, SchemaComponent
from lino.adamo.exceptions import StartupDelay
from lino.adamo.query import Query
from lino.adamo import center

class TooLate(Exception):
    pass

class SchemaPlugin(SchemaComponent,Describable):
    def __init__(self,isActive=True,*args,**kw):
        SchemaComponent.__init__(self)
        Describable.__init__(self,None,*args,**kw)
        self._isActive = isActive

    def isActive(self):
        return self._isActive
        
    def defineTables(self,schema):
        pass
    def defineMenus(self,schema,context,win):
        pass
##     def populate(self,sess):
##         pass


class Schema(Application):
##     usage="usage: %prog [options] DBFILE"
##     description="""\
## where DBFILE is the name of the sqlite database file"""

    HK_CHAR = '&'
    defaultLangs = ('en',)
    tables=[]

    #toolkits="wx console"
    
    #_sessionFactory=DbSession
    
    def __init__(self,#filename=None,
                 checkIntegrityOnStartup=False,
                 tempDir=".",
                 #populate=False,
                 langs=None,**kw):
        Application.__init__(self,**kw)
        #self.schema = Schema()
        #self.filename = filename
        self.tempDir=tempDir
        self.checkIntegrityOnStartup = checkIntegrityOnStartup
        #self.populate=populate
        #self.sess = None
##     def __init__(self,name=None,label=None,doc=None,
##                  langs=None,
##                  **kw):
##         Describable.__init__(self,None,name,label,doc)
        self._initDone= False
        self._datasourceRenderer= None
        self._contextRenderer= None
        if langs is None:
            langs="en de fr nl et"
        self._possibleLangs = tuple(langs.split())
        
        #self._databases = []
        self._plugins = []
        self._tables = []
        
        self.plugins = AttrDict()
        #self.forms = AttrDict()
        #self.options = AttrDict(d=kw)
        
        #center.addSchema(self)

        """ Note: for plugins and tables it is important to keep also a
        sequential list.  """
        
##     def setupOptionParser(self,parser):
##         Application.setupOptionParser(self,parser)
##         #def call_set(option, opt_str, value, parser,**kw):
##         #    self.set(**kw)

##         parser.add_option("-c",
##                           "--check",
##                           help="perform integrity check on startup",
##                           action="store_true",
##                           dest="checkIntegrityOnStartup",
##                           default=False,
##                           )
        
        
##     def applyOptions(self,options,args):
##         Application.applyOptions(self,options,args)
##         #self.checkIntegrityOnStartup = options.checkIntegrityOnStartup
##         if len(args) == 1:
##             self.filename = args[0]
##         else:
##             self.filename=os.path.join(self.tempDir,
##                                        self.name+".db")
        
    def addTable(self,tableClass,**kw):
        #print tableClass
        table = tableClass(None,**kw)
        assert isinstance(table,Table),\
                 repr(table)+" is not a Table"
        assert not self._initDone,\
                 "Too late to declare new tables in " + repr(self)
        table.registerInSchema(self,len(self._tables))
        self._tables.append(table)
        return table
        #name = table.getTableName()
        #self.tables.define(name,table)
        
    def addPlugin(self,plugin):
        assert isinstance(plugin,SchemaPlugin),\
                 repr(plugin)+" is not a SchemaPlugin"
        assert not self._initDone,\
                 "Too late to declare new plugins in " + repr(self)
        plugin.registerInSchema(self,len(self._plugins))
        self._plugins.append(plugin)
        name = plugin.getName()
        self.plugins.define(name,plugin)



##  def addForm(self,form):
##      assert isinstance(form,FormTemplate), \
##               repr(form)+" is not a FormTemplate"
##      assert not self._startupDone,\
##               "Too late to declare new forms in " + repr(self)
##      form.registerInSchema(self,len(self.forms))
##      name = form.getFormName()
##      self.forms.define(name,form)
##      #assert not self._forms.has_key(name)
##      #self._forms[name] = form
        

    def initialize(self):
        
        """ initialize will be called exactly once, after having
        declared all tables of the database.  """
    
        if self._initDone:
            return

        syscon.debug(
            "Initializing %d tables..." % len(self._tables))

        # loop 1
        for table in self._tables:
            table.init1()
        
        # loop 2
        todo = list(self._tables)
        while len(todo):
            tryagain = []
            somesuccess = False
            for table in todo:
                # print "setupTable", table.getName()
                try:
                    table.init2()
                    somesuccess = True
                except StartupDelay, e:
                    syscon.debug("StartupDelay:"+repr(e))
                    tryagain.append(table)
            if not somesuccess:
                "not supported: primary key with pointer to self"
                raise "Schema.initialize() failed"
            todo = tryagain

        # loop 2bis
        #for table in self._tables:
        #   table.defineQuery(None)

        # loop 3 
        for table in self._tables:
            table.init3()

        # loop 4
        for table in self._tables:
            table.init4()
            
        self.onInitialize()
        
        self._initDone = True
        syscon.debug("Schema initialized")

    def onInitialize(self):
        pass

    def setLayout(self,layoutModule):
        # initialize layouts...
        assert self._initDone 
        
        lf = LayoutFactory(layoutModule)
        for table in self._tables:
            wcl = lf.get_wcl(table.Instance)
            assert wcl is not None
            table._rowRenderer = wcl


        self._datasourceRenderer = lf.get_wcl(Query)
        self._contextRenderer = lf.get_wcl(Database)

        assert self._datasourceRenderer is not None
        assert self._contextRenderer is not None
        

    
    def findImplementingTables(self,toClass):
        l = []
        for t in self._tables:
            if isinstance(t,toClass):
                l.append(t)
                #break
        return l
        

    def getTableList(self,tableClasses=None):
        
        """returns an ordered list of all (or optinally some) table
        instances in this Schema.  If tableClasses is specified, it
        must be a sequence of Table classes for which we want the
        instance.  The list is sorted by table definition order.  It
        is forbidden to modify this list!  """
        
        #self.initialize()
        assert self._initDone, \
               "getTableList() before initialize()"
        if tableClasses is None:
            return self._tables
        return [t for t in self._tables
                if t.__class__ in tableClasses]
        
    
    def __repr__(self):
        return str(self.__class__)
    
    def __str__(self):
        return str(self.__class__)


    def database(self,*args,**kw):
        return center.database(self,*args,**kw)
    
##     def addDatabase(self,name=None,**kw): #langs=None,label=None):
##     #def openDatabase(self,name=None,**kw):
##         if self._startupDone:
##             raise TooLate("Cannot addDatabase() after startup()")
##         db = Database(self,name=name,**kw)
##         #langs=langs,name=name,label=label)
##         self._databases.append(db)
##         return db

    def setupSchema(self):
        #print "%s.setupSchema()" % self.__class__
        for t in self.tables:
            self.addTable(t)
        for p in self._plugins:
            p.defineTables(self)
    
    def quickStartup(self,
                     #toolkit=None,
                     langs=None,
                     filename=None,
                     **kw):
        #print "%s.quickStartup()" % self.__class__
        self.setupSchema()
        #job = ui.job("quickStartup()")
        syscon.debug("Initialize Schema")
        self.initialize()
        db = self.database(langs=langs)
        syscon.debug("Connect")
        conn = center.connection(filename=filename)
        db.connect(conn)
        return db.startup(**kw) #syscon.getSystemConsole())
        #return DbSession(db,syscon.getSystemConsole())
        #assert len(self._sessions) == 1
        #return self._sessions[0]
    
        #sess.setDefaultLanguage()
        #return self._sessions

##     def openSession(self,db):
##         sess = DbSession(db,toolkit)
##         self._sessions.append(sess)
##         self.onOpenSession(sess)
##         return sess

        
##     def start_gui(self,toolkit):
##         for db in self._databases:
##             sess=DbSession(db,toolkit)
##             self.run(sess)
##             self.addSession(sess)
    
    
    def run(self,sess):
        self.showMainForm(sess)
        
    def showMainForm(self,sess):
        pass
        
##     def shutdown(self):
##         syscon.debug("Schema.shutdown()")
##         for db in self._databases:
##             db.close()
##         self._databases = []
        
##     def init(self,ui): 
##         # called from Toolkit.main()
##         sess = self.startup(ui)
##         self.showMainForm(ui)

    

##  def onStartUI(self,sess):
##      # overridden by sprl.Schema
##      return True

    def onLogin(self,sess):
        return True

## class DatabaseSchema(Window,PropertySet):

##  defaults = {
##      "startupDone" : False,
##      "_tables" : [],
##      "langs" : ("en",),
##      #"areaType"  : AREA
##      }

##  HK_CHAR = '&'

##  def __init__(self,**kw):
##      #Window.__init__(self,None,)
##      PropertySet.__init__(self,**kw)
## ##       self.startupDone = False
## ##       self._tables = []
## ##       self.langs = ("en",)
## ##       self.areaType = AREA
##      #self.label=label
##      #self.options = kw
## ##           self.__dict__['_renderer'] = None
##      # self.__dict__['_mainWindow'] = None

## ##       def __setattr__(self,name,table):
## ##           #if self.conn is None:
## ##           #    raise "must connect before declaring tables"
## ##           assert isinstance(table,Table)
## ##           if self.startupDone:
## ##               raise "too late to declare new tables"
## ##           self.tables[name] = table
## ##           table.declare(self,name)
## ##           # globals()[name] = table

## ##   def __str__(self):
## ##       return self.label

##      #self.babelNone = tuple([None] * len(self.langs))
    
##  def __repr__(self):
##      return str(self.__class__)
    
##  def __str__(self):
##      return str(self.__class__)
    
##  def defineSystemTables(self,ui):
##      self.addTable("LANG",
##                        Language,
##                        label="Languages")
        
    
##  def defineTables(self,ui):
##      raise NotImplementedError
    
##  def defineMenus(self,ui):
##      raise NotImplementedError
    
##  def addTable(self,name,rowClass,label=None):
##      # assert isinstance(table,Table)
##      if self.startupDone:
##          raise "too late to declare new tables"
##      # table =
##      self._tables.append(
##          Table(self, len(self._tables), name,rowClass,label))
        
##  def addLinkTable(self,
##                        name,parentClass,childClass,
##                        rowClass=None):
##      if self.startupDone:
##          raise "too late to declare new tables"
##      self._tables.append(
##          LinkTable(self,len(self._tables), name,
##                       parentClass,childClass, rowClass))

##  def startup(self,ui=None):
        
##      """ startup will be called exactly
##      once, after having declared all tables of the database.  """
    
##      assert not self.startupDone, "double startup"

##      if ui is None:
##          from ui import UI
##          ui = UI()
        
##      ui.info("Adamo startup...")

##      ui.info("  Initializing database...")
##      self.defineSystemTables(ui)
##      self.defineTables(ui)

##      ui.info("  Initializing %d tables..." % len(self._tables))

##      # loop 1
##      for table in self._tables:
##          table.init1(self)
        
##      # loop 2
##      todo = list(self._tables)
##      while len(todo):
##          tryagain = []
##          somesuccess = False
##          for table in todo:
##              # print "setupTable", table.getName()
##              try:
##                  table.init2(self)
##                  somesuccess = True
##              except StartupDelay, e:
##                  tryagain.append(table)
##          if not somesuccess:
##              raise "startup failed"
##          todo = tryagain

##      # loop 2bis
##      for table in self._tables:
##          table.defineQuery(None)

##      # loop 3 
##      for table in self._tables:
##          table.init3(self)


##      # self.defineMenus(self,ui)
        
##      #if verbose:
##      #   print "setupTables() done"
            
##      ui.info("Adamo startup okay")

    
##      self.__dict__['startupDone'] = True
    

## ##   def addReport(self,name,rpt):
## ##       self.reports[name] = rpt
    
## ##       def setRenderer(self,r):
## ##           self._renderer = r

## ##       def getRenderer(self):
## ##           return self._renderer

## #    def setupTables(self):
        

##  def getTableList(self):
##      return self._tables

    
    
##  def getTable(self,tableId):
##      try:
##          return self._tables[tableId]
##      except KeyError:
##          raise "%d : no such table in %s" % (tableId, str(self))


##  def findImplementingTables(self,toClass):
##      l = []
##      for t in self._tables:
##          for mixin in t._rowMixins:
##              if issubclass(mixin,toClass):
##                  l.append(t)
##                  break
##              #else:
##              #   print t, "doesn't implement", toClass
##      return l
        

            
## def connect_sqlite():
##     from lino.adamo.dbds.sqlite_dbd import Connection
##     return Connection(filename="tmp.db",
##                       schema=schema,
##                       isTemporary=True)

## def connect_odbc():
##     raise ImportError
##     """
    
##     odbc does not work. to continue getting it work, uncomment the
##     above line and run tests/adamo/4.py to reproduce the following
##     error:
    
##     DatabaseError: CREATE TABLE PARTNERS (
##          id BIGINT,
##          lang_id CHAR(3),
##          org_id BIGINT,
##          person_id BIGINT,
##          name VARCHAR(50),
##          PRIMARY KEY (id)
## )
## ('37000', -3553, '[Microsoft][ODBC dBASE Driver] Syntaxfehler in Felddefinition.
## ', 4612)

##     """
##     from lino.adamo.dbds.odbc_dbd import Connection
##     return Connection(dsn="DBFS")

## def connect_mysql():
##     raise ImportError
##     from lino.adamo.dbds.mysql_dbd import Connection
##     return Connection("linodemo")
    

    



## def quickdb(self,schema, verbose=False,
##              langs=None,
##              label=None,
##              filename="tmp.db",
##              isTemporary=True):
    
##  from lino.adamo.ui import UI
##  ui = UI(verbose=verbose)

##  # start it up
##  schema.startup(ui)

##  # Decide which driver to use 
##  from lino.adamo.dbds.sqlite_dbd import Connection
##  conn = Connection( filename="tmp.db",
##                           schema=schema,
##                           isTemporary=isTemporary)

##  db = Database(ui, conn, schema,
##                    langs=langs,
##                    label=label)

## ##   for f in (connect_odbc, connect_sqlite, connect_mysql):
## ##       try:
## ##           conn = f()
## ##           break
## ##       except ImportError:
## ##           pass

## ##   db = ui.addDatabase('demo',conn,schema,label="Lino Demo Database")

##  ui.addDatabase(db) #'tmp', conn,schema, label=label)
##  return db



class LayoutComponent:
    pass

class LayoutFactory:
    "extracts Layouts from "
    def __init__(self,mod):
        #self._schema = schema
        self._layouts = {}
        for k,v in mod.__dict__.items():
            if type(v) is types.ClassType:
                if issubclass(v,LayoutComponent):
                    try:
                        hcl = v.handledClass
                    except AttributeError:
                        pass
                    else:
                        assert not self._layouts.has_key(hcl),\
                                 repr(v) + ": duplicate class handler for " + repr(hcl)
                        self._layouts[hcl] = v
                        #print k,v.handledClass,v

        for k,v in self._layouts.items():
            print str(k), ":", str(v)
        print len(self._layouts), "class layouts"
        
        # setupSchema()
##      for table in schema._tables:
##          if not table._rowAttrs.has_key("writeParagraph"):
##              wcl = self.get_wcl(table.Row)
##              assert wcl is not None
##              from lino.adamo import Vurt, MEMO
##              table._rowAttrs["writeParagraph"] = Vurt(
##                  wcl.writeParagraph,MEMO)

    def get_bases_widget(self,cl):
        #print "get_bases_widget(%s)" % repr(cl)
        try:
            return self._layouts[cl]
        except KeyError:
            pass #print "no widget for " + repr(cl)

        for base in cl.__bases__:
            try:
                return self._layouts[base]
            except KeyError:
                #print "no widget for " + repr(cl)
                pass
        raise KeyError


    def get_wcl(self,cl):
        #print "get_wcl(%s)" % repr(cl)
        try:
            return self.get_bases_widget(cl)
        except KeyError:
            pass

        for base in cl.__bases__:
            try:
                return self.get_bases_widget(base)
            except KeyError:
                pass
        return None
    
    def get_widget(self,o,*args,**kw):
        #print "get_widget(%s)" % repr(o)
        wcl = self.get_wcl(o.__class__)
        if wcl is None:
            msg = "really no widget for "+repr(o)
            #+" (bases = " + str([repr(b) for b in cl.__bases__])
            raise msg
        #print "--> found widget " + repr(wcl)
        return wcl(o,*args,**kw)

## def get_rowwidget(row):      
##  cl = get_widget(row._ds._table.__class__)
##  return cl(row)
        

class MirrorLoaderApplication(Schema):

    def __init__(self,loadfrom=".",**kw):
        Schema.__init__(self,**kw)
        self.loadfrom = loadfrom
    
    def registerLoaders(self,loaders):
        for l in loaders:
            it = self.findImplementingTables(l.tableClass)
            assert len(it) == 1
            it[0].setMirrorLoader(l)

            
    def setupOptionParser(self,parser):
        Schema.setupOptionParser(self,parser)
        
        parser.add_option("--loadfrom",
                          help="""\
directory containing mirror source files""",
                          action="store",
                          type="string",
                          dest="loadfrom",
                          default=".")
    
##     def applyOptions(self,options,args):
##         Application.applyOptions(self,options,args)
##         self.loadfrom = options.loadfrom
