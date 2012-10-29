How to migrate data
===================

Basic instructions
------------------

Here is how we suggest to 
:doc:`migrate existing data </topics/datamig>` 
using :doc:`/topics/dumpy`.

Go to your local directory::

  cd /use/local/django/mysite

Run the :srcref:`stop </bash/stop>` command (a bash script to shut down all 
application services)::

  ./stop
  
Create a dpy dump by invoking the :srcref:`dump </bash/dump>` script::

  ./dump
  
This will create a file :file:`dYYYMMDD.py` in your 
local `fixtures` directory (YYYYMMDD being the current date).
The script will refuse to overwrite an existing file. 
If you need more than one dump on the same day, 
then we suggest to rename the dYYYYMMDD.py to dYYYYMMDDa.py)
 
Now you can call :srcref:`pull </bash/pull>` to upgrade 
your local copy of the Lino source repository::

  ./pull
  
Then use Lino's :mod:`initdb <lino.management.commands.initdb>` 
command to flush the database and reload the dump::
  
  python manage.py initdb dYYYYMMDD
  
Restart application services using the :srcref:`start </bash/start>` 
command::
  
  ./start



The double dump test
-----------------------------------------------------

When :mod:`initdb <lino.management.commands.initdb>` 
successfully terminated without any warnings and error messages, 
then there are good chances 
that your database has been successfully migrated. 

But here is one more automated test that you may run 
when everything seems okay.

This so-called double dump test consists of the following steps:

- make another dump :file:`a.py` of the freshly migrated database 
- load this dump 
- make a third dump :file:`b.py` of your database 
- Compare the files :file:`a.py` and :file:`b.py`:
  if there's no difference, then the double dump test succeeded!


For example, here is a successful upgrade with data migration::
  
  $ python manage.py dumpdata --format py > fixtures/d20110931.py
  $ ./pull # update to new Lino version
  $ python manage.py initdb d20110931 --noinput
  INFO Lino initdb ('d20110901a',) started on database mysite.
  Creating tables ...
  Installing custom SQL ...
  Installing indexes ...
  (...)
  INFO Saved 29798 instances from /usr/local/django/mysite/fixtures/d20110901a.py.
  Installed 29798 object(s) from 1 fixture(s)
  INFO Lino initdb done ('d20110901a',) on database mysite.  
  $
  

Now run the additional test::  
  
  $ python manage.py dumpdata --format py > fixtures/a.py
  
  $ python manage.py initdb a --noinput
  INFO Lino initdb ('a',) started on database mysite.
  Creating tables ...
  Installing custom SQL ...
  Installing indexes ...
  (...)
  INFO Saved 29798 instances from /usr/local/django/mysite/fixtures/a.py.
  Installed 29798 object(s) from 1 fixture(s)
  INFO Lino initdb done ('a',) on database mysite.  
  
  $ python manage.py dumpdata --format py > fixtures/b.py
  
  $ diff fixtures/a.py fixtures/b.py
  
If there's no difference between the two dumps, then the test succeeded!
  
.. note:: 

  With versions before :doc:`/blog/2011/0901` there were still 
  differences if your database contained records with 
  `auto_now 
  <https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateField.auto_now>`_
  fields.
  
  
