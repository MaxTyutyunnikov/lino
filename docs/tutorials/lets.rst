A Local Exchange Trade System
=============================

This tutorial supposes that you followed :doc:`t1`.

In this tutorial we are going to leave Django's 
polls and write a new application.
It is an application to manage a 
Local Exchange Trade System 
(`LETS <http://en.wikipedia.org/wiki/Local_exchange_trading_system>`_),
inspired by a real web site http://www.elavtoit.com

After having interviewed your future customer and analyzed their 
needs, you want to show a "first draft" prototype.
The goal of such a prototype is to have something 
to show to your customer that looks a little bit like 
the final product, and with wich you can play to test 
whether your analysis of the database structure is okay.

The code for such a first draft is in :srcref:`/lino/tutorials/lets1`.

Please explore these files and and copy 
them to a local project directory 
(e,g, :file:`c:\\mypy\\t3a`).
The directory structure should be as follows::

  __init__.py
  settings.py
  manage.py
  lets/__init__.py
  lets/models.py
  fixtures/__init__.py
  fixtures/demo.py

To get the prototype running, first run the following command 
to populate your database with some demo data::

  python manage.py initdb demo
  
Then start the development web server using::

  python manage.py runserver

And point your browser to http://127.0.0.1:8000/

Here are some screenshots.

.. image:: t3a-1.jpg
    :scale: 70
    
.. image:: t3a-2.jpg
    :scale: 70
    
.. image:: t3a-3.jpg
    :scale: 70

That's all for today, except that we ask you to send your questions 
so we can continue to write tutorials.