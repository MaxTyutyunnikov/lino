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


""" 20040206 : bug fixed

problem when accessing data that was already in the database.

In the following test, p[2] returned the same row as the previous p[1]


"""
from lino.misc.tsttools import TestCase, main
from lino.schemas.sprl import demo #.sprl import Schema
from lino.schemas.sprl.tables import *
from lino.adamo import center

class Case(TestCase):

    def test01(self):
        "Accessing data that has not been inserted using adamo"
        sess = demo.startup(self.ui,populate=False)
        
        db = sess.db
        connection = center._center._connections[0]
        
        connection.sql_exec("""
        INSERT INTO PARTNERS (id,name)
               VALUES (1, "Luc");
        """)

        connection.sql_exec("""
        INSERT INTO PARTNERS (id,name)
               VALUES (2, "Ly");
        """)

        PARTNERS = sess.query(Partners)

        luc = PARTNERS.peek(1)
        self.assertEqual(luc.id,1)
        self.assertEqual(luc.name,"Luc")
        ly = PARTNERS.peek(2)
        self.assertEqual(ly.id,2)
        self.assertEqual(ly.name,"Ly")

        self.failIf(luc.isDirty())
        self.failIf(ly.isDirty())
        
        #db.close()
        sess.shutdown()

    def test02(self):
        d = {}
        id1 = (1,)
        id2 = (2,)
        s1 = "Luc"
        s2 = "Ly"
        d[id1] = s1
        d[id2] = s2
        
        self.assertEqual(d[id1],'Luc')
        self.assertEqual(d[id2],'Ly')

if __name__ == '__main__':
    main()

