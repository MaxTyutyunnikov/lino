from lino.ui import Site
SITE = Site(globals(),['lino.modlib.system','lino.modlib.users','tutorials.pisa'],
    languages=('en','de','fr'),
    user_model='users.User')
SECRET_KEY = "20227" # see :djangoticket:`20227`