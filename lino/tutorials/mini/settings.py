#~ from lino.apps.min1.settings import *
#~ from lino.apps.min2.settings import *
from lino.apps.presto.settings import *
class Lino(Lino):
    title = "mini tutorial"
    languages = ['en', 'de','fr']
    #~ languages = ['en']
    
LINO = Lino(__file__,globals()) 

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'test.db',
    }
}

LOGGING = dict(level='DEBUG')
#~ LOGGING = dict(filename=filename,level='DEBUG',rotate=False)  
#~ LOGGING = dict(filename=join(LINO.project_dir,'log',filename),level='DEBUG')
#~ LOGGING = dict(filename=join(LINO.project_dir,'log',filename),level='DEBUG')
import datetime
filename = datetime.date.today().strftime('%Y-%m-%d.log')
logdir = join(LINO.project_dir,'log')
import os
if os.path.exists(logdir):
    LOGGING.update(filename=join(logdir,filename))


EMAIL_HOST = "your.smtp.host"
SERVER_EMAIL = 'you@example.com'

# uncomment the following line for testing in memory database:
#~ DATABASES['default']['NAME'] = ':memory:'