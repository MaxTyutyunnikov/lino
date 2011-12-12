## Copyright 2011 Luc Saffre
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
Middleware to be used on sites with :doc:`/topics/http_auth`.

Code is partly taken from Django's
`django.contrib.auth.middleware`
and `django.middleware.locale` modules.


"""


import logging
logger = logging.getLogger(__name__)

from django.utils import translation
from django.conf import settings
#~ from django.utils.cache import patch_vary_headers

from lino.modlib.users.models import User
#~ from lino.utils import dblogger

class RemoteUserMiddleware(object):
    """
    This does the same as
    `django.contrib.auth.middleware.RemoteUserMiddleware`, 
    but in a simplified manner and without using Sessions.
    
    It also activates the User's language, if that field is not empty.
    Since it will run *after*
    `django.contrib.auth.middleware.RemoteUserMiddleware`
    (at least if you didn't change :meth:`lino.Lino.get_middleware_classes`),
    it will override any browser setting.
    
    The header used is configurable and defaults to ``REMOTE_USER``.  Subclass
    this class and change the ``header`` attribute if you need to use a
    different header.

    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = "REMOTE_USER"

    def process_request(self, request):
      
        #~ language = translation.get_language_from_request(request)
        #~ translation.activate(language)
        #~ request.LANGUAGE_CODE = translation.get_language()
        #~ from lino.utils import babel
        #~ if request.LANGUAGE_CODE == babel.DEFAULT_LANGUAGE:
            #~ print 'oops', request.path_info
      
        username = request.META.get(self.header,settings.LINO.default_user)
        if not username:
            raise Exception("No %s in %s" % (self.header,request.META))
            
        #~ try:
            #~ username = request.META[self.header]
        #~ except KeyError:
            #~ if True:
                #~ raise Exception("No %s in %s" % (self.header,request.META))
            #~ else:
                #~ logger.warning("No %s in %s",self.header,request.META)
                #~ request.user = None
                #~ # If specified header doesn't exist, set `user` to None
                #~ return
        try:
            request.user = User.objects.get(username=username)
        except User.DoesNotExist,e:
            u = User(username=username)
            u.full_clean()
            u.save()
            logger.info("Creating new user %s from request %s",u,request)
            request.user = u
        if request.user.language:
            translation.activate(request.user.language)
            request.LANGUAGE_CODE = translation.get_language()
            
    #~ def process_response(self, request, response):
        #~ language = translation.get_language()
        #~ translation.deactivate()
        #~ patch_vary_headers(response, ('Accept-Language',))
        #~ if 'Content-Language' not in response:
            #~ response['Content-Language'] = language
        #~ return response



class LocaleMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).
    """

    def process_request(self, request):
        language = translation.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        language = translation.get_language()
        translation.deactivate()
