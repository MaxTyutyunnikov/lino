from lino.projects.std.settings import Site
SITE = Site(globals(),'polls',title="Cool Polls")
# your local settings here
DEBUG = True
# DATABASES = ...
SECRET_KEY = 'abc123'

#~ SITE.anonymous_user_profile = '900'
