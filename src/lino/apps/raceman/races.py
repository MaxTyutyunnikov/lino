#coding: latin1

## Copyright 2004-2005 Luc Saffre

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

import datetime

from lino.adamo import *
from lino.schemas.sprl.babel import Languages
from lino.schemas.sprl.addrbook import Persons, SEX

NAME = STRING(width=30)
DOSSARD = STRING(width=4)

class Races(Table):
    def init(self):
        self.addField('id',ROWID) #STRING(width=6))
        self.addField('name1',NAME)
        self.addField('name2',NAME)
        self.addField('date',DATE)
        self.addField('status',STRING(width=1))
        self.addField('tpl',STRING(width=6))
        self.addPointer('type',RaceTypes)
        self.addField('startTime',TIME)

    def setupMenu(self,nav):
        frm = nav.getForm()
        m = frm.addMenu("&Race")
        def f():
            race = nav.getCurrentRow()
            race.showArrivalEntry(frm)
            
        m.addItem(label="&Arrivals",
                  action=f,
                  accel="F6")

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name1

        def showArrivalEntry(self,ui):
            self.lock()
            frm = ui.form(
                label="Arrivals for "+str(self),
                doc="""\
    Ankunftszeiten an der Ziellinie erfassen.
    Beim Startschuss "Start" klicken!
    Jedesmal wenn einer ankommt, ENTER dr�cken.
        """)

            frm.addEntry("dossard",STRING,
                         label="Dossard",
                         value="*",
                         doc="""Hier die Dossardnummer des ankommenden L�ufers eingeben, oder '*' wenn sie sp�ter erfasst werden soll.""")


            def startNow():
                self.startTime = datetime.datetime.now().time()
                frm.setMessage("started at " + str(self.startTime))
                #parent.buttons.arrive.setFocus()
                frm.entries.dossard.setFocus()

            def arriveNow():
                if self.startTime is None:
                    frm.buttons.start.setFocus()
                    raise InvalidRequestError(
                        "cannot arrive before start")
                now = datetime.datetime.now()
                #assert now.date() == self.date,\
                #       "%s != %s" % (repr(now.date()),repr(self.date))
                duration = now - datetime.datetime.combine(
                    now.date(), self.startTime)
                a = self.arrivals.appendRow(
                    dossard=frm.entries.dossard.getValue(),
                    duration=duration,
                    time=now.time())
                frm.setMessage("%s arrived at %s after %s" %(
                    a.dossard,a.time,a.duration))
                frm.entries.dossard.setValue('*')
                frm.entries.dossard.setFocus()
                


            #bbox = frm.addHPanel()
            bbox = frm
            bbox.addButton(name="start",
                          label="&Start",
                          action=startNow)
            bbox.addButton(name="arrive",
                          label="&Arrive",
                          action=arriveNow).setDefault()
            #bbox.addButton("write",
            #               label="&Write",
            #               action=self.writedata)
            bbox.addButton("exit",label="&Exit",action=frm.close)

    ##         fileMenu  = frm.addMenu("&File")
    ##         fileMenu.addButton(frm.buttons.write,accel="Ctrl-S")
    ##         fileMenu.addButton(frm.buttons.exit,accel="Ctrl-Q")

    ##         fileMenu  = frm.addMenu("&Edit")
    ##         fileMenu.addButton(frm.buttons.start)
    ##         fileMenu.addButton(frm.buttons.arrive,accel="Ctrl-A")
            #self.frm = frm
            frm.showModal()
            self.unlock()

        def printRow(self,prn):
            sess = self.getSession()
            q = self.participants.query(
                "person.name cat time dossard",
                orderBy="person.name")
            q.executeReport(prn.report(),
                            label="First report",
                            columnWidths="20 3 8 4")

            q = sess.query(Participants,"time person.name cat dossard",
                           orderBy="time",
                           race=self)
            q.executeReport(prn.report(),
                            label="Another report",
                            columnWidths="8 20 3 4")

            self.ralGroupList(prn,
                              xcKey="club",
                              nGroupSize=3)
            self.ralGroupList(prn, xcKey="club",
                              nGroupSize=5,
                              sex="M")
            self.ralGroupList(prn,
                              xcKey="club",
                              nGroupSize=5,
                              sex="F")

        def ralGroupList(self,prn,
                         xcKey="club",
                         xnValue="place",
                         nGroupSize=3,
                         sex=None,
                         xcName=None,
                         maxGroups=10):
            class Group:
                def __init__(self,id):
                    self.id = id
                    self.values = []
                    self.sum = 0
                    self.names = []

            groups = []

            def collectPos(groups,key):
                for g in groups:
                    if g.id == key:
                        if len(g.values) < nGroupSize:
                            return g
                g = Group(key)
                groups.append(g)
                return g

            for pos in self.participants_by_race.query( \
                orderBy="duration"):
                if pos.duration != None:
                    if sex is None or pos.person.sex == sex:
                        key = getattr(pos,xcKey)
                        if key is not None:
                            v = getattr(pos,xnValue)
                            g = collectPos(groups,key)
                            g.values.append(v)
                            g.sum += v
                            if xcName is None:
                                g.names.append(str(v))
                            else:
                                g.names.append(xcName(pos))

            groups = filter(lambda g: len(g.values) == nGroupSize,
                            groups)
            groups.sort(lambda a,b: a.sum - b.sum)

            rpt = prn.report(label="inter %s %s by %d" % (xcKey,
                                                          sex,
                                                          nGroupSize))
            rpt.addColumn(meth=lambda g: str(g.id),
                          label=xcKey,
                          width=20)
            rpt.addColumn(meth=lambda g: str(g.sum),
                          label=xnValue,
                          width=5)
            rpt.addColumn(
                meth=lambda g: " + ".join(g.names)+" = " +str(g.sum),
                label="values",
                width=40)
            rpt.execute(groups[:maxGroups])

            


        
        
class RaceTypes(Table):
    def init(self):
        self.addField('id',STRING(width=5))
        self.addField('name',NAME)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name
        
class Clubs(Table):
    def init(self):
        self.addField('id',STRING(width=5))
        self.addField('name',NAME)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name
        
class Categories(Table):
    def init(self):
        self.addPointer('type',RaceTypes)
        self.addField('id',STRING(width=3))
        self.addField('seq',ROWID)
        self.addField('name',STRING(width=30))
        self.addField('sex',SEX)
        self.addField('ageLimit',INT)
        
        self.setPrimaryKey('type id')

    class Instance(Table.Instance):
        def getLabel(self):
            return self.id + " ("+self.name+")"
        
class Participants(Table):
    def init(self):
        self.setPrimaryKey("race dossard")
        
        self.addPointer('race',Races).setDetail('participants')
        self.addField('dossard',DOSSARD)
        self.addPointer('person',Persons)
        self.addPointer('club',Clubs)
        self.addField('duration',DURATION)
        self.addPointer('cat',Categories)
        self.addField('payment',STRING(width=1))
        self.addField('place',INT)
        self.addField('catPlace',INT)
        

class Arrivals(Table):
    def init(self):
        self.addPointer('race',Races).setDetail('arrivals')
        self.addField('dossard',DOSSARD)
        self.addField('time',TIME)
        self.addField('duration',DURATION)
        self.addField('ok',BOOL)
        


# order of tables is important: tables will be populated in this order
TABLES = (
    Clubs,
    Persons,
    RaceTypes,
    Categories,
    Races,
    Participants,
    Arrivals,
    )


def setupSchema(schema):
    for t in TABLES:
        schema.addTable(t)

