# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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


USAGE = """
Validate an XML file against the XSD for a SEPA payment order.

Usage:

  python -m lino.utils.xmlgen.sepa.validate XMLFILE

Arguments:
 
XMLFILE : the name of the xml file to validate, or '-' to read from stdin
"""

import sys
from os.path import join, dirname
from lxml import etree

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print USAGE
        sys.exit(-1)

    xmlfile = sys.argv[1]
    doc = etree.parse(file(xmlfile))
    
    xsdfile = join(dirname(__file__),'XSD','pain.001.001.02.xsd')
    xsd = etree.XMLSchema(etree.parse(file(xsdfile)))
    
    xsd.assertValid(doc)

