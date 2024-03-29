#coding: utf8
## Copyright 2009 Luc Saffre

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

import time
from datetime import date
from dateutil import parser as dateparser
from lino.ledger.models import *
from lino.utils.instantiator import Instantiator
from lino.utils import journals

def i2d(i):
    return dateparser.parse(str(i))

account = Instantiator(Account,"name").build


def objects():
    
    BANK = journals.create_journal("BANK",FinancialDocument)
    
    EL = account("Electricity")
    IN = account("Internet")
    CU = account("Customers")
    PR = account("Providers")
    
    doc = BANK.create_document(creation_date=i2d(20090501))
    doc.add_item(account=PR,contact=Contact.objects.get(pk=2),
      debit='12.49')

    return [ BANK, EL, IN, CU, PR, doc ]