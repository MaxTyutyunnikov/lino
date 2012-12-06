## Copyright 2008-2012 Luc Saffre
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

"""
General Ledger. 

"""

import logging
logger = logging.getLogger(__name__)

import datetime
from decimal import Decimal

from django.db import models
from django.conf import settings

from lino import dd
from lino import mixins
from lino.utils import babel
from lino.core.modeltools import full_model_name
#~ from lino.utils.choicelists import Choice
#contacts = reports.get_app('contacts')
#~ from lino.modlib.journals import models as journals
#~ journals = reports.get_app('journals')
#from lino.modlib.contacts import models as contacts
#from lino.modlib.journals import models as journals
from django.utils.translation import ugettext_lazy as _
from lino.modlib.ledger.utils import FiscalYears
#~ from lino.modlib.accounts.utils import AccountTypes

accounts = dd.resolve_app('accounts')
vat = dd.resolve_app('vat')

ZERO = Decimal()

#~ DOCTYPES = []
#~ DOCTYPE_CHOICES = []

#~ def register_voucher_type(docclass,rptclass=None):
    #~ type_id = len(DOCTYPE_CHOICES)
    #~ DOCTYPE_CHOICES.append((type_id,docclass.__name__))
    #~ DOCTYPES.append((docclass,rptclass))
    #~ docclass.doctype = type_id
    #~ return type_id

#~ def get_doctype(cl):
    #~ i = 0
    #~ for c,r in DOCTYPES:
        #~ if c is cl:
            #~ return i
        #~ i += 1
    #~ return None


#~ def default_year():
    #~ return datetime.date.today().year
    
#~ def YearRef(**kw):
    #~ kw.setdefault('default',default_year)
    #~ return models.IntegerField(**kw)

      
class VoucherType(dd.Choice):
    def __init__(self,cls,model,table_class):
        self.table_class = table_class
        self.model = model
        value = full_model_name(model)
        text = model._meta.verbose_name + ' (%s.%s)' % (
            model.__module__,model.__name__)
        name = None
        super(VoucherType,self).__init__(cls,value,text,name)
        
class VoucherTypes(dd.ChoiceList):
    item_class = VoucherType
    #~ blank = False
    max_length = 100
    
    @classmethod
    def add_item(cls,model,table_class):
        return cls.add_item_instance(VoucherType(cls,model,table_class))
    
  
#~ class VatClasses(ChoiceList):
    #~ """
    #~ A VAT rate determines the *rate* of VAT.
    #~ The actual rates are not stored here, 
    #~ they vary depending on your country, 
    #~ the time and type of the operation, 
    #~ and possibly other factors.
    #~ """
    #~ label = _("VAT Rate")
#~ add = VatClasses.add_item
#~ add('0',_("Exempt"),'exempt')
#~ add('1',_("Reduced"),'reduced')
#~ add('2',_("Normal"),'normal')


#~ class VatRegimes(ChoiceList):
    #~ """
    #~ While the rate of VAT is determined using :class:`VatClasses`,
    #~ the VAT regime determines how the VAT is being handled: 
    #~ whether and how it is to be paid.
    #~ """
    #~ label = _("VAT Regimes")
#~ add = VatRegimes.add_item
#~ add('10',_("Private person"),'private')
#~ add('20',_("Subject to VAT"),'subject')
#~ add('25',_("Co-contractor"),'cocontractor')
#~ add('30',_("Intra-community"),'intracom')
#~ add('40',_("Outside EU"),'outside')


    
#~ class JournalTypes(ChoiceList):
    #~ label = _("Journal Type")
#~ add = JournalTypes.add_item
#~ add('S',_("Sales"),'sales')
#~ add('P',_("Purchases"),'purchases')
#~ add('F',_("Financial"),'financial')

class Journal(babel.BabelNamed,mixins.Sequenced):
  
    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")
        
    #~ id = models.CharField(max_length=4,primary_key=True)
    ref = dd.NullCharField(max_length=20,unique=True)
    #~ name = models.CharField(max_length=100)
    trade_type = vat.TradeTypes.field()
    #~ doctype = models.IntegerField() #choices=DOCTYPE_CHOICES)
    voucher_type = VoucherTypes.field() 
    force_sequence = models.BooleanField(default=False)
    #~ total_based = models.BooleanField(_("Voucher entry based on total amount"),default=False)
    chart = models.ForeignKey('accounts.Chart')
    #~ chart = models.ForeignKey('accounts.Chart',blank=True,null=True)
    #~ account = models.ForeignKey('accounts.Account',blank=True,null=True)
    #~ account = models.CharField(max_length=6,blank=True)
    #~ pos = models.IntegerField()
    #~ printed_name = models.CharField(max_length=100,blank=True)
    printed_name = babel.BabelCharField(max_length=100,blank=True)
    
    def get_doc_model(self):
        """The model of vouchers in this Journal."""
        #print self,DOCTYPE_CLASSES, self.doctype
        return self.voucher_type.model
        #~ return DOCTYPES[self.doctype][0]

    def get_doc_report(self):
        return self.voucher_type.table_class
        #~ return DOCTYPES[self.doctype][1]

    def get_voucher(self,year=None,number=None,**kw):
        cl = self.get_doc_model()
        kw.update(journal=self,year=year,number=number) 
        return cl.objects.get(**kw)
        
    def create_voucher(self,**kw):
        """Create an instance of this Journal's voucher model (:meth:`get_doc_model`)."""
        cl = self.get_doc_model()
        kw.update(journal=self) 
        try:
            doc = cl() 
            #~ doc = cl(**kw) # wouldn't work. See Django ticket #10808
            #~ doc.journal = self
            for k,v in kw.items():
                setattr(doc,k,v)
            #~ print 20120825, kw
        except TypeError,e:
            #~ print 20100804, cl
            raise
        #~ doc.full_clean()
        #~ doc.save()
        return doc
        
    def get_next_number(self,voucher):
        self.save()
        cl = self.get_doc_model()
        d = cl.objects.filter(journal=self,year=voucher.year).aggregate(
            models.Max('number'))
        number = d['number__max']
        logger.info("20121206 get_next_number %r",number)
        if number is None:
            return 1
        return number + 1
        
    def __unicode__(self):
        s = super(Journal,self).__unicode__()
        if self.ref:
            s += " (%s)" % self.ref
            #~ return '%s (%s)' % (babel.BabelNamed.__unicode__(self),self.ref or self.id)
        return s
            #~ return self.ref +'%s (%s)' % babel.BabelNamed.__unicode__(self)
            #~ return self.id +' (%s)' % babel.BabelNamed.__unicode__(self)
        
    def save(self,*args,**kw):
        #~ self.before_save()
        r = super(Journal,self).save(*args,**kw)
        self.after_save()
        return r
        
    def after_save(self):
        pass
        
    def full_clean(self,*args,**kw):
        if not self.name:
            self.name = self.id
        #~ if not self.pos:
            #~ self.pos = self.__class__.objects.all().count() + 1
        super(Journal,self).full_clean(*args,**kw)
      
        
    #~ def pre_delete_voucher(self,doc):
    def disable_voucher_delete(self,doc):
        #print "pre_delete_voucher", doc.number, self.get_next_number()
        if self.force_sequence:
            if doc.number + 1 != self.get_next_number(doc):
                return _("%s is not the last voucher in journal" % unicode(doc))



class Journals(dd.Table):
    model = Journal
    order_by = ["seqno"]
    column_names = "seqno id trade_type voucher_type name force_sequence *"
    detail_layout = """
    seqno id trade_type voucher_type 
    force_sequence 
    name
    printed_name
    """
    insert_layout = dd.FormLayout("""
    name
    trade_type 
    voucher_type 
    """,window_size=(60,'auto'))
    

                  
def JournalRef(**kw):
    #~ kw.update(blank=True,null=True) # Django Ticket #12708
    kw.update(related_name="%(app_label)s_%(class)s_set_by_journal")
    return models.ForeignKey(Journal,**kw)

def VoucherNumber(**kw):
    return models.IntegerField(**kw)
    


class RegisterVoucher(dd.RowAction):
    label = _("Register") 
    show_in_workflow = True
    
    #~ icon_file = 'cancel.png'
    #~ icon_file = 'flag_green.png'
    required = dict(states='draft')
    help_text=_("Register this voucher.")
  
    def get_action_permission(self,ar,obj,state):
        if obj.user != ar.get_user():
            return False
        return super(RegisterVoucher,self).get_action_permission(ar,obj,state)
        
    def run(self,obj,ar,**kw):
        #~ ar.confirm(self.help_text,_("Are you sure?"))
        obj.register_voucher(ar)
        obj.save()
        kw.update(refresh=True)
        return kw
    
    
class UnregisterVoucher(dd.RowAction):
    label = _("Unregister")
    show_in_workflow = True
    
    icon_file = 'cancel.png'
    required = dict(states='registered paid')
    help_text=_("Unregister this voucher.")
  
    def get_action_permission(self,ar,obj,state):
        if obj.user != ar.get_user():
            return False
        return super(UnregisterVoucher,self).get_action_permission(ar,obj,state)
        
    def run(self,obj,ar,**kw):
        #~ ar.confirm(self.help_text,_("Are you sure?"))
        obj.unregister_voucher(ar)
        obj.save()
        kw.update(refresh=True)
        return kw


#~ class Voucher(mixins.Controllable):
class Voucher(mixins.UserAuthored,mixins.ProjectRelated):
    """
    A Voucher is a document that represents a monetary transaction.
    Subclasses must define a field `state`.
    This model is subclassed by sales.Invoice, ledger.AccountInvoice, 
    finan.Statement etc...
    
    It is **not** abstract because we have a ForeignKey to Voucher in Movement,
    and we want one Movement model for all ledger movements.
    
    """
    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Vouchers")
        #~ abstract = True
        
    #~ controller_is_optional = False
    
    journal = JournalRef()
    year = FiscalYears.field(blank=True)
    number = VoucherNumber(blank=True,null=True)
    date = models.DateField(default=datetime.date.today)
    #~ ledger_remark = models.CharField("Remark for ledger",
      #~ max_length=200,blank=True)
    narration = models.CharField(_("Narration"),max_length=200,blank=True)
    
    register_action = RegisterVoucher()
    unregister_action = UnregisterVoucher()
    
    #~ @classmethod
    #~ def create_journal(cls,id,**kw):
        #~ doctype = get_doctype(cls)
        #~ jnl = Journal(doctype=doctype,id=id,**kw)
        #~ return jnl
        
    @classmethod
    def create_journal(cls,trade_type,**kw):
    #~ def create_journal(cls,jnl_id,trade_type,**kw):
        #~ doctype = get_doctype(cls)
        #~ jnl = Journal(doctype=doctype,id=jnl_id,*args,**kw)
        tt = vat.TradeTypes.get_by_name(trade_type)
        vt = VoucherTypes.get_by_value(full_model_name(cls))
        #~ jnl = Journal(trade_type=tt,voucher_type=vt,id=jnl_id,**kw)
        jnl = Journal(trade_type=tt,voucher_type=vt,**kw)
        return jnl
        
    @classmethod
    def get_journals(cls):
        vt = VoucherTypes.get_by_value(full_model_name(cls))
        #~ doctype = get_doctype(cls)
        return Journal.objects.filter(voucher_type=vt).order_by('seqno')
            
        
    def __unicode__(self):
        if self.number is None:
            return "Voucher #%s (not registered)" % (self.id)
        return "%s-%s/%s" % (self.journal.pk,self.year,self.number)
        
                
    def register_voucher(self,ar):
        if self.year is None:
            self.year = FiscalYears.from_date(self.date)
        if self.number is None:
            self.number = self.journal.get_next_number(self)
        assert self.number is not None
        """
        delete any existing movements and re-create them
        """
        self.movement_set.all().delete() 
        for m in self.get_wanted_movements():
            m.full_clean()
            m.save()
        state_field = self._meta.get_field('state')
        self.state = state_field.choicelist.registered
        
    def unregister_voucher(self,ar):
        self.number = None
        self.movement_set.all().delete() 
        state_field = self._meta.get_field('state')
        self.state = state_field.choicelist.draft
        
        
    def disable_delete(self,ar):
        msg = self.journal.disable_voucher_delete(self)
        if msg is not None:
            return msg
        return super(Voucher,self).disable_delete(ar)
            
        
    #~ def delete(self):
        #~ self.journal.pre_delete_voucher(self)
        #~ return super(Voucher,self).delete()
        
    #~ def get_child_model(self):
        #~ ## overrides Typed
        #~ return DOCTYPES[self.journal.doctype][0]
        
        
    #~ def get_wanted_movements(self):
        #~ raise NotImplementedError()
        #~ return []
        
    #~ def create_movement_credit(self,account,amount,**kw):
        #~ kw.update(is_credit=True)
        #~ return self.create_movement(account,amount,**kw)
        
    #~ def create_movement_debit(self,account,amount,**kw):
        #~ kw.update(is_credit=False)
        #~ return self.create_movement(account,amount,**kw)
        
    def create_movement(self,account,amount,**kw):
        assert isinstance(account,accounts.Account)
        kw['voucher'] = self
        #~ account = accounts.Account.objects.get(group__ref=account)
        #~ account = self.journal.chart.get_account_by_ref(account)
        kw['account'] = account
        if amount >= 0:
            kw['amount'] = amount
            kw['dc'] = account.type.dc
        else:
            kw['amount'] = - amount
            kw['dc'] = not account.type.dc
        
        #~ kw['journal'] = self.journal
        #~ kw['year'] = self.year
        #~ kw['number'] = self.number
        #~ kw['voucher'] = self
        #kw['number'] = self.number
        #~ kw.setdefault('date',self.date)
        #~ if not kw.get('date',None):
            #~ kw['date'] = self.value_date
        b = Movement(**kw)
        #print b.date
        #b.save()
        return b
        
    def get_row_permission(self,ar,state,ba):
        """
        Only invoices in an editable state may be edited.
        """
        if not ba.action.readonly and not self.state.editable:
            return False
        return super(Voucher,self).get_row_permission(ar,state,ba)

    
        

class DebitOrCreditField(models.BooleanField):
    pass


    
class Movement(mixins.Sequenced):
  
    allow_cascaded_delete = ['voucher']
    
    voucher = models.ForeignKey(Voucher)
    #~ pos = models.IntegerField("Position",blank=True,null=True)
    account = models.ForeignKey(accounts.Account)
    partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    amount = dd.PriceField(default=0)
    dc = DebitOrCreditField()
    #~ is_credit = models.BooleanField(_("Credit"),default=False)
    #~ debit = dd.PriceField(default=0)
    #~ credit = dd.PriceField(default=0)
    
    @dd.virtualfield(dd.PriceField(_("Debit")))
    def debit(self,ar):
        if self.dc: 
            return ZERO
        return self.amount
    
    @dd.virtualfield(dd.PriceField(_("Credit")))
    def credit(self,ar):
        if self.dc: 
            return self.amount
        return ZERO
            
    
    def get_siblings(self):
        return self.voucher.movement_set.order_by('seqno')
        #~ return self.__class__.objects.filter().order_by('seqno')
        
    def __unicode__(self):
        return u"%s.%d" % (unicode(self.voucher),self.seqno)
        
    

class Movements(dd.Table): 
    model = Movement
    column_names = 'voucher account debit credit *'
    editable = False
    
class MovementsByVoucher(Movements):
    master_key = 'voucher'
    column_names = 'seqno account debit credit'
    
class MovementsByPartner(Movements):
    master_key = 'partner'
    column_names = 'seqno account voucher debit credit'
    



class InvoiceStates(dd.Workflow):
    #~ label = _("State")
    pass
add = InvoiceStates.add_item
add('10',_("Draft"),'draft',editable=True) 
add('20',_("Registered"),'registered',editable=False) 
#~ add('20',_("Signed"),'signed')
#~ add('30',_("Sent"),'sent')
add('40',_("Paid"),'paid',editable=False)

#~ InvoiceStates.draft.add_workflow(_("Unregister"),states='registered paid')
#~ InvoiceStates.registered.add_workflow(_("Register"),states='draft')
    
class AccountInvoice(vat.VatDocument,Voucher):
    
    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
    
    your_ref = models.CharField(_("Your reference"),
        max_length=200,blank=True)
    
    due_date = models.DateField(_("Due date"),blank=True,null=True)
    
    state = InvoiceStates.field(default=InvoiceStates.draft)
    
    workflow_state_field = 'state'
    
    def get_trade_type(self):
        return self.journal.trade_type
        
    def add_item(self,account=None,**kw):
        if account is not None:
            #~ if not isinstance(account,accounts.Account):
            if isinstance(account,basestring):
                #~ account = accounts.Account.objects.get(group__ref=account)
                #~ account = accounts.Account.objects.get(ref=account)
                account = self.journal.chart.get_account_by_ref(account)
        kw['account'] = account
        kw['voucher'] = self
        return self.items.model(**kw)
        
    


class VoucherItem(dd.Model):
    """
    Subclasses must define a field `voucher` which must be a FK with related_name='items'
    """
    
    allow_cascaded_delete = ['voucher']
    
    class Meta:
        abstract = True
        
    title = models.CharField(max_length=200,blank=True)
    
    def get_row_permission(self,ar,state,ba):
        """
        Items of registered invoices may not be edited
        """
        if not self.voucher.get_row_permission(ar,state,ba):
            return False
        return super(VoucherItem,self).get_row_permission(ar,state,ba)


class InvoiceDetail(dd.FormLayout):
    main = "general ledger"
    
    totals = """
    total_base
    total_vat
    total_incl
    workflow_buttons
    """
    
    general = dd.Panel("""
    id date partner user 
    due_date your_ref vat_regime item_vat
    ItemsByInvoice:60 totals:20
    """,label=_("General"))
    
    ledger = dd.Panel("""
    journal year number narration
    MovementsByVoucher
    """,label=_("Ledger"))
    
class Invoices(dd.Table):
    parameters = dict(
        pyear=FiscalYears.field(blank=True),
        ppartner=models.ForeignKey('contacts.Partner',blank=True,null=True),
        pjournal=JournalRef(blank=True))
    model = AccountInvoice
    order_by = ["id"]
    column_names = "id date partner total_incl user *" 
    params_layout = "pjournal pyear ppartner"
    detail_layout = InvoiceDetail()
    insert_layout = dd.FormLayout("""
    partner
    date total_incl
    """,window_size=(60,'auto'))
    
    @classmethod
    def get_request_queryset(cls,ar):
        qs = super(Invoices,cls).get_request_queryset(ar)
        if ar.param_values.ppartner:
            qs = qs.filter(partner=ar.param_values.ppartner)
        if ar.param_values.pyear:
            qs = qs.filter(year=ar.param_values.pyear)
        if ar.param_values.pjournal:
            qs = qs.filter(journal=ar.param_values.pjournal)
        return qs
    
    
    
class InvoicesByJournal(Invoices):
    order_by = ["number"]
    master_key = 'journal' # see django issue 10808
    #master = journals.Journal
    column_names = "number date due_date " \
                  "partner " \
                  "total_incl " \
                  "total_base total_vat user *"
                  #~ "ledger_remark:10 " \
    params_panel_hidden = True
                  
    @classmethod
    def get_title_base(self,ar):
        return unicode(ar.master_instance)
        #~ title = _("%(details)s of %(master)s") % dict(
          #~ details=title,
          #~ master=ar.master_instance)
        #~ return title
                  

class InvoiceItem(VoucherItem,vat.VatItemBase):
    
    #~ document = models.ForeignKey(AccountInvoice,related_name='items') 
    voucher = models.ForeignKey(AccountInvoice,related_name='items') 
    
    #~ account = models.ForeignKey('accounts.Account',blank=True,null=True)
    account = models.ForeignKey('accounts.Account')
    
    def get_base_account(self,tt):
        return self.account
        
    @dd.chooser()
    def account_choices(self,voucher):
        if voucher and voucher.journal:
            fkw = {voucher.journal.trade_type.name+'_allowed':True}
            return accounts.Account.objects.filter(chart=voucher.journal.chart,**fkw)
        return []


class ItemsByInvoice(dd.Table):
    model = InvoiceItem
    column_names = "account title vat_class total_base total_vat total_incl seqno"
    master_key = 'voucher'
    order_by = ["seqno"]
    

class InvoicesByPartner(Invoices):
    order_by = ["date"]
    master_key = 'partner'
    column_names = "date total_incl total_base total_vat *"
    


#~ register_voucher_type(Invoice,InvoicesByJournal)
VoucherTypes.add_item(AccountInvoice,InvoicesByJournal)

#~ MODULE_LABEL = _("Ledger")
MODULE_LABEL = accounts.MODULE_LABEL

def site_setup(site):
    if site.is_installed('contacts'):
        for t in (site.modules.contacts.Partners,
          site.modules.contacts.Persons,
          site.modules.contacts.Companies):
            t.add_detail_tab("ledger",
                """
                ledger.InvoicesByPartner
                ledger.MovementsByPartner
                """,
                label=MODULE_LABEL)


def setup_main_menu(site,ui,profile,m): 
    m = m.add_menu(vat.TradeTypes.purchases.name,vat.TradeTypes.purchases.text)
    
    for jnl in Journal.objects.all():
        if jnl.trade_type == vat.TradeTypes.purchases:
            m.add_action(jnl.voucher_type.table_class,
                label=unicode(jnl),
                params=dict(master_instance=jnl))


#~ def setup_main_menu(site,ui,user,m): 
    #~ m = m.add_menu("ledger",MODULE_LABEL)
    #~ for jnl in Journal.objects.all():
        #~ m.add_action(jnl.voucher_type.table_class,
            #~ label=unicode(jnl),
            #~ params=dict(master_instance=jnl))
    
def setup_my_menu(site,ui,profile,m): 
    pass
  
def setup_config_menu(site,ui,profile,m): 
    #~ m = m.add_menu("ledger",MODULE_LABEL)
    m = m.add_menu("accounts",MODULE_LABEL)
    m.add_action(Journals)
    
    
def setup_explorer_menu(site,ui,profile,m):
    #~ m = m.add_menu("ledger",MODULE_LABEL)
    m = m.add_menu("accounts",MODULE_LABEL)
    m.add_action(Invoices)
    m.add_action(VoucherTypes)
  


def customize_accounts():

    for tt in vat.TradeTypes.objects():
        dd.inject_field('accounts.Account',
            tt.name+'_allowed',
            models.BooleanField(verbose_name=tt.text))

customize_accounts()
