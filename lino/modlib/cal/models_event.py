# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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
Part of the :xfile:`models` module for the :mod:`lino.modlib.cal` app.

Defines the :class:`EventType` and :class:`Event` models and their tables.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import cgi
import datetime
import dateutil

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
#~ from django.utils.translation import string_concat
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.db.models import loading
from django.core import exceptions
from django.utils.importlib import import_module

from north import dbutils
from north.dbutils import dtosl


from lino import mixins
from lino import dd
#~ from lino.core import reports
from lino.core import actions
from lino.utils import AttrDict
from lino.utils import ONE_DAY
from lino.core import constants


from lino.modlib.cal.utils import (
    DurationUnits, Recurrencies, 
    setkw, dt2kw, 
    when_text, 
    Weekdays, AccessClasses, CalendarAction)
    
    
    
    
contacts = dd.resolve_app('contacts')
postings = dd.resolve_app('postings')
outbox = dd.resolve_app('outbox')


#~ from .models import StartedSummaryDescription
from .mixins import Ended
from .models import Component
from .models import Priority
from .mixins import RecurrenceSet, EventGenerator
from .mixins import UpdateReminders

from .models_calendar import Calendars
from .models_calendar import Subscription


#~ Membership = dd.resolve_model('users.Membership')
#~ Subscription = dd.resolve_model('cal.Subscription')


from .workflows import (
    TaskStates, EventStates, GuestStates)
    

class EventType(dd.BabelNamed,dd.Sequenced,dd.PrintableType,outbox.MailableType):
    """
    An EventType is a collection of events and tasks.
    """
    
    templates_group = 'cal/Event'
    
    class Meta:
        abstract = settings.SITE.is_abstract_model('cal.EventType')
        verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")
        ordering = ['seqno']
        
    #~ name = models.CharField(_("Name"),max_length=200)
    description = dd.RichTextField(_("Description"),blank=True,format='html')
    is_appointment = models.BooleanField(_("Event is an appointment"),default=True)
    all_rooms = models.BooleanField(_("Locks all rooms"),default=False)
    locks_user = models.BooleanField(_("Locks the user"),
        help_text=_("Lino won't not accept more than one locking event per user at the same time."),
        default=False)
    #~ is_default = models.BooleanField(
        #~ _("is default"),default=False)
    #~ is_private = models.BooleanField(
        #~ _("private"),default=False,help_text=_("""\
#~ Whether other users may subscribe to this EventType."""))
    start_date = models.DateField(
        verbose_name=_("Start date"),
        blank=True,null=True)
    event_label = dd.BabelCharField(_("Event label"), 
        max_length=200,blank=True,default=_("Appointment")) 
    
    #~ def full_clean(self,*args,**kw):
        #~ if not self.name:
            #~ if self.username:
                #~ self.name = self.username
            #~ elif self.user is None:
                #~ self.name = "Anonymous"
            #~ else:
                #~ self.name = self.user.get_full_name()
        #~ super(EventType,self).full_clean(*args,**kw)
        

    #~ def __unicode__(self):
        #~ return self.name
        
    #~ def color(self,request):
        #~ return settings.SITE.get_calendar_color(self,request)
    #~ color.return_type = models.IntegerField(_("Color"))
        
        
    
class EventTypes(dd.Table):
    help_text = _("""The list of Event Types defined on this system.
    An EventType is a list of events which have certain things in common,
    especially they are displayed in the same colour in the calendar panel""")
    required = dd.required(user_groups='office',user_level='manager')
    model = 'cal.EventType'
    column_names = "name build_method template *"
    
    detail_layout = """
    name 
    event_label
    # description
    start_date id 
    # type url_template username password
    build_method template email_template attach_to_email
    is_appointment all_rooms locks_user
    EventsByType 
    """

    insert_layout = dd.FormLayout("""
    name 
    event_label 
    """,window_size=(60,'auto'))

#~ def default_calendar(user):
    #~ """
    #~ Returns or creates the default calendar for the given user.
    #~ """
    #~ try:
        #~ return Calendar.objects.get(user=user,is_default=True)
    #~ except Calendar.DoesNotExist,e:
        #~ color = Calendar.objects.all().count() + 1
        #~ while color > 32:
            #~ color -= 32
        #~ cal = Calendar(user=user,is_default=True,color=color)
        #~ cal.full_clean()
        #~ cal.save()
        #~ logger.debug(u"Created default calendar for %s.",user)
        #~ return cal






#~ class EventType(mixins.PrintableType,outbox.MailableType,dd.BabelNamed):
    #~ """The type of an Event.
    #~ Determines which build method and template to be used for printing the event.
    #~ """
  
    #~ templates_group = 'cal/Event'
    
    #~ class Meta:
        #~ verbose_name = pgettext(u"cal",u"Event Type")
        #~ verbose_name_plural = pgettext(u"cal",u'Event Types')

#~ class EventTypes(dd.Table):
    #~ model = EventType
    #~ required = dict(user_groups='office')
    #~ column_names = 'name build_method template *'
    #~ detail_layout = """
    #~ id name
    #~ build_method template email_template attach_to_email
    #~ cal.EventsByType
    #~ """



    
    
#~ class AutoEvent(object):
    #~ def __init__(self,auto_id,user,date,subject,owner,start_time,end_time):
        #~ self.auto_id = auto_id
        #~ self.user = user
        #~ self.date = date
        #~ self.subject = subject
        #~ self.owner = owner
        #~ self.start_time = start_time
        #~ self.end_time = end_time
    
    

class RecurrentEvent(dd.BabelNamed,RecurrenceSet,EventGenerator):
    """
    An event that recurs at intervals.
    """
    
    class Meta:
        verbose_name = _("Recurrent Event")
        verbose_name_plural = _("Recurrent Events")
        
    event_type = models.ForeignKey('cal.EventType',blank=True,null=True)
    #~ summary = models.CharField(_("Summary"),max_length=200,blank=True) # iCal:SUMMARY
    description = dd.RichTextField(_("Description"),blank=True,format='html')
    
    #~ def on_create(self,ar):
        #~ super(RecurrentEvent,self).on_create(ar)
        #~ self.event_type = settings.SITE.site_config.holiday_event_type
   
    #~ def __unicode__(self):
        #~ return self.summary
        
    def update_cal_rset(self):
        return self
    def update_cal_from(self,ar):
        return self.start_date
        
    def update_cal_calendar(self):
        return self.event_type
        
    def update_cal_summary(self,i):
        return unicode(self)
        

class RecurrentEvents(dd.Table):
    """
    The list of all :class:`Recurrence Sets <RecurrenceSet>`.
    """
    model = 'cal.RecurrentEvent'
    required = dd.required(user_groups='office',user_level='manager')
    column_names = "name every_unit event_type *"
    auto_fit_column_widths = True
    
    insert_layout = """
    name
    user event_type
    """
    detail_layout = """
    id user event_type name 
    start_date start_time  end_date end_time
    max_events every_unit every 
    monday tuesday wednesday thursday friday saturday sunday
    description cal.EventsByController
    """
    



class ExtAllDayField(dd.VirtualField):
    """
    An editable virtual field needed for 
    communication with the Ext.ensible CalendarPanel
    because we consider the "all day" checkbox 
    equivalent to "empty start and end time fields".
    """
    
    editable = True
    
    def __init__(self,*args,**kw):
        dd.VirtualField.__init__(self,models.BooleanField(*args,**kw),None)
        
    def set_value_in_object(self,request,obj,value):
        if value:
            obj.end_time = None
            obj.start_time = None
        else:
            if not obj.start_time:
                obj.start_time = datetime.time(9,0,0)
            if not obj.end_time:
                obj.end_time = datetime.time(10,0,0)
        #~ obj.save()
        
    def value_from_object(self,obj,ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return (obj.start_time is None)
        
#~ from lino.modlib.workflows import models as workflows # Workflowable

#~ class Components(dd.Table):
#~ # class Components(dd.Table,workflows.Workflowable):
  
    #~ workflow_owner_field = 'user'    
    #~ workflow_state_field = 'state'
    
    #~ def disable_editing(self,request):
    #~ def get_row_permission(cls,row,user,action):
        #~ if row.rset: return False
        
    #~ @classmethod
    #~ def get_row_permission(cls,action,user,row):
        #~ if not action.readonly:
            #~ if row.user != user and user.level < UserLevel.manager: 
                #~ return False
        #~ if not super(Components,cls).get_row_permission(action,user,row):
            #~ return False
        #~ return True




#~ bases = (Component,Ended,mixins.TypedPrintable,outbox.Mailable, postings.Postable)
#~ class Event(*bases):
class Event(Component,Ended,
    mixins.TypedPrintable,
    outbox.Mailable, 
    postings.Postable):
    """
    A Calendar Event (french "Rendez-vous", german "Termin") 
    is a planned ("scheduled") lapse of time where something happens.
    """
    
    class Meta:
        abstract = settings.SITE.is_abstract_model('cal.Event')
        #~ abstract = True
        verbose_name = pgettext(u"cal",u"Event")
        verbose_name_plural = pgettext(u"cal",u"Events")
        
    event_type = models.ForeignKey('cal.EventType',blank=True,null=True)
        
    transparent = models.BooleanField(_("Transparent"),default=False,help_text=_("""\
Indicates that this Event shouldn't prevent other Events at the same time."""))
    #~ type = models.ForeignKey(EventType,null=True,blank=True)
    room = dd.ForeignKey('cal.Room',null=True,blank=True) # iCal:LOCATION
    priority = models.ForeignKey(Priority,null=True,blank=True)
    #~ priority = Priority.field(_("Priority"),blank=True) # iCal:PRIORITY
    state = EventStates.field(default=EventStates.suggested) # iCal:STATUS
    #~ status = models.ForeignKey(EventStatus,verbose_name=_("Status"),blank=True,null=True) # iCal:STATUS
    #~ duration = dd.FieldSet(_("Duration"),'duration_value duration_unit')
    #~ duration_value = models.IntegerField(_("Duration value"),null=True,blank=True) # iCal:DURATION
    #~ duration_unit = DurationUnit.field(_("Duration unit"),blank=True) # iCal:DURATION
    #~ repeat_value = models.IntegerField(_("Repeat every"),null=True,blank=True) # iCal:DURATION
    #~ repeat_unit = DurationUnit.field(verbose_name=_("Repeat every"),null=True,blank=True) # iCal:DURATION
    all_day = ExtAllDayField(_("all day"))
    #~ all_day = models.BooleanField(_("all day"),default=False)
    
    assigned_to = dd.ForeignKey(settings.SITE.user_model,
        verbose_name=_("Assigned to"),
        related_name="cal_events_assigned",
        blank=True,null=True
        )
        
    def has_conflicting_events(self):
        qs = self.get_conflicting_events()
        if qs is None: return False
        return qs.count() > 0
        
    #~ def conflicts_with_existing(self):
    def get_conflicting_events(self):
        """
        Return a QuerySet of Events that conflict with this one.
        Must work also when called on an unsaved instance.
        May return None to indicate an empty queryset.
        Applications may override this to add specific conditions.
        """
        if self.transparent: 
            return
        #~ return False
        #~ Event = dd.resolve_model('cal.Event')
        #~ ot = ContentType.objects.get_for_model(RecurrentEvent)
        qs = self.__class__.objects.filter(transparent=False)
        end_date = self.end_date or self.start_date
        flt = Q(start_date=self.start_date,end_date__isnull=True)
        flt |= Q(end_date__isnull=False,start_date__lte=self.start_date,end_date__gte=end_date)
        if end_date == self.start_date:
            if self.start_time and self.end_time:
                # the other starts before me and ends after i started
                c1 = Q(start_time__lte=self.start_time,end_time__gt=self.start_time)
                # the other ends after me and started before i ended
                c2 = Q(end_time__gte=self.end_time,start_time__lt=self.end_time)
                # the other is full day
                c3 = Q(end_time__isnull=True,start_time__isnull=True)
                flt &= (c1|c2|c3)
        qs = qs.filter(flt)
        if self.id is not None:  # don't conflict with myself
            qs = qs.exclude(id=self.id)
        if self.auto_type is not None:
            qs = qs.exclude(auto_type=self.auto_type,
                owner_id=self.owner_id,owner_type=self.owner_type)
        if self.room is not None:
            # other event in the same room
            c1 = Q(room=self.room)
            # other event locks all rooms (e.h. holidays)
            c2 = Q(event_type__all_rooms=True)
            qs = qs.filter(c1|c2)
        if self.user is not None:
            if self.event_type is not None:
                if self.event_type.locks_user:
                    #~ c1 = Q(event_type__locks_user=False)
                    #~ c2 = Q(user=self.user)
                    #~ qs = qs.filter(c1|c2)
                    qs = qs.filter(user=self.user,event_type__locks_user=True)
        #~ qs = Event.objects.filter(flt,owner_type=ot)
        #~ if we.start_date.month == 7:
            #~ print 20131011, self, we.start_date, qs.count()
        #~ print 20131025, qs.query
        return qs
    
    def is_fixed_state(self):
        return self.state.fixed
        #~ return self.state in EventStates.editable_states 

    def is_user_modified(self):
        return self.state != EventStates.suggested
        
        
    #~ def after_send_mail(self,mail,ar,kw):
        #~ if self.state == EventStates.assigned:
            #~ self.state = EventStates.notified
            #~ kw['message'] += '\n('  +_("Event %s has been marked *notified*.") % self + ')'
            #~ self.save()
            
    def save(self,*args,**kw):
        r = super(Event,self).save(*args,**kw)
        self.add_guests()
        #~ """
        #~ The following hack removes this event from the series of 
        #~ automatically generated events so that the Generator re-creates 
        #~ a new one.
        #~ """
        #~ if self.state == EventStates.cancelled:
            #~ self.auto_type = None
        return r
            
    def add_guests(self):
        """
        Decide whether it is time to add Guest instances for this event,
        and if yes, call :meth:`suggest_guests` to instantiate them.
        """
        #~ print "20130722 Event.save"
        #~ print "20130717 add_guests"
        if settings.SITE.loading_from_dump: return
        if not self.is_user_modified(): 
            #~ print "not is_user_modified"
            return
        if not self.state.edit_guests:
        #~ if not self.state in (EventStates.suggested, EventStates.draft):
        #~ if self.is_fixed_state(): 
            #~ print "is a fixed state"
            return 
        if self.guest_set.all().count() > 0: 
            #~ print "guest_set not empty"
            return
        for g in self.suggest_guests():
            g.save()
            #~ settings.SITE.modules.cal.Guest(event=self,partner=p).save()
            
    def suggest_guests(self):
        """
        Yield a list of Partner instances to be invited to this Event.
        This method is called when :meth:`add_guests` decided so.
        """
        return []
        
    def get_event_summary(event,ar):
        """
        How this event should be summarized in contexts 
        where possibly another user is looking 
        (i.e. currently in invitations of guests, or in the extensible calendar 
        panel).
        """
        #~ from django.utils.translation import ugettext as _
        s = event.summary
        if event.user != ar.get_user():
            if event.access_class == AccessClasses.show_busy:
                s = _("Busy")
            s = event.user.username + ': ' + unicode(s)
        elif settings.SITE.project_model is not None and event.project is not None:
            s += " " + unicode(_("with")) + " " + unicode(event.project)
        if event.state:
            s = ("(%s) " % unicode(event.state)) + s
        n = event.guest_set.all().count()
        if n:
            s = ("[%d] " % n) + s
        return s


        
            
    def before_ui_save(self,ar,**kw):
        """
        Mark the event as "user modified" by setting a default state.
        This is important because EventGenerators may not modify any user-modified Events.
        """
        #~ logger.info("20130528 before_ui_save")
        if self.state is EventStates.suggested:
            self.state = EventStates.draft
        return super(Event,self).before_ui_save(ar,**kw)
        
    def on_create(self,ar):
        self.event_type = ar.user.event_type or settings.SITE.site_config.default_event_type
        self.start_date = datetime.date.today()
        self.start_time = datetime.datetime.now().time()
        if self.assigned_to is None: # 20130722 e.g. CreateClientEvent sets it explicitly
            self.assigned_to = ar.subst_user
        super(Event,self).on_create(ar)
        
    #~ def on_create(self,ar):
        #~ self.start_date = datetime.date.today()
        #~ self.start_time = datetime.datetime.now().time()
        #~ # default user is almost the same as for UserAuthored
        #~ # but we take the *real* user, not the "working as"
        #~ if self.user_id is None:
            #~ u = ar.user
            #~ if u is not None:
                #~ self.user = u
        #~ super(Event,self).on_create(ar)
        
        
        
    def get_postable_recipients(self):
        """return or yield a list of Partners"""
        if settings.SITE.is_installed('contacts') and issubclass(settings.SITE.project_model,contacts.Partner):
            if self.project:
                yield self.project
        for g in self.guest_set.all():
            yield g.partner
        #~ if self.user.partner:
            #~ yield self.user.partner
        
    def get_mailable_type(self):  
        return self.event_type
        
    def get_mailable_recipients(self):
        if settings.SITE.is_installed('contacts') and issubclass(settings.SITE.project_model,contacts.Partner):
            if self.project:
                yield ('to',self.project)
        for g in self.guest_set.all():
            yield ('to',g.partner)
        if self.user.partner:
            yield ('cc',self.user.partner)
            
    #~ def get_mailable_body(self,ar):
        #~ return self.description
        
    def get_system_note_recipients(self,ar,silent):
        if self.user != ar.user:
            yield "%s <%s>" % (unicode(self.user),self.user.email)
        if silent:
            return
        for g in self.guest_set.all():
            if g.partner.email:
                yield "%s <%s>" % (unicode(g.partner),g.partner.email)
      
        
    @dd.displayfield(_("When"))
    def when_text(self,ar):
        assert ar is not None
        #~ print 20130802, ar.renderer
        #~ raise foo
        #~ txt = when_text(self.start_date)
        txt = when_text(self.start_date,self.start_time)
        #~ return txt
        #~ logger.info("20130802a when_text %r",txt)
        return ar.obj2html(self,txt)
        #~ try:
            #~ e = ar.obj2html(self,txt)
        #~ except Exception,e:
            #~ import traceback
            #~ traceback.print_exc(e)
        #~ logger.info("20130802b when_text %r",E.tostring(e))
        #~ return e

        
            
    @dd.displayfield(_("Link URL"))
    def url(self,ar): return 'foo'
    
    @dd.virtualfield(dd.DisplayField(_("Reminder")))
    def reminder(self,request): return False
    #~ reminder.return_type = dd.DisplayField(_("Reminder"))
    
    def get_calendar(self):
        """
        Returns the Calendar which contains this event,
        or None if no subscription is found.
        Needed for ext.ensible calendar panel.

        The default implementation returns None.
        Override this if your app uses Calendars.
        """
        #~ for sub in Subscription.objects.filter(user=ar.get_user()):
            #~ if sub.contains_event(self):
                #~ return sub
        return None
    
    
    @dd.virtualfield(models.ForeignKey('cal.Calendar'))
    def calendar(self,ar):
        return self.get_calendar()
        
    

    def get_print_language(self):
        if settings.SITE.project_model is not None and self.project:
            return self.project.get_print_language()
        return self.user.language
        
    @classmethod
    def get_default_table(cls):
        return OneEvent

    @classmethod
    def on_analyze(cls,lino):
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(cls,
            '''summary''')
            

dd.update_field(Event,'user',verbose_name=_("Responsible user"))


class EventDetail(dd.FormLayout):
    start = "start_date start_time"
    end = "end_date end_time"
    main = """
    event_type summary user assigned_to
    start end #all_day #duration state
    room priority access_class transparent #rset 
    owner created:20 modified:20  
    description
    GuestsByEvent outbox.MailsByController
    """
class EventInsert(EventDetail):
    main = """
    event_type summary 
    start end 
    room priority access_class transparent 
    """
    
#~ class NextDateAction(dd.ListAction):
    #~ label = _("Next")
    #~ # action_name = 'next'
    #~ default_format = ext_requests.URL_FORMAT_JSON
    
    #~ def setup_action_request(self,actor,ar):
        #~ # print "coucou"
        #~ # assert row is None
        #~ start_date = ar.param_values.start_date or datetime.date.today()
        #~ end_date = ar.param_values.end_date or start_date
        #~ ar.param_values.define('start_date',start_date + ONE_DAY)
        #~ ar.param_values.define('end_date',end_date + ONE_DAY)
        #~ # ar.param_values.end_date += ONE_DAY
        #~ # logger.info("20121203 cal.NextDateAction.setup_action_request() %s",ar.param_values)
        #~ # return ar.success_response(refresh=True)
    
    
class EventEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = EventEvents.add_item
add('10', _("Okay"),'okay')
add('20', _("Pending"),'pending')
    
    
#~ unclear_event_states = (EventStates.suggested,EventStates.draft,EventStates.notified)
#~ unclear_event_states = (EventStates.suggested,EventStates.draft)

class Events(dd.Table):
    help_text = _("A List of calendar entries. Each entry is called an event.")
    #~ debug_permissions = True
    model = 'cal.Event'
    required = dd.required(user_groups='office',user_level='manager')
    #~ column_names = 'start_date start_time user summary workflow_buttons calendar *'
    column_names = 'when_text:20 user summary event_type *'
    #~ column_names = 'start_date start_time user summary event_type *'
    
    hidden_columns = """
    priority access_class transparent
    owner created modified
    description
    sequence auto_type build_time owner owner_id owner_type 
    end_date end_time
    """
    
    #~ active_fields = ['all_day']
    order_by = ["start_date","start_time"]
    
    detail_layout = EventDetail()
    insert_layout = EventInsert()
    
    params_panel_hidden = True
    
    parameters = dd.ObservedPeriod(
        user = dd.ForeignKey(settings.SITE.user_model,
            verbose_name=_("Managed by"),
            blank=True,null=True,
            help_text=_("Only rows managed by this user.")),
        project = dd.ForeignKey(settings.SITE.project_model,
            blank=True,null=True),
        event_type = dd.ForeignKey('cal.EventType',blank=True,null=True),
        assigned_to = dd.ForeignKey(settings.SITE.user_model,
            verbose_name=_("Assigned to"),
            blank=True,null=True,
            help_text=_("Only events assigned to this user.")),
        state = EventStates.field(blank=True,
            help_text=_("Only rows having this state.")),
        #~ unclear = models.BooleanField(_("Unclear events"))
        observed_event = EventEvents.field(blank=True),
        show_appointments = dd.YesNo.field(_("Appointments"),blank=True),
    )
    
    params_layout = """
    start_date end_date observed_event state 
    user assigned_to project event_type show_appointments
    """
    #~ params_layout = dd.Panel("""
    #~ start_date end_date other
    #~ """,other="""
    #~ user 
    #~ assigned_to 
    #~ state
    #~ """)
    
    #~ next = NextDateAction() # doesn't yet work. 20121203
    
    fixed_states = set(EventStates.filter(fixed=True))
    #~ pending_states = set([es for es in EventStates if not es.fixed])
    pending_states = set(EventStates.filter(fixed=False))
    
    @classmethod
    def get_request_queryset(self,ar):
        #~ logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(Events,self).get_request_queryset(ar)
            
        if ar.param_values.user:
            #~ if ar.param_values.assigned_to:
                #~ qs = qs.filter(Q(assigned_to=ar.param_values.assigned_to)|Q(user=ar.param_values.user))
            #~ else:
            qs = qs.filter(user=ar.param_values.user)
        if ar.param_values.assigned_to:
            qs = qs.filter(assigned_to=ar.param_values.assigned_to)
            
        if settings.SITE.project_model is not None and ar.param_values.project:
            qs = qs.filter(project=ar.param_values.project)

        if ar.param_values.event_type:
            qs = qs.filter(event_type=ar.param_values.event_type)
        else:
            if ar.param_values.show_appointments == dd.YesNo.yes:
                qs = qs.filter(event_type__is_appointment=True)
            elif ar.param_values.show_appointments == dd.YesNo.no:
                qs = qs.filter(event_type__is_appointment=False)
                
        if ar.param_values.state:
            qs = qs.filter(state=ar.param_values.state)
            
        #~ if ar.param_values.observed_event:
        if ar.param_values.observed_event == EventEvents.okay:
            qs = qs.filter(state__in=self.fixed_states)
        elif ar.param_values.observed_event == EventEvents.pending:
            qs = qs.filter(state__in=self.pending_states)
            
            
        if ar.param_values.start_date:
            qs = qs.filter(start_date__gte=ar.param_values.start_date)
            #~ if ar.param_values.end_date:
                #~ qs = qs.filter(start_date__gte=ar.param_values.start_date)
            #~ else:
                #~ qs = qs.filter(start_date=ar.param_values.start_date)
        if ar.param_values.end_date:
            qs = qs.filter(start_date__lte=ar.param_values.end_date)
        return qs
        
    @classmethod
    def get_title_tags(self,ar):
        for t in super(Events,self).get_title_tags(ar):
            yield t
        if ar.param_values.start_date or ar.param_values.end_date:
            yield unicode(_("Dates %(min)s to %(max)s") % dict(
              min=ar.param_values.start_date or'...',
              max=ar.param_values.end_date or '...'))
              
        if ar.param_values.state:
            yield unicode(ar.param_values.state)
            
        if ar.param_values.user:
            yield unicode(ar.param_values.user)
            
        if settings.SITE.project_model is not None and ar.param_values.project:
            yield unicode(ar.param_values.project)
            
        if ar.param_values.assigned_to:
            yield unicode(self.parameters['assigned_to'].verbose_name) + ' ' + unicode(ar.param_values.assigned_to)

    @classmethod
    def apply_cell_format(self,ar,row,col,recno,td):
        """
        Enhance today by making background color a bit darker.
        """
        if row.start_date == datetime.date.today():
            td.attrib.update(bgcolor="#bbbbbb")
    
class EventsByType(Events):
    master_key = 'event_type'
    
#~ class EventsByType(Events):
    #~ master_key = 'type'
    
#~ class EventsByPartner(Events):
    #~ required = dd.required(user_groups='office')
    #~ master_key = 'user'
    
class EventsByRoom(Events):
    """
    Displays the :class:`Events <Event>` at a given :class:`Room`.
    """
    master_key = 'room'

class EventsByController(Events):
    required = dd.required(user_groups='office')
    master_key = 'owner'
    column_names = 'when_text:20 summary workflow_buttons *'
    auto_fit_column_widths = True

if settings.SITE.project_model:    
  
    class EventsByProject(Events):
        required = dd.required(user_groups='office')
        master_key = 'project'
        auto_fit_column_widths = True
        column_names = 'when_text user summary workflow_buttons'

class OneEvent(Events):
    show_detail_navigator = False
    use_as_default_table = False
    required = dd.required(user_groups='office')
    
if settings.SITE.user_model:    
  
    #~ class MyEvents(Events,mixins.ByUser):
    class MyEvents(Events):
        label = _("My events")
        help_text = _("Table of all my calendar events.")
        required = dd.required(user_groups='office')
        #~ column_names = 'start_date start_time event_type project summary workflow_buttons *'
        #~ column_names = 'when_text:20 event_type project summary *'
        column_names = 'when_text summary workflow_buttons project'
        
        @classmethod
        def param_defaults(self,ar,**kw):
            kw = super(MyEvents,self).param_defaults(ar,**kw)
            kw.update(user=ar.get_user())
            kw.update(show_appointments=dd.YesNo.yes)
            #~ kw.update(assigned_to=ar.get_user())
            #~ logger.info("20130807 %s %s",self,kw)
            kw.update(start_date=datetime.date.today())
            return kw
            
        @classmethod
        def create_instance(self,ar,**kw):
            kw.update(start_date=ar.param_values.start_date)
            return super(MyEvents,self).create_instance(ar,**kw)
            
        
        
    #~ class MyUnclearEvents(MyEvents):
        #~ label = _("My unclear events")
        #~ help_text = _("Events which probably need your attention.")
        #~ 
        #~ @classmethod
        #~ def param_defaults(self,ar,**kw):
            #~ kw = super(MyUnclearEvents,self).param_defaults(ar,**kw)
            #~ kw.update(observed_event=EventEvents.pending)
            #~ kw.update(start_date=datetime.date.today())
            #~ kw.update(end_date=datetime.date.today()+ONE_DAY)
            #~ return kw
        
    class MyAssignedEvents(MyEvents):
        label = _("Events assigned to me")
        help_text = _("Table of events assigned to me.")
        #~ master_key = 'assigned_to'
        required = dd.required(user_groups='office')
        #~ column_names = 'when_text:20 project summary workflow_buttons *'
        #~ known_values = dict(assigned_to=EventStates.assigned)
        
        @classmethod
        def param_defaults(self,ar,**kw):
            kw = super(MyAssignedEvents,self).param_defaults(ar,**kw)
            kw.update(user=None)
            kw.update(assigned_to=ar.get_user())
            return kw
        
    class unused_MyEventsToday(MyEvents):
        required = dd.required(user_groups='office')
        help_text = _("Table of my events per day.")
        column_names = 'when_text summary workflow_buttons project'
        label = _("My events today")
        #~ order_by = ['start_date', 'start_time']
        
        #~ @classmethod
        #~ def param_defaults(self,ar,**kw):
            #~ kw = super(MyEventsToday,self).param_defaults(ar,**kw)
            #~ today = datetime.date.today()
            #~ kw.update(start_date=today)
            #~ # kw.update(end_date=today)
            #~ # logger.info("20130807 %s %s",self,kw)
            #~ return kw
            
        #~ parameters = dict(
          #~ date = models.DateField(_("Date"),
          #~ blank=True,default=datetime.date.today),
        #~ )
        #~ @classmethod
        #~ def get_request_queryset(self,ar):
            #~ qs = super(MyEventsToday,self).get_request_queryset(ar)
            #~ return qs.filter(start_date=ar.param_values.date)
            
        #~ @classmethod
        #~ def create_instance(self,ar,**kw):
            #~ kw.update(start_date=ar.param_values.date)
            #~ return super(MyEventsToday,self).create_instance(ar,**kw)

        #~ @classmethod
        #~ def setup_request(self,rr):
            #~ rr.known_values = dict(start_date=datetime.date.today())
            #~ super(MyEventsToday,self).setup_request(rr)
            

      

class ExtDateTimeField(dd.VirtualField):
    """
    An editable virtual field needed for 
    communication with the Ext.ensible CalendarPanel
    because Lino uses two separate fields 
    `start_date` and `start_time`
    or `end_date` and `end_time` while CalendarPanel expects 
    and sends single DateTime values.
    """
    editable = True
    def __init__(self,name_prefix,alt_prefix,label):
        self.name_prefix = name_prefix
        self.alt_prefix = alt_prefix
        rt = models.DateTimeField(label)
        dd.VirtualField.__init__(self,rt,None)
    
    def set_value_in_object(self,request,obj,value):
        obj.set_datetime(self.name_prefix,value)
        
    def value_from_object(self,obj,ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return obj.get_datetime(self.name_prefix,self.alt_prefix)

class ExtSummaryField(dd.VirtualField):
    """
    An editable virtual field needed for 
    communication with the Ext.ensible CalendarPanel
    because we want a customized "virtual summary" 
    that includes the project name.
    """
    editable = True
    def __init__(self,label):
        rt = models.CharField(label)
        dd.VirtualField.__init__(self,rt,None)
        
    def set_value_in_object(self,request,obj,value):
        if obj.project:
            s = unicode(obj.project)
            if value.startswith(s):
                value = value[len(s):]
        obj.summary = value
        
    def value_from_object(self,obj,ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return obj.get_event_summary(ar)


#~ def user_calendars(qs,user):
    #~ subs = Subscription.objects.filter(user=user).values_list('calendar__id',flat=True)
    #~ return qs.filter(id__in=subs)

if settings.SITE.use_extensible:
  
    def parsedate(s):
        return datetime.date(*settings.SITE.parse_date(s))
  
    class CalendarPanel(dd.Frame):
        """
        Opens the "Calendar View" (a special window with the Ext.ensible CalendarAppPanel).
        """
        help_text = _("""Displays your events in a classical "calendar view", 
with the possibility to switch between daily, weekly, monthly view.""")
        required = dd.required(user_groups='office')
        label = _("Calendar")
        
        @classmethod
        def get_default_action(self):
            return CalendarAction()

    class PanelCalendars(Calendars):
        use_as_default_table = False
        required = dd.required(user_groups='office')
        #~ column_names = 'id name description color is_hidden'
        #~ column_names = 'id babel_name description color is_hidden'
        column_names = 'id summary description color is_hidden'
        
        @classmethod
        def get_request_queryset(self,ar):
            qs = super(PanelCalendars,self).get_request_queryset(ar)
            subs = Subscription.objects.filter(user=ar.get_user()).values_list('calendar__id',flat=True)
            return qs.filter(id__in=subs)
            
            #~ return qs.filter(user=ar.get_user())
            #~ for sub in Subscription.objects.filter(user=ar.get_user()):
                #~ qs = sub.add_events_filter(qs,ar)
            #~ return qs
            #~ return user_calendars(qs,ar.get_user())
            
        @dd.displayfield()
        def summary(cls,self,ar):
            #~ return dd.babelattr(self,'name')
            return unicode(self)
            
        @dd.virtualfield(models.BooleanField(_('Hidden')))
        def is_hidden(cls,self,ar):
            #~ return False
            #~ if self.user == ar.get_user():
                #~ return False
            try:
                sub = self.subscription_set.get(user=ar.get_user())
            except self.subscription_set.model.DoesNotExist as e:
                return False
            return sub.is_hidden

            
    class PanelEvents(Events):
        """
        The table used for Ext.ensible CalendarPanel.
        """
        required = dd.required(user_groups='office')
        use_as_default_table = False
        #~ parameters = dict(team_view=models.BooleanField(_("Team View")))
        
        #~ column_names = 'id start_dt end_dt summary description user room event_type #rset url all_day reminder'
        column_names = 'id start_dt end_dt summary description user room calendar #rset url all_day reminder'
        
        start_dt = ExtDateTimeField('start',None,_("Start"))
        end_dt = ExtDateTimeField('end','start',_("End"))
        
        summary = ExtSummaryField(_("Summary"))
        #~ overrides the database field of same name
        
      
        @classmethod
        def get_title_tags(self,ar):
            for t in super(PanelEvents,self).get_title_tags(ar):
                yield t
            if ar.subst_user:
                yield unicode(ar.subst_user)
                
        @classmethod
        def parse_req(self,request,rqdata,**kw):
            """
            Handle the request parameters issued by Ext.ensible CalendarPanel.
            """
            #~ filter = kw.get('filter',{})
            assert not kw.has_key('filter')
            fkw = {}
            #~ logger.info("20120118 filter is %r", filter)
            endDate = rqdata.get(constants.URL_PARAM_END_DATE,None)
            if endDate:
                d = parsedate(endDate)
                fkw.update(start_date__lte=d)
            startDate = rqdata.get(constants.URL_PARAM_START_DATE,None)
            if startDate:
                d = parsedate(startDate)
                #~ logger.info("startDate is %r", d)
                fkw.update(start_date__gte=d)
            #~ logger.info("20120118 filter is %r", filter)
            
            #~ subs = Subscription.objects.filter(user=request.user).values_list('calendar__id',flat=True)
            #~ filter.update(calendar__id__in=subs)
            
            flt = models.Q(**fkw)
            
            """
            If you override `parse_req`, then keep in mind that it will
            be called *before* Lino checks the requirements. 
            For example the user may be AnonymousUser even if 
            the requirements won't let it be executed.
            
            `request.subst_user.profile` may be None e.g. when called 
            from `find_appointment` in :ref:`welfare.pcsw.Clients`.
            """
            if not request.user.profile.authenticated: 
                raise exceptions.PermissionDenied(
                    _("As %s you have no permission to run this action.") % request.user.profile)
                
            # who am i ?
            me = request.subst_user or request.user
            
            # show all my events
            for_me = models.Q(user__isnull=True)
            for_me |= models.Q(user=me)
            
            # also show events to which i am invited
            if me.partner:
                #~ me_as_guest = Guest.objects.filter(partner=request.user.partner)
                #~ for_me = for_me | models.Q(guest_set__count__gt=0)
                #~ for_me = for_me | models.Q(guest_count__gt=0)
                for_me = for_me | models.Q(guest__partner=me.partner)
            
            if False:
                # in team view, show also events of all my team members
                tv = rqdata.get(constants.URL_PARAM_TEAM_VIEW,False)
                if tv and constants.parse_boolean(tv):
                    # positive list of ACLs for events of team members
                    team_classes = (None,AccessClasses.public,AccessClasses.show_busy)
                    my_teams = Membership.objects.filter(user=me)
                    we = settings.SITE.user_model.objects.filter(users_membership_set_by_user__team__in=my_teams)
                    #~ team_ids = Membership.objects.filter(user=me).values_list('watched_user__id',flat=True)
                    #~ for_me = for_me | models.Q(user__id__in=team_ids,access_class__in=team_classes)
                    for_me = for_me | models.Q(user__in=we,access_class__in=team_classes)
            flt = flt & for_me
            #~ logger.info('20120710 %s', flt)
            kw.update(filter=flt)
            #~ logger.info('20130808 %s %s', tv,me)
            return kw
            
        #~ @classmethod
        #~ def get_request_queryset(self,ar):
            #~ qs = super(PanelEvents,self).get_request_queryset(ar)
            #~ return qs
            
        @classmethod
        def create_instance(self,ar,**kw):
            obj = super(PanelEvents,self).create_instance(ar,**kw)
            if ar.current_project is not None:
                obj.project = settings.SITE.project_model.objects.get(pk=ar.current_project)
                #~ obj.state = EventStates.published
            return obj
            

if False:
    
    def reminders_as_html_old(ar,days_back=None,days_forward=None,**kw):
        s = '<div class="htmlText" style="margin:5px">%s</div>' % reminders_as_html(ar,days_back=None,days_forward=None,**kw)
        return s
        
    def reminders_as_html(ar,days_back=None,days_forward=None,**kw):
        """
        Return a HTML summary of all open reminders for this user.
        """
        user = ar.get_user()
        if not user.profile.authenticated: return ''
        today = datetime.date.today()
        
        past = {}
        future = {}
        def add(cmp):
            if cmp.start_date < today:
                lookup = past
            else:
                lookup = future
            day = lookup.get(cmp.start_date,None)
            if day is None:
                day = [cmp]
                lookup[cmp.start_date] = day
            else:
                day.append(cmp)
                
        flt = models.Q()
        if days_back is not None:
            flt = flt & models.Q(start_date__gte = today - datetime.timedelta(days=days_back))
        if days_forward is not None:
            flt = flt & models.Q(start_date__lte=today + datetime.timedelta(days=days_forward))
        
        events = ar.spawn(MyEvents,
            user=user,
            filter=flt & (models.Q(state=None) | models.Q(state__lte=EventStates.published)))
        tasks = ar.spawn(MyTasks,
            user=user,
            filter=flt & models.Q(state__in=[None,TaskStates.todo]))
        
        for o in events:
            o._detail_action = MyEvents.get_url_action('detail_action')
            add(o)
            
        for o in tasks:
            o._detail_action = MyTasks.get_url_action('detail_action')
            add(o)
            
        def loop(lookup,reverse):
            sorted_days = lookup.keys()
            sorted_days.sort()
            if reverse: 
                sorted_days.reverse()
            for day in sorted_days:
                #~ yield E.h3(dtosl(day))
                yield '<h3>'+dtosl(day) + '</h3>'
                yield dd.summary(ar,lookup[day],**kw)
                
        #~ if days_back is not None:
            #~ return loop(past,True)
        #~ else:
            #~ return loop(future,False)
            
        if days_back is not None:
            s = ''.join([chunk for chunk in loop(past,True)])
        else:
            s = ''.join([chunk for chunk in loop(future,False)])
            
        #~ s = '<div class="htmlText" style="margin:5px">%s</div>' % s
        return s
        
        
    settings.SITE.reminders_as_html = reminders_as_html
    
def update_reminders_for_user(user,ar):
    n = 0 
    for model in dd.models_by_base(EventGenerator):
        for obj in model.objects.filter(user=user):
            obj.update_reminders(ar)
            #~ logger.info("--> %s",unicode(obj))
            n += 1
    return n
      
      
        
        
class UpdateUserReminders(UpdateReminders):
    """
    Users can invoke this to re-generate their automatic tasks.
    """
    def run_from_ui(self,ar,**kw):
        user = ar.selected_rows[0]
        logger.info("Updating reminders for %s",unicode(user))
        n = update_reminders_for_user(user,ar)
        #~ ar.response.update(success=True)
        msg = _("%(num)d reminders for %(user)s have been updated."
          ) % dict(user=user,num=n)
        logger.info(msg)
        ar.success(msg,**kw)
        
@dd.receiver(dd.pre_analyze)
def pre_analyze(sender,**kw):
    #~ logger.info("%s.set_merge_actions()",__name__)
    #~ modules = sender.modules
    sender.user_model.add_model_action(update_reminders=UpdateUserReminders())
    
        
        

__all__ = [
    'UpdateReminders',
    'Event','Events',
    'CalendarPanel',
    #~ 'MyAssignedEvents',
    'EventType','EventTypes']

