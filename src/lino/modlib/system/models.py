## Copyright 2009 Luc Saffre
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

from django.contrib.auth import models as auth
from django.contrib.sessions import models as sessions
from django import forms
from django.db import models
from django.utils.translation import ugettext as _

from lino import reports
from lino import layouts
from lino.utils import perms


class Permissions(reports.Report):
    model = auth.Permission
    order_by = 'content_type__app_label codename'
  
class Users(reports.Report):
    model = auth.User
    order_by = "username"
    display_field = 'username'

class Groups(reports.Report):
    model = auth.Group
    order_by = "name"
    display_field = 'name'

class Sessions(reports.Report):
    model = sessions.Session
    display_field = 'session_key'



class PasswordReset(layouts.DialogLayout):
    width = 50
    title = _("Request Password Reset")
    email = models.EmailField(verbose_name=_("E-mail"), max_length=75)
    #form = PasswordResetForm
    main = """
    intro
    email
    ok cancel
    """
    intro = layouts.StaticText("""
    Please fill in you e-mail adress.
    We will then send you a mail with a new temporary password.
    """)
    
    

class LoginAction(reports.Action):
    label = _("Login")
    def run(self,context):
        redirect_to = request.REQUEST.get(redirect_field_name, '')
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                # Light security check -- make sure redirect_to isn't garbage.
                if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                    redirect_to = settings.LOGIN_REDIRECT_URL
                from django.contrib.auth import login
                login(request, form.get_user())
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                return HttpResponseRedirect(redirect_to)
            print "not valid"
        else:
            form = AuthenticationForm(request)
        request.session.set_test_cookie()
        if Site._meta.installed:
            current_site = Site.objects.get_current()
        else:
            current_site = RequestSite(request)
        context = self.context(request,
            title = _('Login'),
            form = form,
            redirect_field_name = redirect_to,
            site = current_site,
            site_name = current_site.name,
        )
        return render_to_response(template_name, context, 
            context_instance=RequestContext(request))
    

#from django.contrib.auth.forms import AuthenticationForm
class Login(layouts.DialogLayout):
    #width = 40
    #height = 12
    #form = AuthenticationForm
    username = models.CharField(verbose_name=_("Username"), max_length=75)    
    password = models.CharField(verbose_name=_("Password"), max_length=75)    
    main = """
    text
    username
    password
    cancel ok
    """
    ok = LoginAction
    text = layouts.StaticText("Please enter your username and password to authentificate.")
    


class Logout(layouts.DialogLayout):
    width = 50
    form = None
    


def add_auth_menu(lino):
    m = lino.add_menu("auth",_("~Authentificate"))
    m.add_action(Login(),can_view=perms.is_anonymous)
    m.add_action(Logout(),can_view=perms.is_authenticated)
    m.add_action(PasswordReset(),can_view=perms.is_authenticated)
