.. _lino.tutorial.quickstart:

===============
Getting started
===============

Installation
------------

Note that Lino doesn't yet run under Python3, you need Python 2.7 or 2.6.  

The easiest way is to simply type::

  pip install lino

If this works, then you can skip to the next section.

It may take some time because Lino uses a lot of other Python packages 
which pip must possibly download.

If you didn't yet have `pip <http://www.pip-installer.org/en/latest/>`_, 
run `sudo aptitude install python-pip`.
If you cannot or don't want to perform system-wide installs, 
use `virtualenv <https://pypi.python.org/pypi/virtualenv>`_.

Another possibility is to install a development version of Lino 
and its related projects, as described in :ref:`lino.dev.install`.

  
Start your project
------------------

We begin by creating a plain empty Django project::

  $ cd
  $ django-admin startproject mysite
  
If the above command is new to you, then we recommend 
you to follow the 
:ref:`Lino Polls tutorial <lino.tutorial.polls>` 
before continuing this one.

Now open the
:xfile:`settings.py` file of your new project
and replace its content with the following:

.. literalinclude:: settings.py
    :linenos:

Explanations:

#.  The Python way to specify  encoding
    (:pep:`263`).
    That's needed because of the non-ascii **ì** in "Lino Così" 
    in line 3.
    
#.  We import settings from Lino Così, 
    one of the :ref:`out-of-the-box projects <lino.projects>` included with Lino.
    
#.  Then we define a :setting:`SITE` setting, 
    an instance of the :class:`Site <lino.site.Site>` class,
    passing our 
    :func:`globals` as first argument. 
    This will set default values 
    for all required Django settings
    (e.g. :setting:`DATABASES` and :setting:`LOGGING`).
    
#.  With one exception: 
    Django wants system admins to define their own 
    `SECRET_KEY <https://docs.djangoproject.com/en/dev/ref/settings/#secret-key>`__ 
    setting, so Lino doesn't dare to set a default value for this. 
    Hint: as long as you're on a development server you just put some 
    non-empty string and that's okay.

You might add ``DEBUG = True`` or other settings of your choice.

The basic idea is to keep local :xfile:`settings.py` files 
small and to delegate the responsibility of maintaining
default values for Django settings to the application developer.

In case you think already now about how to host many different Lino 
applications on your server, then read also about 
the :ref:`djangosite_local.py <djangosite_local>` file, 
another technique which Lino adds to plain Django.


Initial data
------------

Next we create your database and populate it with some demo content.
This is just one command to type::

  $ python manage.py initdb_demo

That is, you run the :mod:`initdb_demo <lino.management.commands.initdb_demo>`
management command that comes with every Lino application.
It will ask you::

  INFO Started manage.py initdb_demo (using mysite.settings) --> PID 3848
  INFO This is Lino Così 0.1 using Python 2.7.3, Django 1.4.5, django-site 0.0.2, North 0.0.2, Lino 1.6.0, Jinja 2.6, Sphinx 1.1.3, python-dat
  eutil 2.1, OdfPy ODFPY/0.9.6, docutils 0.10, suds 0.4, PyYaml 3.10, Appy 0.8.3 (2013/02/22 15:29).
  INFO Languages: en, de, fr. 16 apps, 37 models, 93 actors.
  We are going to flush your database (/home/luc/mysite/mysite/default.db).
  Are you sure (y/n) ?

If you answer "y" here, then
Lino will delete everything in the given database file
and replace it with its "factory default" demo data.
That's what you want, don't you? So go on and type ``y``::

  Creating tables ...
  Creating table ui_siteconfig
  ...
  Installing custom SQL ...
  Installing indexes ...
  INFO Loading /home/luc/hgwork/lino/lino/ui/fixtures/std.py...
  ...
  INFO Loading /home/luc/hgwork/lino/lino/projects/cosi/fixtures/userman.py...
  Installed 361 object(s) from 14 fixture(s)
  INFO Stopped manage.py initdb_demo (PID 3780)  


There's a lot to say about what we just did.
Lino applications use to make abundant use of :ref:`dpy` 
in order to have a rich set of "demo data".
If you are curious, then read more about Python fixtures in
:ref:`lino.tutorial.dpy`.



Start the web server
--------------------

Now you can start the development server::

  $ python manage.py runserver
  
which should output something like::  
  
  Validating models...
  0 errors found
  Django version 1.4.5, using settings 'mysite.settings'
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CTRL-BREAK.

And then point our web browser to http://127.0.0.1:8000/.
This produces the same result as 
the `online demo of Lino Così 
<http://demo4.lino-framework.org/>`__.

.. image:: quickstart.jpg
  :scale: 80

Congratulations for having installed your first Lino application.

Note what the development server does when the first web request arrives::

  INFO Checking /media URLs
  INFO Building /home/luc/mysite/mysite/media/cache/js/lino_000_de.js ...
  [27/Feb/2013 10:42:36] "GET / HTTP/1.1" 200 4465
  [27/Feb/2013 10:42:40] "GET /media/cache/js/lino_000_de.js HTTP/1.1" 200 198655


