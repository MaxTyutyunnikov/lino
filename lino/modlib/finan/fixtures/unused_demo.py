# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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

#import time
#from datetime import date
#from dateutil import parser as dateparser
#from lino.projects.finan import models as finan
#~ import decimal
from decimal import Decimal
from django.conf import settings

from lino import dd
from lino.utils import Cycler
from lino.utils.instantiator import Instantiator, i2d
from lino.core.dbutils import resolve_model

partner_model = settings.SITE.partners_app_label + '.Partner'
Partner = dd.resolve_model(partner_model)


REQUEST = None


def objects():
  
  
    ledger = dd.resolve_app('ledger')
    finan = dd.resolve_app('finan')
    #~ partners = dd.resolve_app('partners')
    #~ contacts = dd.resolve_app('contacts')
    
    
    MODEL = finan.BankStatement
    vt = ledger.VoucherTypes.get_for_model(MODEL)
    JOURNALS = Cycler(vt.get_journals())
    PARTNERS = Cycler(Partner.objects.order_by('name'))
    USERS = Cycler(settings.SITE.user_model.objects.all())
    AMOUNTS = Cycler([Decimal(x) for x in 
        "2.50 6.80 9.95 14.50 20 29.90 39.90 39.90 99.95 199.95 599.95 1599.99".split()])
    ITEMCOUNT = Cycler(1,3,10)
    for i in range(2):
        jnl = JOURNALS.pop()
        voucher = MODEL(journal=jnl,
          user=USERS.pop(),
          date=settings.SITE.demo_date(-30+i))
        yield voucher
        ACCOUNTS = Cycler(jnl.get_allowed_accounts())
        for j in range(ITEMCOUNT.pop()):
            item = voucher.add_voucher_item(
                partner=PARTNERS.pop(),
                account=ACCOUNTS.pop(),
                amount=AMOUNTS.pop()
                )
            #~ item.total_incl_changed(REQUEST)
            #~ item.before_ui_save(REQUEST)
            #~ if item.total_incl:
                #~ print "20121208 ok", item
            #~ else:
                #~ if item.product.price:
                    #~ raise Exception("20121208")
            yield item
        voucher.register(REQUEST)
        yield voucher

    
