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
from lino.core import actions

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
from lino.utils.choicelists import ChoiceList
#~ from lino.utils.perms import UserLevels
#~ from lino.utils.choosers import chooser


from Cheetah.Template import Template as CheetahTemplate
#~ from lino.utils import dtosl, dtos

uploads = dd.resolve_app("uploads")


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
    
    
from lino.utils.config import find_template_config_files

class MailableType(dd.Model):
  
    templates_group = None

    class Meta:
        abstract = True
        
    attach_to_email = models.BooleanField(_("Attach to email"),help_text="""\
Whether the printable file should be attached to the email
when creating an email from a mailable of this type.
""")
    #~ email_as_attachment = models.BooleanField(_("Email as attachment"))
    email_template = models.CharField(max_length=200,
      verbose_name=_("Email template"),
      blank=True,help_text="""\
The name of the file to be used as template 
when creating an email from a mailable of this type.
""")
    
    @dd.chooser(simple_values=True)
    def email_template_choices(cls):
        return find_template_config_files('.eml.html',cls.templates_group)
      
    


class CreateMailAction(dd.RowAction):
    """
    Creates an outbox mail and displays it.
    """
  
    url_action_name = 'mail'
    #~ label = _('Create email')
    #~ label = pgettext_lazy(u'verb',u'Mail')
    label = _('Create email')
    
    callable_from = (actions.GridEdit, 
        actions.ShowDetailAction,
        actions.ShowEmptyTable) # but not from InsertRow
    
    def get_action_permission(self,user,obj,state):
        """
        This action is not available:
        
        - when the user has not email address
        - on an obj whose MailableType is empty or has no :attr:`MailableType.email_template` configured
        """
        if not user.email:
            return False
        if obj is not None:
            mt = obj.get_mailable_type()
            if not mt or not mt.email_template:
                return False
            #~ if obj.attach_to_email(ar) and obj.get_target_name() is None:
            if mt.attach_to_email and not obj.get_target_name():
                return False
        return super(CreateMailAction,self).get_action_permission(user,obj,state)
        
    def run(self,elem,ar,**kw):
      
        as_attachment = elem.attach_to_email(ar)
        
        m = Mail(user=ar.get_user(),
            subject=elem.get_mailable_subject(),
            owner=elem)
        #~ if as_attachment:
        m.body = elem.get_mailable_intro(ar)
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
        
    
class Mailable(dd.Model):
    """
    Mixin for models that provide a "Post" button.
    A Mailable model must also inherit mixins.CachedPrintable (or mixins.TypedPrintable)
    """

    class Meta:
        abstract = True
        
    create_mail = CreateMailAction()
    #~ post2 = PostAction(True)
    
    #~ post_as_attachment = models.BooleanField(_("Post as attachment"),default=False)
        
        
    #~ def get_print_language(self,pm):
        #~ return babel.DEFAULT_LANGUAGE
        
    def get_mailable_type(self):  
        raise NotImplementedError()
        #~ return self.type
        
    def attach_to_email(self,ar):
        return self.get_mailable_type().attach_to_email
        #~ return isinstance(self,mixins.CachedPrintable)
        
    def get_mailable_intro(self,ar):
        mt = self.get_mailable_type()
        #~ tplname = self._meta.app_label + '/' + self.__class__.__name__ + '/email.html'
        fn = find_config_file(mt.email_template,mt.templates_group)
        if fn is None:
            raise Exception("No config file %s / %s" % (mt.templates_group,mt.email_template))
            #~ return ''
        #~ logger.info("Using email template %s",fn)
        tpl = CheetahTemplate(file(fn).read())
        #~ tpl.self = elem # doesn't work because Cheetah adds itself a name 'self' 
        tpl.instance = self
        tpl.dtosl = babel.dtosl
        tpl.dtos = babel.dtos
        return unicode(tpl)
        
    #~ def get_mailable_body(self,ar):
        #~ raise NoteImplementdError()
        
    def get_mailable_subject(self):
        """
        Return the content of the `subject` 
        field for the email to be created.
        """
        return unicode(self)
        

  
class Recipient(dd.Model):
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
        
    def get_row_permission(self,user,state,action):
        """
        Recipients of a Mail may not be edited if the Mail is read-only.
        """
        if self.mail_id and not self.mail.get_row_permission(user,state,action):
            return False
        return super(Recipient,self).get_row_permission(user,state,action)
      


class Recipients(dd.Table):
    required = dict(user_level='manager',user_groups='office')
    #~ required_user_level = UserLevels.manager
    model = Recipient
    #~ column_names = 'mail  type *'
    #~ order_by = ["address"]

class RecipientsByMail(Recipients):
    required = dict()
    #~ required_user_level = None
    master_key = 'mail'
    column_names = 'partner:20 address:20 name:20 type:10 *'
    #~ column_names = 'type owner_type owner_id'
    #~ column_names = 'type owner'



class SendMailAction(dd.RowAction):
    """
    Sends this as an email.
    """
  
    url_action_name = 'send'
    label = _('Send email')
    callable_from = None
            
    def get_action_permission(self,user,obj,state):
        if obj is not None and obj.sent:
            return False
        return super(SendMailAction,self).get_action_permission(user,obj,state)
        
    def run(self,elem,rr,**kw):
        #~ if elem.sent:
            #~ return rr.ui.error_response(message='Mail has already been sent.')
        #~ subject = elem.subject
        #~ sender = "%s <%s>" % (rr.get_user().get_full_name(),rr.get_user().email)
        sender = "%s <%s>" % (elem.user.get_full_name(),elem.user.email)
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
        #~ as_attachment = elem.owner.attach_to_email(rr)
        #~ body = elem.body
        #~ if as_attachment:
            #~ body = elem.body
        #~ else:
            #~ body = elem.owner.get_mailable_body(rr)
        text_content = html2text(elem.body)
        msg = EmailMultiAlternatives(subject=elem.subject, 
            from_email=sender,
            body=text_content, 
            to=to,bcc=bcc,cc=cc)
        msg.attach_alternative(elem.body, "text/html")
        for att in elem.attachment_set.all():
            #~ if as_attachment or att.owner != elem.owner:
            fn = att.owner.get_target_name()
            if fn is None:
                raise Warning(_("Couldn't find target file of %s") % att.owner)
            msg.attach_file(fn)
            
        for up in uploads.UploadsByController.request(master_instance=elem):
        #~ for up in uploads.Upload.objects.filter(owner=elem):
            fn = os.path.join(settings.MEDIA_ROOT,up.file.name)
            msg.attach_file(fn)
            
        num_sent = msg.send()
            
        elem.sent = datetime.datetime.now()
        elem.save()
        kw.update(refresh=True)
        #~ msg = "Email %s from %s has been sent to %s." % (
            #~ elem.id,elem.sender,', '.join([
                #~ r.address for r in elem.recipient_set.all()]))
        msg = _("Email %(id)s from %(sender)s has been sent to %(num)d recipients.") % dict(
            id=elem.id,sender=sender,num=num_sent)
        kw.update(message=msg,alert=True)
        #~ for n in """EMAIL_HOST SERVER_EMAIL EMAIL_USE_TLS EMAIL_BACKEND""".split():
            #~ msg += "\n" + n + " = " + unicode(getattr(settings,n))
        logger.info(msg)
        return rr.success_response(**kw)



#~ class Mail(mails.Mail,mixins.ProjectRelated,mixins.Controllable):
class Mail(mixins.AutoUser,mixins.Printable,mixins.ProjectRelated,mixins.Controllable):
  
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
        
    #~ sender = models.ForeignKey(settings.LINO.user_model,
        #~ verbose_name=_("Sender"))
        #~ related_name='outmails_by_sender',
        #~ blank=True,null=True)
    sent = models.DateTimeField(null=True,editable=False)

    #~ def disabled_fields(self,ar):
        #~ if not self.owner.post_as_attachment:
            #~ return ['body']
        #~ return []
        
    def get_print_language(self,bm):
        if self.user is not None:
            return self.user.language
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
        
    def get_row_permission(self,user,state,action):
        """
        Mails may not be edited after they have been sent.
        """
        if self.sent and not action.readonly:
            return False
        return super(Mail,self).get_row_permission(user,state,action)
      

#~ class MailDetail(dd.DetailLayout):
    #~ main = """
    #~ """

class Mails(dd.Table):
    #~ read_access = dd.required(user_level='manager')
    required = dict(user_level='manager',user_groups='office')
    model = Mail
    column_names = "sent recipients subject * body"
    order_by = ["sent"]
    detail_template = """
    subject project date 
    user sent #build_time id owner
    RecipientsByMail:50x5 AttachmentsByMail:20x5 uploads.UploadsByController:20x5
    body:90x10
    """
    
if not settings.LINO.project_model:
    Mails.detail_template.replace('project','')
    
    
class MyOutbox(Mails):
    required = dict()
    #~ required_user_level = None
    #~ known_values = dict(outgoing=True)
    label = _("My Outbox")
    #~ filter = models.Q(sent__isnull=True)
    master_key = 'user'
    
    @classmethod
    def setup_request(self,ar):
        if ar.master_instance is None:
            ar.master_instance = ar.get_user()
        #~ print "20120519 MyOutbox.setup_request()", ar.master_instance

#~ class MySent(MyOutbox):
    #~ label = _("Sent Mails")
    #~ filter = models.Q(sent__isnull=False)
    
class MailsByController(Mails):
    required = dict()
    master_key = 'owner'
    #~ label = _("Postings")
    #~ slave_grid_format = 'summary'

  
class MailsByUser(Mails):
    required = dict()
    label = _("Outbox")
    column_names = 'sent subject recipients'
    #~ order_by = ['sent']
    order_by = ['-date']
    master_key = 'user'

class MailsByProject(Mails):
    required = dict()
    label = _("Outbox")
    column_names = 'date subject recipients user *'
    #~ order_by = ['sent']
    order_by = ['-date']
    master_key = 'project'
    
class SentByPartner(Mails):
    required = dict()
    master = 'contacts.Partner'
    label = _("Outbox")
    column_names = 'sent subject user'
    order_by = ['sent']
    
    @classmethod
    def get_request_queryset(self,rr):
        q1 = Recipient.objects.filter(partner=rr.master_instance).values('mail').query
        qs = Mail.objects.filter(id__in=q1)
        qs = qs.order_by('sent')
        return qs

    
    

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
    required = dict(user_groups='office')
    #~ window_size = (400,500)
    #~ detail_template = """
    #~ mail owner
    #~ """
    
class AttachmentsByMail(Attachments):
    master_key = 'mail'
    slave_grid_format = 'summary'

class AttachmentsByController(Attachments):
    master_key = 'owner'




MODULE_LABEL = _("Outbox")
  
def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m  = m.add_menu("outbox",MODULE_LABEL)
    #~ m.add_action(MyInbox)
    m.add_action(MyOutbox)
    #~ m.add_action(MySent)
  
def setup_config_menu(site,ui,user,m):
    #~ if user.level >= UserLevels.manager:
    m  = m.add_menu("outbox",MODULE_LABEL)
    #~ m.add_action(MailTypes)
  
def setup_explorer_menu(site,ui,user,m):
    #~ if user.level >= UserLevels.manager:
    m  = m.add_menu("outbox",MODULE_LABEL)
    m.add_action(Mails)
  