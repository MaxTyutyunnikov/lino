# -*- coding: UTF-8 -*-
"""
This is a `Python dump <http://lino-framework.org/topics/dumpy.html>`_.
"""
from __future__ import unicode_literals
SOURCE_VERSION = '1.5.8'
from decimal import Decimal
from datetime import datetime as dt
from datetime import time,date
from lino.utils import babel
from lino.utils.mti import create_child
from lino.dd import resolve_model
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

            
def new_content_type_id(m):
    if m is None: return m
    # if not fmn: return None
    # m = resolve_model(fmn)
    ct = ContentType.objects.get_for_model(m)
    if ct is None: return None
    return ct.pk
    

def bv2kw(fieldname,values):
    """
    Needed if `lino.Lino.languages` changed between dumpdata and loaddata
    """
    return babel.babel_values(fieldname,en=values[0])
    
admin_LogEntry = resolve_model("admin.LogEntry")
auth_Group = resolve_model("auth.Group")
auth_Permission = resolve_model("auth.Permission")
auth_User = resolve_model("auth.User")
contenttypes_ContentType = resolve_model("contenttypes.ContentType")
polls_Choice = resolve_model("polls.Choice")
polls_Poll = resolve_model("polls.Poll")
sessions_Session = resolve_model("sessions.Session")
sites_Site = resolve_model("sites.Site")

def create_django_admin_log(id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message):
    kw = dict()
    kw.update(id=id)
    kw.update(action_time=action_time)
    kw.update(user_id=user_id)
    content_type_id = new_content_type_id(content_type_id)
    kw.update(content_type_id=content_type_id)
    kw.update(object_id=object_id)
    kw.update(object_repr=object_repr)
    kw.update(action_flag=action_flag)
    kw.update(change_message=change_message)
    return admin_LogEntry(**kw)

def create_auth_group(id, name):
    kw = dict()
    kw.update(id=id)
    kw.update(name=name)
    return auth_Group(**kw)

def create_auth_permission(id, name, content_type_id, codename):
    kw = dict()
    kw.update(id=id)
    kw.update(name=name)
    content_type_id = new_content_type_id(content_type_id)
    kw.update(content_type_id=content_type_id)
    kw.update(codename=codename)
    return auth_Permission(**kw)

def create_auth_user(id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined):
    kw = dict()
    kw.update(id=id)
    kw.update(username=username)
    kw.update(first_name=first_name)
    kw.update(last_name=last_name)
    kw.update(email=email)
    kw.update(password=password)
    kw.update(is_staff=is_staff)
    kw.update(is_active=is_active)
    kw.update(is_superuser=is_superuser)
    kw.update(last_login=last_login)
    kw.update(date_joined=date_joined)
    return auth_User(**kw)

def create_django_content_type(id, name, app_label, model):
    kw = dict()
    kw.update(id=id)
    kw.update(name=name)
    kw.update(app_label=app_label)
    kw.update(model=model)
    return contenttypes_ContentType(**kw)

def create_polls_choice(id, poll_id, choice_text, votes):
    kw = dict()
    kw.update(id=id)
    kw.update(poll_id=poll_id)
    kw.update(choice_text=choice_text)
    kw.update(votes=votes)
    return polls_Choice(**kw)

def create_polls_poll(id, question, pub_date):
    kw = dict()
    kw.update(id=id)
    kw.update(question=question)
    kw.update(pub_date=pub_date)
    return polls_Poll(**kw)

def create_django_session(session_key, session_data, expire_date):
    kw = dict()
    kw.update(session_key=session_key)
    kw.update(session_data=session_data)
    kw.update(expire_date=expire_date)
    return sessions_Session(**kw)

def create_django_site(id, domain, name):
    kw = dict()
    kw.update(id=id)
    kw.update(domain=domain)
    kw.update(name=name)
    return sites_Site(**kw)



def polls_poll_objects():
    yield create_polls_poll(1,u'What is your preferred colour?',dt(2013,2,9,0,0,0))
    yield create_polls_poll(2,u'Do you like Django?',dt(2013,2,9,0,0,0))
    yield create_polls_poll(3,u'Do you like ExtJS?',dt(2013,2,9,0,0,0))

def polls_choice_objects():
    yield create_polls_choice(1,1,u'Blue',0)
    yield create_polls_choice(2,1,u'Red',0)
    yield create_polls_choice(3,1,u'Yellow',0)
    yield create_polls_choice(4,1,u'other',0)
    yield create_polls_choice(5,2,u'Yes',0)
    yield create_polls_choice(6,2,u'No',0)
    yield create_polls_choice(7,2,u'Not yet decided',0)
    yield create_polls_choice(8,3,u'Yes',0)
    yield create_polls_choice(9,3,u'No',0)
    yield create_polls_choice(10,3,u'Not yet decided',0)

def auth_user_objects():
    yield create_auth_user(1,u'root',u'',u'',u'root@example.com',u'pbkdf2_sha256$10000$DFEG51doF0oP$ohs0NG2XFJcRZgVKrVUrQxgQ00Oinxs5kc3h9Lxvcx8=',True,True,True,dt(2013,2,9,5,9,10),dt(2013,2,9,5,9,10))


def objects():
    yield polls_poll_objects()
    yield polls_choice_objects()
    yield auth_user_objects()

settings.LINO.loading_from_dump = True

settings.LINO.install_migrations(globals())
