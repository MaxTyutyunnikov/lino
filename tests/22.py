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


from lino.misc.tsttools import TestCase, main

from lino.apps.addrbook import demo
from lino.apps.addrbook.tables import Nation

class Case(TestCase):
    "Does the big demo database startup()"

    def setUp(self):
        TestCase.setUp(self)
        self.db = demo.startup(langs="en fr",big=True)

    def tearDown(self):
        self.db.shutdown()


    def test01(self):
        NATIONS = self.db.query(Nation)
        self.assertEqual(NATIONS.peek('ee').area,45226)
        self.assertEqual(NATIONS.peek('be').area,30510)
        self.assertEqual(NATIONS.peek('ee').population,1408556)
        self.assertEqual(NATIONS.peek('be').population,10289088)

if __name__ == '__main__':
    main()

