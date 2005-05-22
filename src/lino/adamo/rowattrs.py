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

#import types
#from copy import copy

from lino.adamo import datatypes
from lino.misc.compat import *
from lino.misc.etc import issequence
from lino.adamo.exceptions import DataVeto, StartupDelay, NoSuchField
from lino.misc.descr import Describable, setdefaults


class RowAttribute(Describable):
    def __init__(self,owner, name,
                 label=None,doc=None):
        Describable.__init__(self,None,name,label,doc)
        self._owner = owner
        self._isMandatory = False
        self._onValidate = []
        
    def child(self,*args,**kw):
        return self.__class__(self,owner,*args,**kw)
    
    def validate(self,row,value):
        if value is None:
            if self._isMandatory:
                raise DataVeto("may not be empty")
            else:
                return
        for v in self._onValidate:
            v(row,value)
    
    def afterSetAttr(self,row):
        pass
        """called after setting this value for this attribute in this
        row. Automatically replaced by after_xxx table method.
        Override this to modify other attributes who depend on this
        one.    """

    def format(self,v):
        return str(v)
        
    def parse(self,s):
        return s
        
    def onOwnerInit1(self,owner,name):
        pass
        
    def onTableInit1(self,owner,name):
        pass
    
    def onTableInit2(self,owner,schema):
        pass
        #self.owner = table
        
    def onTableInit3(self,owner,schema):
        self._onValidate = tuple(self._onValidate)

##     def onAreaInit(self,area):
##         pass
    
    #def setSticky(self):
    #    self.sticky = True

    def setMandatory(self):
        self._isMandatory = True

    def onAppend(self,row):
        pass

##     def validate(self,row,value):
##         return value

    def checkIntegrity(self,row):
        pass

    def getAttrName(self):
        return self.name
    
##  def __str__(self):
##      return self.name

    def __repr__(self):
        return "<%s %s.%s>" % (self.__class__.__name__,
                                      self._owner.getTableName(),
                                      self.name)

    def getDefaultValue(self,row):
        return None

    def setCellValue(self,row,value):
        # does not setDirty() !
        self.validate(row,value)
        row._values[self.name] = value
        
##     def getCellValue(self,row,col):
##         # overridden by BabelField and Detail
##         return row.getFieldValue(self.name)

    def setValueFromString(self,row,s):
        # does not setDirty() !
        if len(s) == 0:
            self.setCellValue(row,v)
        else:
            v=self.parse(s)
            self.setCellValue(row,v)
    
    
    def getFltAtoms(self,colAtoms,context):
        return colAtoms

##     def getTestEqual(self,ds, colAtoms,value):
##         raise NotImplementedError

    def canWrite(self,row):
        # note : row may be None. 
        return True
    
##     def row2atoms(self,row):
##         """fill into atomicRow the atomic data necessary to represent
##         this column"""
##         value = row._values.get(self.name)
##         return self.value2atoms(value, row.getDatabase())

        
##     def value2atoms(self,value,ctx):
##         print self,value
##         raise NotImplementedError
    
    
    def atoms2row(self,atomicRow,colAtoms,row):
        atomicValues = [atomicRow[atom.index] for atom in colAtoms]
        row._values[self.name] = self.atoms2value(atomicValues,
                                                  row.getSession())

    #
    # change atoms2value(self,atomicRow,colAtoms,context)
    # to atoms2value(self,atomicValues,context)
    #
    def atoms2value(self,atomicValues,session):
        raise NotImplementedError

        
##  def atoms2dict(self,atomicRow,valueDict,colAtoms,area):
##      # overridden by Detail to do nothing
##      valueDict[self.name] = self.atoms2value(atomicRow,colAtoms,area)
        
    
    def getNeededAtoms(self,ctx):
        return ()

##  def getValueFromRow(self,row):
##      try:
##          return row._values[self.name]
##      except KeyError,e:
##          row._readFromStore()
##          return row._values[self.name]
##      #return row._values[name]

        

class Field(RowAttribute):
    """
    
    A Field is a component which represents an atomic piece of data.
    A field is a storable atomic value of a certain type.
    
    """
    def __init__(self,owner,name,type,**kw):
        RowAttribute.__init__(self,owner,name,**kw)
        self.type = type
        #self.visibility = 0
        #self.format = format

    def setType(self,type):
        self.type = type

    def getType(self):
        return self.type

    def format(self,v):
        return self.type.format(v)
        
    def validate(self,row,value):
        if value is not None:
            self.type.validate(value)
        RowAttribute.validate(self,row,value)
        
    def parse(self,s):
        return self.type.parse(s)
        
##  def asFormCell(self,renderer,value,size=None):
##      renderer.renderValue(value,self.type,size)
        
    def getNeededAtoms(self,ctx):
        return ((self.name, self.type),)
        #return (query.provideAtom(self.name, self.type),)

##     def value2atoms(self,value,ctx):
##         return (value,)


##     def getTestEqual(self,ds,colAtoms,value):
##         assert len(colAtoms) == 1
##         a = colAtoms[0]
##         return ds._connection.testEqual(a.name,a.type,value)

        
    def atoms2value(self,atomicValues,session):
        assert len(atomicValues) == 1
        return atomicValues[0]
        
    
    def getMinWidth(self):
        return self.type.minWidth
    def getMaxWidth(self):
        return self.type.maxWidth



class BabelField(Field):

    def getNeededAtoms(self,ctx):
        assert ctx is not None,\
                 "tried to use BabelField for primary key?"
        l = []
        for lang in ctx.getBabelLangs(): 
            l.append( (self.name+"_"+lang.id, self.type) )
        return l


##     def getSupportedLangs(self):
##         return self._owner._schema.getSupportedLangs()

    
    def setCellValue(self,row,value):
        langs = row.getSession().getBabelLangs()
        values = row.getFieldValue(self.name)
        if values is None:
            values = [None] * len(row.getDatabase().getBabelLangs())
            row._values[self.name] = values
        if len(langs) > 1:
            assert issequence(value), \
                   "%s is not a sequence" % repr(value)
            assert len(value) == len(langs), \
                   "%s expects %d values but got %s" % \
                   (self.name, len(langs), repr(value))
            i = 0
            for lang in langs:
                if lang.index != -1:
                    values[lang.index] = value[i]
                i += 1
        else:
            assert not issequence(value)
            index = langs[0].index
            if index != -1:
                values[index] = value
            
        
##     def getCellValue(self,row,col):
##         langs = row.getSession().getBabelLangs()
##         dblangs = row.getDatabase().getBabelLangs()
##         #if row.getTableName() == "Nations":
##         #    print __name__, langs, dblangs
##         # 35.py dblangs = row._ds._session.getBabelLangs()
##         values = row.getFieldValue(self.name)
##         #values = Field.getCellValue(self,row)
##         if values is None:
##             values = [None] * len(dblangs)
##         else:
##             assert issequence(values), \
##                    "%s is not a sequence" % repr(values)
##             assert len(values) == len(dblangs), \
##                    "Expected %d values but got %s" % \
##                    (len(dblangs), repr(values))
        
##         if len(langs) > 1:
##             l = []
##             for lang in langs:
##                 if lang.index != -1:
##                     l.append(values[lang.index])
##                 else:
##                     l.append(None)
##             return l
##         else:
##             index = langs[0].index
##             assert not index == -1
##             #print __name__, values[index], langs
##             return values[index]
        
##     def getTestEqual(self,ds, colAtoms,value):
##         langs = ds.getSession().getBabelLangs()
##         lang = langs[0] # ignore secondary languages
##         a = colAtoms[lang.index]
##         return ds._connection.testEqual(a.name,a.type,value)

##     def value2atoms(self,value,ctx):
##         # value is a sequence with all langs of db
##         dblangs = ctx.getBabelLangs()
##         rv = [None] * len(dblangs)
##         if value is None:
##             return rv
##         assert issequence(value), "%s is not a sequence" % repr(value)
##         assert len(value) == len(dblangs), \
##                "Expected %d values but got %s" % \
##                (len(dblangs), repr(value))
##         i = 0
##         for lang in dblangs:
##             rv[lang.index] = value[i]
##             i += 1

##         return rv
            
    def atoms2row(self,atomicRow,colAtoms,row):
        langs = row.getSession().getBabelLangs()
        dblangs = row.getDatabase().getBabelLangs()
        assert len(dblangs) == len(colAtoms)
        # 35.py dblangs = row._ds._session.getBabelLangs()
        values = row.getFieldValue(self.name)
        if values is None:
            values = [None] * len(dblangs)
            row._values[self.name] = values
        for lang in dblangs:
            #assert lang.index != -1
            #if lang.index != -1:
            value = atomicRow[colAtoms[lang.index].index]
            values[lang.index] = value
        #row._values[self.name] = l
    
    
    def getFltAtoms(self,colAtoms,context):
        l = []
        langs = context.getBabelLangs()
        for lang in langs:
            if lang.index != -1:
                l.append(colAtoms[lang.index])
        return l

    

    
## class Match(Field):
##     def __init__(self,origin,**kw):
##         assert isinstance(origin,Field)
##         self._origin = origin
##         Field.__init__(self,origin.type,**kw)
##         self.getLabel = origin.getLabel

##     def __getattr__(self,name):
##         return getattr(self._origin,name)
    

## class Button(RowAttribute,Action):
##  def __init__(self,meth,label=None,*args,**kw):
##      RowAttribute.__init__(self,label=label,doc=meth.__doc__)
##      Action.__init__(self,meth,*args,**kw)
        
##  def getCellValue(self,row):
##      return self._func(row)
    


class Pointer(RowAttribute):
    """
    
    A Pointer links from this to another table.
    
    """
    def __init__(self, owner, name, toClass,
                 detailName=None,
                 **kw):
        RowAttribute.__init__(self,owner,name,**kw)
        self._toClass = toClass
        
        #self.sticky = True # joins are sticky by default
        
        self.detailName = detailName
        #self.dtlColumnNames = None
        self.dtlKeywords = {}
        self._neededAtoms = None

    def setDetail(self,name,columnNames=None,**kw):
        self.detailName = name
        #self.dtlColumnNames = columnNames
        if columnNames is not None:
            kw['columnNames'] = columnNames
        self.dtlKeywords = kw
        
    def onTableInit1(self,owner,name):
        if self.detailName is None:
            self.setDetail(
                owner.getTableName().lower()+'_by_'+self.name)
            
    def onTableInit2(self,owner,schema):
        self._toTables = schema.findImplementingTables(self._toClass)
        assert len(self._toTables) > 0, \
                 "%s.%s : found no tables implementing %s" % \
                 (owner.getName(),
                  str(self),
                  str(self._toClass))
        #if len(self._toTables) > 1:
        #   print "rowattrs.py:", repr(self)

    def onTableInit3(self,owner,schema):
        RowAttribute.onTableInit3(self,owner,schema)
        for toTable in self._toTables:
            toTable.addDetail( self.detailName,
                               self,
                               #self.dtlColumnNames,
                               **self.dtlKeywords)
            
##     def getTestEqual(self,ds,colAtoms,value):
##         av = self.value2atoms(value,ds.getSession())
##         i = 0
##         l = []
##         for (n,t) in self.getNeededAtoms(ds.getSession()):
##             l.append(ds._connection.testEqual(n,t,av[i]))
##             i += 1
##         return " AND ".join(l)


            
    def getNeededAtoms(self,ctx):
        
        """ The toTable is possibly not yet enough initialized to tell
        me her primary atoms. In this case getPrimaryAtoms() will raise
        StartupDelay which will be caught in Schema.startup() """
        
        if self._neededAtoms is None:
            neededAtoms = []
            if len(self._toTables) > 1:
                #neededAtoms.append((self.name+"_tableId",AREATYPE))
                #i = 0
                for toTable in self._toTables:
                    for (name,type) in toTable.getPrimaryAtoms():
                        neededAtoms.append(
                            (self.name + toTable.getTableName()
                             + "_" + name,
                             type) )
                    #i += 1
            else:
                for (name,type) in self._toTables[0].getPrimaryAtoms():
                    neededAtoms.append( (self.name + "_" + name,
                                         type) )

            self._neededAtoms = tuple(neededAtoms)
        return self._neededAtoms

    def checkIntegrity(self,row):
        raise "won't work: getCellValue() now needs col"
        pointedRow = self.getCellValue(row)
        if pointedRow is None:
            return # ok

        if pointedRow._query.peek(*pointedRow.getRowId()) is None:
            return "%s points to non-existing row %s" % (
                self.name,str(pointedRow.getRowId()))



    def getMinWidth(self):
        # TODO: 
        return 10
    def getMaxWidth(self):
        # TODO: 
        return 50
        #w = 0
        #for pk in self._toTable.getPrimaryKey():
        #   w += pk.getPreferredWidth()
        #return w

        
##     def _findToTable(self,tableId):
##         for toTable in self._toTables:
##             if toTable.getTableId() == tableId:
##                 return toTable
##         raise "not found %d" % tableId

    
##     def value2atoms(self,value,ctx):
##         pointedRow = value
##         #print repr(pointedRow)
##         if pointedRow is None:
##             return [None] * len(self._neededAtoms)
        
##         if len(self._toTables) == 1:
##             return pointedRow.getRowId()
##         else:
##             rv = [None] * len(self._neededAtoms)
##             i = 0
##             tableId = pointedRow._query.getLeadTable().getTableId()
##             rid = pointedRow.getRowId()
##             for toTable in self._toTables:
##                 if toTable.getTableId() == tableId:
##                     ai = 0
##                     for a in toTable.getPrimaryAtoms():
##                         rv[i] = rid[ai]
##                         i+=1
##                         ai+=1
##                     return rv
##                 else:
##                     i += len(toTable.getPrimaryAtoms())


    def atoms2value(self,atomicValues,sess):
        #ctx = row._ds._context
        if len(self._toTables) > 1:
            toTable = self._findUsedToTable(atomicValues)
            if toTable is None:
                return None
            atomicValues = self._reduceAtoms(toTable.getTableId(),
                                                        atomicValues)
            #toArea = getattr(sess.tables,toTable.getTableName())
            toArea = sess.query(toTable.__class__)
        else:
            #toTable = self._toTables[0]
            #areaName = toTable.getTableName()
            #toArea = getattr(sess.tables,areaName)
            toArea = sess.query(self._toTables[0].__class__)
        
        if None in atomicValues:
            return None
        try:
            return toArea.getInstance(atomicValues,False)
        except DataVeto,e:
            return str(e)
    
    
    def _findUsedToTable(self,atomicValues):
        i = 0
        for toTable in self._toTables:
            for justLoop in toTable.getPrimaryAtoms():
                #if atomicRow[colAtoms[i].index] is not None:
                if atomicValues[i] is not None:
                    return toTable
                i += 1
        return None
    
    def _reduceAtoms(self,tableId,atomicValues):
        """
            
        We want only the atoms for this tableId.  Example: if there
        are 3 possible tables (tableId may be 0,1 or 2) and pklen
        is 2, then there are 2*3 = 6 atoms.
            
              tableId 0 -> I want atoms 0 and 1  -> [0:2]
              tableId 1 -> I want atoms 2 and 3  -> [2:4]
              tableId 2 -> I want atoms 4 and 5  -> [4:7]
              
        """
            
        # the first atom is the tableId
        for toTable in self._toTables:
            pklen = len(toTable.getPrimaryAtoms())
            if toTable.getTableId() == tableId:
                return atomicValues[:pklen]
            else:
                atomicValues = atomicValues[pklen:]
        raise "invalid tableId %d" % tableId
    
    def getType(self):
        return datatypes.STRING

    def getTargetSource(self,row): 
        return row.getSession().query(self._toClass)
    
        
class Detail(RowAttribute):
    def __init__(self,owner,
                 name,pointer,label=None,doc=None,**kw):
        
        self.pointer = pointer
        RowAttribute.__init__(self,owner,
                              name,label=label,doc=doc)
        kw[self.pointer.name] = None
        self._queryParams = kw
        
    def format(self,ds):
        return str(len(ds))+" "+ds.getLeadTable().getName()

        
    def validate(self,row,value):
        raise "cannot set value of a detail"
    
    def getMinWidth(self):
        # TODO: 
        return 20
    def getMaxWidth(self):
        # TODO: 
        return 40

##     def onAreaInit(self,area):
##         area.defineQuery(self.name,self._queryParams)
        

##     def row2atoms(self,row):
##         return ()
    
    def atoms2row(self,atomicRow,colAtoms,row):
        row._values[self.name] = None
    
    def atoms2value(self,atomicRow,colAtoms,sess):
        assert len(colAtoms) == 0
        raise "cannot"
        
    def canWrite(self,row):
        # note : row may be None. 
        return False


##     def getCellValue(self,row,col):
##         q=col.detailQuery.child(masters=(row,))
##         #print "Detail.getCellValue():", q._search
##         return q
##         return col.detailQuery.child(samples={
##             self.pointer.name:row})
##         ds=row.getFieldValue(self.name)
##         if ds is None:
##             #ds=self.getDefaultValue()
##             kw = dict(self._queryParams)
##             kw[self.pointer.name] = row
##             ds=row.getSession().query(
##                 self.pointer._owner.__class__, **kw)
##             row._values[self.name] = ds
##         return ds
        
    def getType(self):
        return datatypes.STRING

class Vurt(Field):
    """
    
    A Vurt (virtual field) is a method 
    
    """
    def __init__(self,func,type,**kw):
        Field.__init__(self,type,**kw)
        self._func = func
        #self.type = type

    def format(self,v):
        return self.type.format(v)
        
    def parse(self,s):
        raise "not allowed"
        

##     def getPreferredWidth(self):
##         return self.type.width


    def setCellValue(self,row,value):
        raise "not allowed"
        
    def getCellValue(self,row,col):
        return self._func(row)
    
    def atoms2row(self,atomicRow,colAtoms,row):
        pass

    
    
