# coding: latin1
## Copyright Luc Saffre 2003-2005

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


"""

Deciding whether to store values of a DataRow in a tuple of atomic
values or in a dict of complex values...

1. I iterate over a PARTNERS query with only the "currency" column
   (because this is the only one I am going to use. Plus the implicit
   "nation" column.

    The "print p" statement will do a call to Partners.getRowLabel()
    which will access row.name --- a field that was not included in my
    query!

    Or if I modify the row, then the validateRow() action will be
    triggered and it will ask for the partner's name.

    If a field was not part of the initial query, it will silently be
    looked up.

2. Accessing p.nation.name means that an attribute "p.nation" exists
   and has a Nations row as value.

3. (new:) Iterating over a row returns the cell value for each visible
   column of its query.



"""
from lino.misc.tsttools import TestCase, main

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Nations,Partners

class Case(TestCase):
    
    def test01(self):
        sess = demo.startup()
        be = sess.query(Nations).peek("be")
        q = sess.query(Partners,"title firstName name",nation=be)
        
        sess.startDump()
        q.executeReport(columnWidths="6 10 20")
        s = sess.stopDump()
        
        #print s
        
        self.assertEqual(s,"""\
Partners
========
title |firstName |name                
------+----------+--------------------
Herrn |Andreas   |Arens               
Dr.   |Henri     |Bodard              
Herrn |Emil      |Eierschal           
Frau  |Erna      |Eierschal           
Herrn |Gerd      |Gro�mann            
Herrn |Fr�d�ric  |Freitag             
      |          |PAC Systems PGmbH   
""")
                         
                

if __name__ == '__main__':
    main()

