About Lino
==========

A Lino application is technically just a Django project, 
but certain choices have been made for you.
For example the application developer does not need to write any 
URLconf, HTML, CSS nor Javascript.
A Lino application has an out-of-the box user interface.

Advantages: everything gets much easier: writing a prototype, 
changing database structures and business logic,
long-term maintenance, documentation...
Disadvantage: you are limited to applications that fit into this
out-of-the box user interface.

Technical details about the differences between Lino and Django 
are described in :doc:`lino_and_django`.


Features
--------
    
Because Lino applications are Django projects, 
the following features (copied from the 
`Django website <https://www.djangoproject.com/>`_) 
also apply to Lino:

- **Object-relational mapper** :
  Define your data models entirely in Python. 
  You get a rich, dynamic database-access API for free -- 
  but you can still write SQL if needed.
  
- **Internationalization** :
  Django has full support for multi-language applications, 
  letting you specify translation strings and providing 
  hooks for language-specific functionality.  

- **Cache system** :
  Hook into memcached or other cache frameworks for super performance 
  -- caching is as granular as you need.
  
Lino then adds its own features to the above:

- An out-of-the-box :doc:`user interface </topics/ui>`.
  Lino application developers don't waste their time writing html templates or css.

- :doc:`/topics/layouts` :  
  Design not only your *models* but also your *forms* using the Python language.
  
- Lino adds enterprise-level concepts for definining 
  :doc:`/topics/perms` and :doc:`/topics/workflow`.
  
- :ref:`mldbc` : 
  Use Lino's rich experience with applications that manage 
  multilingual database content.
  
- Use Lino's tools for generating :ref:`userdocs`.
  
- Lino includes :ref:`dpy`, 
  a great alternative to `South <http://south.aeracode.org/>`_
  to manage your :ref:`database migrations <datamig>`.
  
- Other features include extensions to handle
  :ref:`polymorphism`.
  


Components
----------

Lino consists of different parts which are currently in a single 
project, but that might change in the future:

- the framework itself. See :mod:`lino.dd` for an overview
  of the concepts.

- a collection of *user interface renderers*.
  Currently there's one for ExtJS 
  and another for a Twitter/Bootstrap-based "plain" interface.

- :ref:`modlib`, a collection of reusable Django apps and out-of-the-box 
  demo applications



Design goals
------------

- Lino applications are intuitive and easy-to-understand for the end user.
  (Context menus, Tooltips,...)
- agile programming
- rapid prototyping 
- libraries of reusable code
- short release cycles
- maintainable code
- stable 


History
-------

Luc Saffre, the author of Lino, is also the author of :term:`TIM`, 
a DOS-based framework for writing database applications for small enterprises. 
Lino is a successor for TIM.
TIM is over 15 years old, but Luc continues to live from maintaining 
it and giving professional support to its users. 
TIM users have relatively wide-spread profiles, 
ranging from the independant craftsman who writes 50 invoices per year 
to the government agency with 30 users and hundreds of documents per day.

Luc has been working on writing a successor for TIM **since the early 1990s**.
He has done and dropped projects in C++, PHP and Java. 
Since **August 2004** he's mostly working in Python. 
In **March 2009** he discovered :term:`Django` whose database model and application 
server concepts seem ideal for Lino. 
In **August 2009** he started to use the :term:`ExtJS` Javascript framework.

The first real-world Lino application started 
in a Belgian *Public Centre for Social Welfare* 
(PCSW) in **January 2011**.
In **August 2012** we forked it into a separate project 
`Lino-Welfare <http://welfare.lino-framework.org>`_
to be maintained by an independant organization.

In September 2012 we purchased the domain name `lino-framework.org`.

The second real-world Lino application started
:doc:`in Czechia <joe>` 
in **July 2013**.



More
----  
  
.. toctree::
   :maxdepth: 1
   
   testimonals
   faq
   luc
   license
   why_gpl
   values
   name
   
   lino_and_django
   thanks
   compared
   why_extjs
   ui

