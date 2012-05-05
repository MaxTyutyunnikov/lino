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
Lino-specific extensions to make the :term:`CBSS` 
connection visible.

"""

import os
import traceback
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from appy.shared.xml_parser import XmlUnmarshaller
from lxml import etree


from lino import mixins
from lino import dd

from lino.utils import babel
from lino.utils import dblogger
#~ from lino.tools import resolve_model
from lino.utils.xmlgen import cbss


from lino.utils.choicelists import ChoiceList
from lino.utils.choicelists import Gender
from lino.modlib.contacts import models as contacts
from lino.tools import makedirs_if_missing

WSDL_PARTS = ('cache','wsdl','cbss.wsdl')
ENVS = ('test', 'acpt', 'prod')

class RequestStatus(ChoiceList):
    """
    The status of a :class:`CBSSRequest` or :class:`SSDNRequest`.
    """
    label = _("Status")

add = RequestStatus.add_item
add('0',_("New"),alias='new')
add('1',_("Pending"),alias='pending')
add('2',_("Exception"),alias='exception')
add('3',_("OK"),alias='ok')
add('4',_("Warnings"),alias='warnings')
add('5',_("Errors"),alias='errors')
  

    
    


class SendAction(dd.RowAction):
    """
    This defines the "Execute" button on a 
    :class:`CBSSRequest` or
    :class:`SSDNRequest` 
    record.
    """
    name = 'sendcbss'
    label = _('Execute')
    #~ callable_from = None
    callable_from = (dd.GridEdit,dd.ShowDetailAction)
    
    def disabled_for(self,obj,request):
        if obj.sent:
            return True
    
    def run(self,rr,elem,**kw):
        elem.execute_request(rr)
        if elem.status == RequestStatus.warnings:
            kw.update(message=_("There were warnings but no errors."))
            kw.update(alert=True)
        kw.update(refresh=True)
        return rr.ui.success_response(**kw)


class SSDNRequest(mixins.ProjectRelated,mixins.AutoUser):
    """
    Abstract Base Class for Models that represent 
    SSDN ("classic") requests to the :term:`CBSS` (and responses).
    """
    
    cbss_namespace = NotImplementedError
    """
    Concrete subclasses must set this.
    """
    
    class Meta:
        abstract = True
        
    sent = models.DateTimeField(
        verbose_name=_("Sent"),
        blank=True,null=True,
        editable=False,
        help_text="""\
The date and time when this request has been executed. 
This is empty for requests than haven't been sent.
Read-only.""")
    
    status = RequestStatus.field(default=RequestStatus.new,editable=False)
    
    request_xml = models.TextField(verbose_name=_("Request"),
        editable=False,blank=True,
        help_text="""The raw XML string that has been (or will be) sent.""")
    
    response_xml = models.TextField(
        verbose_name=_("Response"),
        editable=False,blank=True,
        help_text="""\
The response received, raw XML string. 
If the request failed with a local exception, then it contains a traceback.""")
    
    def execute_request(self,rr):
        """
        This is the general method for all services,
        executed when a user runs :class:`SendAction`.
        """
        if not self.id:
            self.save()
        kw = self.get_request_params()
        try:
            #~ srvreq = self.cbss_namespace('ns1').build_request(**kw)
            srvreq = self.cbss_namespace.build_request(**kw)
        except cbss.Warning,e:
            self.status = RequestStatus.exception
            self.response_xml = unicode(e)
            self.save()
            return
            
        self.request_xml = etree.tostring(srvreq,pretty_print=True)
        self.status = RequestStatus.pending
        self.save()
        
        now = datetime.datetime.now()
        #~ if isinstance(self.cbss_namespace,cbss.NewStyleService):
            #~ up = settings.LINO.cbss2_user_params
        #~ elif isinstance(self.cbss_namespace,cbss.SSDNService):
            #~ up = settings.LINO.cbss_user_params
        #~ else:
            #~ raise Exception("Invalid cbss_namespace %r" % self.cbss_namespace)
            
        try:
            res = self.cbss_namespace.execute(
              settings.LINO.cbss_environment,
              srvreq,
              settings.LINO.cbss_user_params,
              str(self.id),now)
        except cbss.Warning,e:
            self.status = RequestStatus.exception
            self.response_xml = unicode(e)
            self.save()
            return
        except Exception,e:
            self.status = RequestStatus.exception
            self.response_xml = traceback.format_exc(e)
            self.save()
            return
        self.sent = now
        self.response_xml = res.data.xmlString
        reply = cbss.xml2reply(res.data.xmlString)
        rc = reply.ServiceReply.ResultSummary.ReturnCode
        if rc == '0':
            self.status = RequestStatus.ok
        elif rc == '1':
            self.status = RequestStatus.warnings
        elif rc == '10000':
            self.status = RequestStatus.errors
        self.save()
        
        if self.status != RequestStatus.ok:
            msg = '\n'.join(list(cbss.reply2lines(reply)))
            raise Exception(msg)
            
        self.on_cbss_ok(reply)
        
    def on_cbss_ok(self,reply):
        """
        Called when a successful reply has been received.
        """
        pass
        
    @classmethod
    def setup_report(cls,rpt):
        #~ call_optional_super(CBSSRequest,cls,'setup_report',rpt)
        rpt.add_action(SendAction())
        
    def __unicode__(self):
        return u"%s#%s" % (self.__class__.__name__,self.pk)
        
        
class CBSSRequest(mixins.ProjectRelated,mixins.AutoUser):
    """
    Abstract Base Class for Models that represent 
    requests to the :term:`CBSS` (and responses).
    """
    
    cbss_namespace = NotImplementedError
    """
    Concrete subclasses must set this.
    """
    
    class Meta:
        abstract = True
        
    sent = models.DateTimeField(
        verbose_name=_("Sent"),
        blank=True,null=True,
        editable=False,
        help_text="""\
The date and time when this request has been executed. 
This is empty for requests than haven't been sent.
Read-only.""")
    
    status = RequestStatus.field(default=RequestStatus.new,editable=False)
    
    request_xml = models.TextField(verbose_name=_("Request"),
        editable=False,blank=True,
        help_text="""The raw XML string that has been (or will be) sent.""")
    
    response_xml = models.TextField(
        verbose_name=_("Response"),
        editable=False,blank=True,
        help_text="""\
The response received, raw XML string. 
If the request failed with a local exception, then it contains a traceback.""")
    
    def execute_request(self,ar):
        """
        This is the general method for all services,
        executed when a user runs :class:`SendAction`.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        now = datetime.datetime.now()
        
        self.status = RequestStatus.pending
        self.save()
        
        url = ar.ui.media_url(*WSDL_PARTS)
        
        logger.info("Instantiate Client at %s", url)
        from suds.client import Client
        from suds.transport.http import HttpAuthenticated
        t = HttpAuthenticated(
            username=settings.LINO.username, 
            password=settings.LINO.password)
        client = Client(url, transport=t)
        #print client

        ci = client.factory.create('ns0:CustomerIdentificationType')
        cbeNumber = client.factory.create('ns0:CbeNumberType')
        ci.cbeNumber = settings.LINO.cbss_cbe_number
        ic = client.factory.create('ns0:InformationCustomerType')
        ic.ticket = str(self.id)
        ic.timestampSent = now
        ic.customerIdentification = ci

        si = client.factory.create('ns0:SearchInformationType')
        si.ssin = self.ssin 
        si.language = "fr"
        si.history = True

        
        try:
            res = client.service.retrieveTI(ic,None,si)        
        except cbss.Warning,e:
            self.status = RequestStatus.exception
            self.response_xml = unicode(e)
            self.save()
            return
        except Exception,e:
            self.status = RequestStatus.exception
            self.response_xml = traceback.format_exc(e)
            self.save()
            return
        self.sent = now
        self.response_xml = unicode(res)
        
        if False:
            reply = cbss.xml2reply(res.data.xmlString)
            rc = reply.ServiceReply.ResultSummary.ReturnCode
            if rc == '0':
                self.status = RequestStatus.ok
            elif rc == '1':
                self.status = RequestStatus.warnings
            elif rc == '10000':
                self.status = RequestStatus.errors
            self.save()
            
            if self.status != RequestStatus.ok:
                msg = '\n'.join(list(cbss.reply2lines(reply)))
                raise Exception(msg)
            
        self.on_cbss_ok(reply)
        
    def on_cbss_ok(self,reply):
        """
        Called when a successful reply has been received.
        """
        pass
        
    @classmethod
    def setup_report(cls,rpt):
        #~ call_optional_super(CBSSRequest,cls,'setup_report',rpt)
        rpt.add_action(SendAction())
        
    def __unicode__(self):
        return u"%s#%s" % (self.__class__.__name__,self.pk)
        
        
class IdentifyPersonRequest(SSDNRequest,contacts.PersonMixin,contacts.Born):
    """
    Represents a request to the :term:`CBSS` IdentifyPerson service.
    
    """
    
    cbss_namespace = cbss.IPR # IdentifyPersonRequest
    
    class Meta:
        verbose_name = _("IdentifyPerson Request")
        verbose_name_plural = _("IdentifyPerson Requests")
        
    national_id = models.CharField(max_length=200,
        blank=True,verbose_name=_("National ID")
        #~ ,validators=[niss_validator]
        )
        
    middle_name = models.CharField(max_length=200,
      blank=True,
      verbose_name=_('Middle name'),
      help_text="Whatever this means...")
    tolerance = models.IntegerField(verbose_name=_('Tolerance'),
      default=0,
      help_text=u"""
      Falls Monat oder Tag des Geburtsdatums unbekannt sind, 
      um wieviel Einheiten die Suche nach unten/oben ausgeweitet wird.
      Gültige Werte: 0 bis 10.
      <p>Zum Beispiel 
      <table border=1 class="htmlText">
      <tr>
        <td>Geburtsdatum<td/>
        <td colspan="3">Toleranz<td/>
      </tr><tr>
        <td><td/>
        <td>0<td/>
        <td>1</td>
        <td>10</td>
      </tr><tr>
        <td> 1968-00-00  <td/>
        <td> im Jahr 1968 <td/>
        <td> von 1967 bis 1969 </td>
        <td> 1958 bis 1978 <td/>
      </tr><tr>
        <td> 1968-06-00  <td/>
        <td> im Juni 1968 <td/>
        <td> von Mai  bis Juli 1968 </td>
        <td>von Oktober 1967 bis April 1969</td>
      </tr>
      </table>
      </p>
      """)
      
    def save(self,*args,**kw):
        if self.project: 
            person = self.project
            if person.national_id and not self.national_id:
                self.national_id = person.national_id
            if not self.last_name:
                self.last_name = person.last_name
            if not self.first_name:
                self.first_name = person.first_name
                
        super(IdentifyPersonRequest,self).save(*args,**kw)
        
    def get_request_params(self,**kw):
        """
        """
        national_id = self.national_id.replace('=','')
        national_id = national_id.replace(' ','')
        national_id = national_id.replace('-','')
        kw.update(national_id=national_id)
        kw.update(last_name=self.last_name)
        kw.update(first_name=self.first_name)
        kw.update(middle_name=self.middle_name)
        if self.birth_date is not None:
            kw.update(birth_date=str(self.birth_date))
        kw.update(tolerance=self.tolerance)
        if self.gender == Gender.male:
            kw.update(gender=1)
        elif self.gender == Gender.female:
            kw.update(gender=2)
        else:
            kw.update(gender=0)
        return kw
        
        #~ VD = cbss.ipr.VerificationData
        #~ SC = cbss.ipr.SearchCriteria
        #~ PC = cbss.ipr.PhoneticCriteria
        #~ if self.national_id:
            #~ return cbss.ipr.verify_request(
              #~ self.national_id,
              #~ LastName=self.last_name,
              #~ FirstName=self.first_name,
              #~ BirthDate=self.birth_date,
              #~ )
        #~ else:
          #~ pc = []
          #~ pc.append(cbss.ipr.LastName(self.last_name))
          #~ pc.append(cbss.ipr.FirstName(self.first_name))
          #~ pc.append(cbss.ipr.MiddleName(self.middle_name))
          #~ # if person.birth_date:
          #~ pc.append(cbss.ipr.BirthDate(self.birth_date))
          #~ if self.gender == Gender.male:
              #~ pc.append(cbss.ipr.Gender(1))
          #~ elif self.gender == Gender.female:
              #~ pc.append(cbss.ipr.Gender(2))
          #~ else:
              #~ pc.append(cbss.ipr.Gender(0))
          #~ pc.append(cbss.ipr.Tolerance(self.tolerance))
          #~ return cbss.ipr.IdentifyPersonRequest(SC(PC(*pc)))
    
dd.update_field(IdentifyPersonRequest,'first_name',blank=True)
dd.update_field(IdentifyPersonRequest,'last_name',blank=True)
#~ IdentifyPersonRequest._meta.get_field_by_name('first_name')[0].blank = True
#~ IdentifyPersonRequest._meta.get_field_by_name('last_name')[0].blank = True

class IdentifyPersonRequestDetail(dd.DetailLayout):
    box1 = """
    id project user sent status
    """
    box2 = """
    national_id
    spacer
    """
    box3 = """
    first_name middle_name last_name
    birth_date tolerance  gender 
    """
    
    box4 = """
    request_xml response_xml
    """
    
    main = """
    box1
    box2 box3
    box4
    """
    
    def setup_handle(self,lh):
        lh.box1.label = _("Request information")
        lh.box2.label = _("Using the national ID")
        lh.box3.label = _("Using phonetic search")
        lh.box4.label = _("Result")
    

class IdentifyPersonRequests(dd.Table):
    #~ window_size = (500,400)
    model = IdentifyPersonRequest
    detail_layout = IdentifyPersonRequestDetail()
    #~ detail_template = """
    #~ id project 
    #~ national_id
    #~ first_name middle_name last_name
    #~ birth_date tolerance  gender 
    #~ sent status 
    #~ request_xml
    #~ response_xml
    #~ """
    
    @dd.constant()
    def spacer(self,ui):  return '<br/>'
    
class IdentifyRequestsByPerson(IdentifyPersonRequests):
    master_key = 'project'
    
    
def setup_site_cache(self,mtime,force):
    """Called from :meth:`build_lino_js`. 
    First argment is the LINO instance."""
    
    import logging
    logger = logging.getLogger(__name__)
    
    cbss_environment = settings.LINO.cbss_environment
    if cbss_environment is None:
        return # silently return
        
    if not cbss_environment in ENVS:
        raise Exception("Invalid `cbss_environment` %r: must be one of %s." % (
          cbss_environment,ENVS))
    
    
    #~ makedirs_if_missing(os.path.join(settings.MEDIA_ROOT,*WSDL_PARTS[:-1]))
    fn = os.path.join(settings.MEDIA_ROOT,*WSDL_PARTS) 
    if not force and os.path.exists(fn):
        if os.stat(fn).st_mtime > mtime:
            logger.info("NOT generating %s because it is newer than the code.",fn)
            return
    s = file(os.path.join(os.path.dirname(__file__),'XSD','RetrieveTIGroupsV3.wsdl')).read()
    s = s % dict(cbss_environment=cbss_environment)
    makedirs_if_missing(os.path.dirname(fn))
    open(fn,'wt').write(s)
    logger.info("Generated %s for environment %r.",fn,cbss_environment)
    