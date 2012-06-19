# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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
Defines models for :mod:`lino.modlib.outbox`.
"""

import logging
logger = logging.getLogger(__name__)

import os
import sys
import cgi
import datetime


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import IntegrityError
from django.utils.encoding import force_unicode


from lino import mixins
#~ from lino.mixins import mails
from lino import tools
from lino import dd
#~ from lino.utils.babel import default_language
#~ from lino import reports
#~ from lino import layouts
#~ from lino.utils import perms
from lino.utils.restify import restify
#~ from lino.utils import printable
from lino.utils import babel
#~ from lino.utils import call_optional_super
from django.conf import settings
#~ from lino import choices_method, simple_choices_method

#~ from lino.modlib.mails.utils import RecipientType

from lino.utils.html2text import html2text
from django.core.mail import EmailMultiAlternatives
from lino.utils.config import find_config_file
from lino.utils.choicelists import ChoiceList, UserLevel

from Cheetah.Template import Template as CheetahTemplate
#~ from lino.utils import dtosl, dtos

class RecipientType(ChoiceList):
    """
    A list of possible values for the `type` field of a 
    :class:`Recipient`.
    """
    label = _("Recipient Type")
    
add = RecipientType.add_item
add('to',_("to"),'to')
add('cc',_("cc"),'cc')
add('bcc',_("bcc"),'bcc')
#~ add('snail',_("Snail mail"),'snail')


#~ class MailType(mixins.PrintableType,babel.BabelNamed):
    #~ "Deserves more documentation."
  
    #~ templates_group = 'mails/Mail'
    
    #~ class Meta:
        #~ verbose_name = _("Mail Type")
        #~ verbose_name_plural = _('Mail Types')

#~ class MailTypes(dd.Table):
    #~ model = MailType
    #~ column_names = 'name build_method template *'


class CreateMailAction(dd.RowAction):
    """
    Creates an outbox mail and displays it.
    """
  
    url_action_name = 'mail'
    #~ label = _('Create email')
    #~ label = pgettext_lazy('verb','Mail')
    label = _('Mail')
    callable_from = None
    
    def get_view_permission(self,user):
        if not user.email:
            return False
        return super(CreateMailAction,self).get_view_permission(user)
        
    def run(self,elem,ar,**kw):
      
        as_attachment = elem.mail_as_attachment(ar)
        if as_attachment:
            html_content = elem.get_mailable_intro(ar)
        else:
            html_content = ''
        
        m = Mail(sender=ar.get_user(),
            subject=elem.get_mailable_subject(),
            body=html_content,
            owner=elem)
        m.full_clean()
        m.save()
        for t,p in elem.get_mailable_recipients():
            r = Recipient(mail=m,type=t,partner=p)
            r.full_clean()
            r.save()
        if as_attachment:
            a = Attachment(mail=m,owner=elem)
            a.save()
        js = ar.renderer.instance_handler(m)
        #~ url = rr.renderer.js2url(js)
        #~ kw.update(open_url=rr.renderer.get_detail_url(m))
        #~ kw.update(open_url=url)
        kw.update(eval_js=js)
        return ar.success_response(**kw)
        
    
class Mailable(models.Model):
    """
    Mixin for models that provide a "Post" button.
    A Mailable model must also inherit mixins.CachedPrintable (or mixins.TypedPrintable)
    """

    class Meta:
        abstract = True
        
    create_mail = CreateMailAction()
    #~ post2 = PostAction(True)
    
    #~ post_as_attachment = models.BooleanField(_("Post as attachment"),default=False)
        
        
    def get_print_language(self,pm):
        return babel.DEFAULT_LANGUAGE
        
    def get_mailable_intro(self,ar):
        tplname = self._meta.app_label + '/' + self.__class__.__name__ + '/email.html'
        fn = find_config_file(tplname)
        if fn is None:
            return ''
        #~ logger.info("Using email template %s",fn)
        tpl = CheetahTemplate(file(fn).read())
        #~ tpl.self = elem # doesn't work because Cheetah adds itself a name 'self' 
        tpl.dtosl = babel.dtosl
        tpl.dtos = babel.dtos
        tpl.instance = self
        return unicode(tpl)
        
    def mail_as_attachment(self,ar):
        return isinstance(self,mixins.CachedPrintable)
        
    def get_mailable_body(self,ar):
        raise NoteImplementdError()
        
    def get_mailable_subject(self):
        """
        Return the content of the `subject` 
        field for the email to be created.
        """
        return unicode(self)
        
    def get_mailable_recipients(self):
        "return or yield a list of (type,partner) tuples"
        return []
        

  
class Recipient(models.Model):
    """
    Abstract base for :class:`inbox.Recipient` and :class:`outbox.Recipient`.
    """
    allow_cascaded_delete = True
    
    class Meta:
        verbose_name = _("Recipient")
        verbose_name_plural = _("Recipients")
    mail = models.ForeignKey('outbox.Mail')
    partner = models.ForeignKey('contacts.Partner',
        #~ verbose_name=_("Recipient"),
        blank=True,null=True)
    type = RecipientType.field(default=RecipientType.to)
    address = models.EmailField(_("Address"))
    name = models.CharField(_("Name"),max_length=200)
    #~ address_type = models.ForeignKey(ContentType)
    #~ address_id = models.PositiveIntegerField()
    #~ address = generic.GenericForeignKey('address_type', 'address_id')
    
    def name_address(self):
        return '%s <%s>' % (self.name,self.address)      
        
    def __unicode__(self):
        return "[%s]" % unicode(self.name or self.address)
        #~ return "[%s]" % unicode(self.address)
        
    def full_clean(self):
        if self.partner:
            if not self.address:
                self.address = self.partner.email
            if not self.name:
                self.name = self.partner.get_full_name(salutation=False)
        super(Recipient,self).full_clean()
        


class Recipients(dd.Table):
    required_user_level = UserLevel.manager
    model = Recipient
    #~ column_names = 'mail  type *'
    #~ order_by = ["address"]

class RecipientsByMail(Recipients):
    required_user_level = None
    master_key = 'mail'
    column_names = 'type:10 partner:20 address:20 name:20 *'
    #~ column_names = 'type owner_type owner_id'
    #~ column_names = 'type owner'



class SendMailAction(dd.RowAction):
    """
    Sends this as an email.
    """
  
    url_action_name = 'send'
    label = _('Send email')
    callable_from = None
            
    def run(self,elem,rr,**kw):
        #~ if elem.sent:
            #~ return rr.ui.error_response(message='Mail has already been sent.')
        #~ subject = elem.subject
        #~ sender = "%s <%s>" % (rr.get_user().get_full_name(),rr.get_user().email)
        sender = "%s <%s>" % (elem.sender.get_full_name(),elem.sender.email)
        #~ recipients = list(elem.get_recipients_to())
        to = []
        cc = []
        bcc = []
        #~ [r.name_address() for r in elem.recipient_set.filter(type=mails.RecipientType.cc)]
        found = False
        for r in elem.recipient_set.all():
            recipients = None
            if r.type == RecipientType.to:
                recipients = to
            elif r.type == RecipientType.cc:
                recipients = cc
            elif r.type == RecipientType.bcc:
                recipients = bcc
            if recipients is not None:
                recipients.append(r.name_address())
                found = True
            #~ else:
                #~ logger.info("Ignoring recipient %s (type %s)",r,r.type)
        if not found:
            return rr.error_response("No recipients found.")
        as_attachment = elem.mail_as_attachment()
        if as_attachment:
            body = elem.body
        else:
            body = elem.owner.get_mailable_body(rr)
        text_content = html2text(body)
        msg = EmailMultiAlternatives(subject=elem.subject, 
            from_email=sender,
            body=text_content, 
            to=to,bcc=bcc,cc=cc)
        msg.attach_alternative(body, "text/html")
        for att in elem.attachment_set.all():
            #~ if as_attachment or att.owner != elem.owner:
            fn = att.owner.get_target_name()
            #~ msg.attach(os.path.split(fn)[-1],open(fn).read())
            msg.attach_file(fn)
        num_sent = msg.send()
            
        elem.sent = datetime.datetime.now()
        elem.save()
        kw.update(refresh=True)
        #~ msg = "Email %s from %s has been sent to %s." % (
            #~ elem.id,elem.sender,', '.join([
                #~ r.address for r in elem.recipient_set.all()]))
        msg = "Email %s from %s has been sent to %d recipients." % (
            elem.id,elem.sender,num_sent)
        kw.update(message=msg)
        #~ for n in """EMAIL_HOST SERVER_EMAIL EMAIL_USE_TLS EMAIL_BACKEND""".split():
            #~ msg += "\n" + n + " = " + unicode(getattr(settings,n))
        logger.info(msg)
        return rr.success_response(**kw)



#~ class Mail(mails.Mail,mixins.ProjectRelated,mixins.Controllable):
class Mail(mixins.Printable,mixins.ProjectRelated,mixins.Controllable):
  
    class Meta:
        verbose_name = _("Outgoing Mail")
        verbose_name_plural = _("Outgoing Mails")
        
    send_mail = SendMailAction()
    
    date = models.DateField(verbose_name=_("Date"),
        auto_now_add=True,
        help_text="""
        The official date to be printed on the document.
        """)
        
    subject = models.CharField(_("Subject"),
        max_length=200,blank=True,
        #null=True
        )
    body = dd.RichTextField(_("Body"),blank=True,format='html')
    
    #~ type = models.ForeignKey(MailType,null=True,blank=True)
    
    #~ send = SendMailAction()
        
    sender = models.ForeignKey(settings.LINO.user_model,
        verbose_name=_("Sender"))
        #~ related_name='outmails_by_sender',
        #~ blank=True,null=True)
    sent = models.DateTimeField(null=True,editable=False)

    #~ def disabled_fields(self,ar):
        #~ if not self.owner.post_as_attachment:
            #~ return ['body']
        #~ return []
        
    def get_print_language(self,bm):
        if self.sender is not None:
            return self.sender.language
        return super(Mail,self).get_print_language(bm)
        
    
    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name,self.pk)
        
    def get_recipients(self,rr):
        #~ recs = []
        recs = [ unicode(r) for r in 
            Recipient.objects.filter(mail=self,type=RecipientType.to)]
          
            #~ s = rr.ui.href_to(r.owner)
            #~ if r.type != RecipientType.to:
                #~ s += "(%s)" % r.type
            #~ recs.append(s)
        return ', '.join(recs)
    recipients = dd.VirtualField(dd.HtmlBox(_("Recipients")),get_recipients)
        

#~ class MailDetail(dd.DetailLayout):
    #~ main = """
    #~ """

class Mails(dd.Table):
    required_user_level = UserLevel.manager
    model = Mail
    column_names = "sent recipients subject * body"
    order_by = ["sent"]
    detail_template = """
    id sender date sent 
    subject
    RecipientsByMail:50x5 AttachmentsByMail:20x5
    body:90x10
    """
    
class MyOutbox(Mails):
    required_user_level = None
    #~ known_values = dict(outgoing=True)
    label = _("My Outbox")
    #~ filter = models.Q(sent__isnull=True)
    master_key = 'sender'
    
    @classmethod
    def setup_request(self,ar):
        if ar.master_instance is None:
            ar.master_instance = ar.get_user()
        #~ print "20120519 MyOutbox.setup_request()", ar.master_instance

#~ class MySent(MyOutbox):
    #~ label = _("Sent Mails")
    #~ filter = models.Q(sent__isnull=False)
    
class MailsByController(Mails):
    master_key = 'owner'
    #~ label = _("Postings")
    #~ slave_grid_format = 'summary'


#~ class MailsByPartner(object):
    #~ master = 'contacts.Partner'
    #~ can_add = perms.never
    

class Attachment(mixins.Controllable):
  
    allow_cascaded_delete = True
    
    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
        
    mail = models.ForeignKey('outbox.Mail')
    
    def __unicode__(self):
        if self.owner_id:
            return unicode(self.owner)
        return unicode(self.id)
        
    def save(self,*args,**kw):
        if not hasattr(self.owner,'get_target_url'):
            raise Exception("Controllers of Attachment must define a method `get_target_url`.")
        super(Attachment,self).save(*args,**kw)
        
    def summary_row(self,ui,**kw):
        url = self.owner.get_target_url(ui)
        #~ url = ui.build_url(*parts)
        text = url.split('/')[-1]
        return ui.ext_renderer.href(url,text)
        
        
        
class Attachments(dd.Table):
    model = Attachment
    #~ window_size = (400,500)
    #~ detail_template = """
    #~ mail owner
    #~ """
    
class AttachmentsByMail(Attachments):
    master_key = 'mail'
    slave_grid_format = 'summary'

class AttachmentsByController(Attachments):
    master_key = 'owner'


  
#~ class OutboxByPartner(Outbox,MailsByPartner):
class OutboxByUser(Mails):
    required_user_level = None
    label = _("Outbox")
    column_names = 'sent subject recipients'
    #~ order_by = ['sent']
    order_by = ['-date']
    master_key = 'sender'

class OutboxByProject(Mails):
    required_user_level = None
    label = _("Outbox")
    column_names = 'date subject recipients sender *'
    #~ order_by = ['sent']
    order_by = ['-date']
    master_key = 'project'
    
class SentByPartner(Mails):
    required_user_level = None
    master = 'contacts.Partner'
    label = _("Sent Mails")
    column_names = 'sent subject sender'
    order_by = ['sent']
    
    @classmethod
    def get_request_queryset(self,rr):
        q1 = Recipient.objects.filter(partner=rr.master_instance).values('mail').query
        qs = Mail.objects.filter(id__in=q1)
        qs = qs.order_by('sent')
        return qs
    





class PostingState(ChoiceList):
    """
    List of possible values for the `state` field of a 
    :class:`Posting`.
    """
    label = _("Posting State")
add = PostingState.add_item
add('00',_("New"),'new')
add('01',_("Ready to print"),'ready')
add('03',_("Printed"),'printed')
add('04',_("Sent"),'sent')
add('05',_("Returned"),'returned')
    

class Posting(mixins.Controllable):
    class Meta:
        verbose_name = _("Posting")
        verbose_name_plural = _("Postings")
    partner = models.ForeignKey('contacts.Partner',
        verbose_name=_("Recipient"),
        blank=True,null=True)
    state = PostingState.field()
    #~ sender = models.ForeignKey(settings.LINO.user_model)
    date = models.DateField()
    
    def save(self,*args,**kw):
        if not isinstance(self.owner,Postable):
            raise Exception("Controller of popsting must be a Postable.")
        super(Posting,self).save(*args,**kw)

    @dd.action(_("Print"))
    def print_action(self,ar):
        return self.owner.print_from_posting(self,ar)
    

class Postings(dd.Table):
    workflow_state_field = 'state'
    required_user_level = UserLevel.manager
    model = Posting
    column_names = 'date owner partner *'
    #~ @dd.action()
    
class PostingsByController(Postings):
    required_user_level = None
    master_key = 'owner'
    column_names = 'date partner state workflow_buttons *'
  
class PostingsByPartner(Postings):
    required_user_level = None
    master_key = 'partner'
    column_names = 'date owner *'
    
    
class CreatePostings(dd.RowAction):
    """
    Creates a new Posting for each recipient.
    """
  
    url_action_name = 'post'
    #~ label = _('Create email')
    label = _('Post')
    callable_from = None
    
    def run(self,elem,ar,**kw):
        recs = tuple(elem.get_postable_recipients())
        ar.confirm(
          _("Going to create %(num)d postings for %(elem)s") 
          % dict(num=len(recs),elem=elem))
        for p in recs:
            p = Posting(owner=elem,partner=p,date=datetime.date.today(),state=PostingState.new)
            p.full_clean()
            p.save()
        #~ js = rr.renderer.instance_handler(m)
        #~ url = rr.renderer.js2url(js)
        #~ kw.update(open_url=rr.renderer.get_detail_url(m))
        #~ kw.update(open_url=url)
        kw.update(refresh=True)
        return ar.success_response(**kw)
        
    
    
class Postable(models.Model):
    """
    Mixin for models that provide a "Post" button.
    """

    class Meta:
        abstract = True
        
    create_postings = CreatePostings()
    
    def print_from_posting(self,posting,ar):
        return ar.error_response("Not implemented")
        
    def get_postable_recipients(self):
        """return or yield a list of Partners"""
        return []
        
    


  

MODULE_LABEL = _("Outbox")
  
def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m  = m.add_menu("outbox",MODULE_LABEL)
    #~ m.add_action(MyInbox)
    m.add_action(MyOutbox)
    #~ m.add_action(MySent)
  
def setup_config_menu(site,ui,user,m):
    #~ if user.level >= UserLevel.manager:
    m  = m.add_menu("outbox",MODULE_LABEL)
    #~ m.add_action(MailTypes)
  
def setup_explorer_menu(site,ui,user,m):
    #~ if user.level >= UserLevel.manager:
    m  = m.add_menu("outbox",MODULE_LABEL)
    m.add_action(Mails)
  