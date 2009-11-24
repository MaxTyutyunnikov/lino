## Copyright 2008-2009 Luc Saffre
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


import sys
import decimal
#import logging ; logger = logging.getLogger('lino.apps.finan')

from django import forms

from lino import reports
from lino import layouts
from lino.utils import perms

from django.db import models
from lino.modlib import fields

contacts = reports.get_app('contacts')
ledger = reports.get_app('ledger')
journals = reports.get_app('journals')

#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.ledger import models as ledger
#~ from lino.modlib.journals import models as journals

def _functionId(nFramesUp):
    # thanks to:
    # http://nedbatchelder.com/blog/200410/file_and_line_in_python.html
    """ Create a string naming the function n frames up on the stack.
    """
    co = sys._getframe(nFramesUp+1).f_code
    return "%s (%s:%d)" % (co.co_name, co.co_filename, co.co_firstlineno)


def todo_notice(msg):
    print "[todo] in %s :\n       %s" % (_functionId(1),msg)
  
class BankStatement(ledger.LedgerDocument):
    
    date = fields.MyDateField()
    balance1 = fields.PriceField()
    balance2 = fields.PriceField()
    
    def before_save(self):
        if not self.booked:
            if self.value_date is None:
                self.value_date = self.date
            #journals.AbstractDocument.before_save(self)
            #ledger.LedgerDocumentMixin.before_save(self)
            balance = self.balance1
            if self.id is not None:
                for i in self.docitem_set.all():
                    balance += i.debit - i.credit
            self.balance2 = balance
        super(BankStatement,self).before_save()
        
    #~ def after_save(self):
        #~ lino.log.info("Saved document %s (balances=%r,%r)",self,self.balance1,self.balance2)
        
    def collect_bookings(self):
        sum_debit = 0 # decimal.Decimal(0)
        for i in self.docitem_set.all():
            b = self.create_booking(
              pos=i.pos,
              account=i.account,
              partner=i.partner,
              date=i.date,
              debit=i.debit,
              credit=i.credit)
            sum_debit += i.debit - i.credit
            yield b
        #todo_notice("BankStatement.balance1 and 2 are strings?!")
        #http://code.google.com/p/lino/issues/detail?id=1
        #lino.log.info("finan.BankStatement %r %r",self.balance1, sum_debit)
        self.balance2 = self.balance1 + sum_debit
        #jnl = self.get_journal()
        acct = ledger.Account.objects.get(id=self.journal.account)
        b = self.create_booking(account=acct)
        if sum_debit > 0:
            b.debit = sum_debit
        else:
            b.credit = - sum_debit
        yield b
        
        
    def add_item(self,account=None,partner=None,**kw):
        pos = self.docitem_set.count() + 1
        if account is not None:
            if not isinstance(account,ledger.Account):
                account = ledger.Account.objects.get(pk=account)
        if partner is not None:
            if not isinstance(partner,contacts.Partner):
                partner = contacts.Partner.objects.get(pk=partner)
        kw['account'] = account
        kw['partner'] = partner
        for k in ('debit','credit'):
            v = kw.get(k,None)
            if isinstance(v,basestring):
                kw[k] = decimal.Decimal(v)
        return self.docitem_set.create(**kw)
    
  
class DocItem(models.Model):
    document = models.ForeignKey(BankStatement) 
    pos = models.IntegerField("Position")
    date = fields.MyDateField(blank=True,null=True)
    debit = fields.PriceField(default=0)
    credit = fields.PriceField(default=0)
    remark = models.CharField(max_length=200,blank=True)
    account = models.ForeignKey(ledger.Account)
    partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    
    def save(self,*args,**kw):
        if self.pos is None:
            self.pos = self.document.docitem_set.count() + 1
        return super(DocItem,self).save(*args,**kw)
        
    def __unicode__(self):
        return u"DocItem %s.%d" % (self.document,self.pos)
        
#~ class Booking(models.Model):
    #~ #journal = models.ForeignKey(journals.Journal)
    #~ #number = models.IntegerField()
    #~ document = models.ForeignKey(LedgerDocument) 
    #~ pos = models.IntegerField("Position")
    #~ date = fields.MyDateField() 
    #~ account = models.ForeignKey(Account)
    #~ contact = models.ForeignKey(contacts.Contact,blank=True,null=True)
    #~ debit = fields.PriceField(default=0)
    #~ credit = fields.PriceField(default=0)
    

##
## report definitions
##        
        

class FinDocPageLayout(layouts.PageLayout):
    
    box1 = """
    date value_date
    ledger_remark
    """
    
    balance = """
    balance1
    balance2
    """
    
    main = """
            box1 balance
            ItemsByDocument
            """
    
class BankStatements(journals.DocumentsByJournal):
    model = BankStatement
    page_layouts = (FinDocPageLayout, )
    columnNames = "number date balance1 balance2 ledger_remark value_date"
    
    
    
class DocItems(reports.Report):
    columnNames = "document pos:3 "\
                  "date account partner remark debit credit" 
    model = DocItem
    order_by = "pos"

class ItemsByDocument(DocItems):
    columnNames = "pos:3 date account partner remark debit credit" 
    #master = BankStatement
    fk_name = 'document'
    order_by = "pos"
    
BankStatement.content = ItemsByDocument

journals.register_doctype(BankStatement,BankStatements)
