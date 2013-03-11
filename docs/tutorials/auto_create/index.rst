lookup_or_create and the auto_create signal
===========================================

This document describes and tests the
:meth:`lookup_or_create <lino.core.model.Model.lookup_or_create>`
method and the 
:attr:`auto_create <lino.core.signals.auto_create>` signal.
I wrote it primarily to reproduce and test the 
"NameError / global name 'dd' is not defined"
on :doc:`/blog/2013/0311`.

We define a single simple model:

.. literalinclude:: models.py


.. djangodoctest:: tutorials.auto_create.settings

Create an empty database:

>>> call_command('initdb',interactive=False)
Creating tables ...
Creating table ui_siteconfig
Creating table auto_create_tag
Installing custom SQL ...
Installing indexes ...

Define a handler for the auto_create signal:

>>> from lino import dd
>>> @dd.receiver(dd.auto_create)
... def my_auto_create_handler(sender,**kw):
...    print_("My auto_create handler was called with",sender)

Manually create a Tag:

>>> Tag(name="Foo").save()

A first call to `lookup_or_create`:

>>> Tag.lookup_or_create("name","Foo")
Tag #1 (u'Foo')

The signal was not emitted here because the Foo tag existed before.

>>> print_(Tag.lookup_or_create("name","Bar"))
My auto_create handler was called with Bar
Bar
>>> print_(Tag.objects.all())
[Tag #1 (u'Foo'), Tag #2 (u'Bar')]

Voilà, that's all for the moment.
