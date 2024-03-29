.. _lino.tutorial.dpy:


============================
Playing with Python fixtures
============================

Python fixtures are one of Lino's important features.
We suppose that you have read at least the beginning of
their documentation article :ref:`dpy`.
In this tutorial we are going to show how to use them.

The :mod:`initdb <djangosite.management.commands.initdb>` command
-----------------------------------------------------------------

Remember that we told you (in :ref:`lino.tutorial.quickstart`) 
to "prepare your database" by running the command::

  $ python manage.py initdb_demo
  
The :xfile:`manage.py` Python script is the standard Django interface 
for running a so-called management command.
I you don't know what *management commands* are, 
please read this:
`django-admin.py and manage.py 
<https://docs.djangoproject.com/en/dev/ref/django-admin/>`_.

The :mod:`initdb_demo <lino.management.commands.initdb_demo>` 
which we used here is a `custom management command 
<https://docs.djangoproject.com/en/dev/howto/custom-management-commands/>`_ 
provided by Lino.
It does nothing else than to call 
:mod:`initdb <djangosite.management.commands.initdb>`,
passing it a predefined set of fixture names, 
called the **demo fixtures**.

So the ``initdb_demo`` command above is equivalent to::
  
  $ python manage.py initdb std few_countries few_cities few_languages furniture demo demo2
  
The 
:mod:`initdb <djangosite.management.commands.initdb>` 
command 
performs three actions in one:

- a flush of your database, removing *all existing tables* 
  (not only Django tables)
  from the database specified in your :xfile:`settings.py`,
 
- then runs Django's `syncdb` command to re-create all tables,

- and finally runs Django's `loaddata` command to load 
  the specified fixtures.

Removing all existing tables
may sound dangerous, but that's what we want when we have a 
:doc:`Python dump </topics/dumpy>` to restore our database.
Keep in mind that you should rather not let 
Lino and some other application share the same database.

So the above line is roughly equivalent to::

  $ python manage.py flush
  $ python manage.py syncdb
  $ python manage.py loaddata std all_countries few_cities all_languages props demo 
  
Have a look at the following fixture files

- :srcref:`few_countries </lino/modlib/countries/fixtures/few_countries.py>`
  and :srcref:`all_countries </lino/modlib/countries/fixtures/all_countries.py>`

- :srcref:`few_languages </lino/modlib/countries/fixtures/few_languages.py>`
  and :srcref:`all_languages </lino/modlib/countries/fixtures/all_languages.py>`

- :srcref:`few_cities </lino/modlib/countries/fixtures/few_cities.py>`
  and :srcref:`be </lino/modlib/countries/fixtures/be.py>`.

Play with them::

  python manage.py initdb std all_countries be few_languages props demo 
  python manage.py initdb std few_languages few_countries few_cities demo 
  ...



Writing your own fixture
------------------------

Create a directory `fixtures` in your local project directory::

   mkdir ~/mypy/mysite/fixtures
   
Create a file `dumpy1.py` in that directory as the following.
But put your real name and data, this is your local file.

.. literalinclude:: dumpy1.py
    :linenos:
    
   
Try to apply this fixture::    

  $ python manage.py initdb dumpy1
  Gonna flush your database (myproject).
  Are you sure (y/n) ?y
  INFO Lino initdb ('dumpy1',) started on database myproject.
  INFO Lino version 1.1.11 using Python 2.7.1, Django 1.4 pre-alpha SVN-16280, 
  python-dateutil 1.4.1, Cheetah 2.4.4, docutils 0.7, PyYaml 3.08, 
  pyratemp (not installed), xhtml2pdf 3.0.32, ReportLab Toolkit 2.4, 
  appy.pod 0.6.6 (2011/04/26 20:50)
  No fixtures found.
  INFO Saved 2 instances from t:\hgwork\lino\docs\tutorials\dumpy1.py.
  Installed 1 object(s) from 1 fixture(s)
  INFO Lino initdb done ('dumpy1',) on database t:\data\luc\lino\dsbe\dsbe_test.db.


Second step
-----------

Since `.py` fixtures are normal Python modules, there are 
no limits to our phantasy when creating new objects.

A first thing that drops into mind is: there should be a more compact 
way to create many records of a same table. That's why 
:class:`lino.utils.instantiator.Instantiator` was written.
Here is the same fixture in a more compact way:

.. literalinclude:: dumpy2.py
    :linenos:


Third step
----------

Play around and try to add some more objects to your local demo database!


The default demo fixtures
-------------------------

The :ref:`cosi` application developer had decided that a 
demo site should by default load just *this* set of fixtures.
How did he do that?
Look at the source code of  
:srcref:`/lino/projects/cosi/settings/__init__.py`
where he overrides the 
:attr:`demo_fixtures <lino.site.Site.demo_fixtures>` 
attribute of his :class:`Site <lino.projects.cosi.settings.Site>` 
class, setting it to::

    demo_fixtures = 'std few_countries few_cities few_languages furniture demo demo2'.split()


Conclusion
----------

Python fixtures are an important tool for application developers
because 

- they are more flexible than json or xml fixtures and easy to adapt 
  when your database structure changes.
  
- they provide a simple interface to deploy demo data for an aplication


Where to go now
---------------

Now we suggest that your continue to read
:ref:`lino.tutorial.polls`
