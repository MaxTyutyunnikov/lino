.. _lino.tutorial.human:

About Humans
============

This test application explains some basic truths about humans.

The database structure used for the following examples is very simple,
we define a single model `Person` 
which just inherits :class:`lino.mixins.human.Human`:

.. literalinclude:: models.py


.. 
  >>> from tutorials.human.models import Person


Overview
---------

Lino is not complicated. Humans have three properties: 
`first_name`, `last_name` and `gender`.
All these fields may be blank,
except if your application changed that rule
using :func:`dd.update_field <lino.core.inject.update_field>`.


Genders
-------

The :class:`Genders <lino.core.choicelists.Genders>` choicelist
defines the possible values for the `gender` field of a Human.

>>> from lino.dd import Genders
>>> [g.value for g in Genders.objects()]
['M', 'F']
>>> [unicode(g) for g in Genders.objects()]
[u'Male', u'Female']

The default `__unicode__` method of a Human includes 
the "salutation" which indicates the gender:

>>> print Person(first_name="John", last_name="Smith",gender=Genders.male)
Mr John Smith

>>> print Person(last_name="Smith",gender=Genders.female)
Mrs Smith

If you don't specify a gender, Lino doesn't print any salutation:

>>> print Person(first_name="John", last_name="Smith")
John Smith

>>> print Person(first_name="John")
John

The salutation depends not only on the gender, but also on the 
current language.
This is Mr Jean Dupont:

>>> p = Person(first_name="Jean",last_name="Dupont",gender=Genders.male)

We can address him in English:

>>> print p
Mr Jean Dupont

The same object will render differently when we switch to French...

>>> from north.dbutils import set_language
>>> set_language('fr')
>>> print p
M. Jean Dupont

... or to German...

>>> set_language('de')
>>> print p
Herrn Jean Dupont


Switch back to English:

>>> set_language(None)


The full name
-------------

Calling `unicode` on a person actually returns the same as the property `full_name`:

>>> print p
Mr Jean Dupont

>>> print p.full_name
Mr Jean Dupont

They are equivalent *here*, but remember that applications may override 
one of them (usually `__unicode__`) because in reality not all humans 
are equal. 

>>> print p.get_full_name()
Mr Jean Dupont

The :func:`get_full_name <lino.modlib.contacts.models.Person.get_full_name>` 
function has 2 optional parameters `nominative` and `salutation`.

In German you may need to get a nominative form of the salutation:

>>> set_language('de')

>>> print p.get_full_name(nominative=True)
Herr Jean Dupont

You may want to omit the salutation:

>>> print p.get_full_name(salutation=False)
Jean Dupont

The property `full_name` (without parentheses) of Person 
is an alias for the function call `get_full_name()` without parameters.

>>> print p.full_name
Herrn Jean Dupont





Uppercase last name
-------------------

In France it is usual to print the last name with captial letters.

>>> set_language('fr')
>>> print p.get_full_name(upper=True)
M. Jean DUPONT

Lino also has a setting 
:attr:`uppercase_last_name <lino.ui.Site.uppercase_last_name>`
which causes this to be the default.

>>> from django.conf import settings
>>> settings.SITE.uppercase_last_name = True

>>> print p
M. Jean DUPONT

When setting 
:attr:`uppercase_last_name <lino.ui.Site.uppercase_last_name>`
is set to True and you (exceptionally) do *not* want uppercase last names, 
then you must specify it explicitly:

>>> print p.get_full_name(upper=False)
M. Jean Dupont


The `mf` method
---------------

The :meth:`mf <lino.mixins.human.Human.mf>` method of a Human
is useful in document templates when you want to generate texts 
that differ depending on the gender of a Human.

>>> set_language('en')
>>> mankind = [Person(first_name="Adam", gender=Genders.male),
...   Person(first_name="Eva", gender=Genders.female)]

>>> def about(p):
...     return "%s was the first %s." % (
...         p,p.mf("man","woman"))
>>> for p in mankind:
...     print about(p)
Mr Adam was the first man.
Mrs Eva was the first woman.


The `mf` method is a bit sexistic in that it returns 
the male value when the `gender` field is blank:

>>> p = Person(first_name="Kai")
>>> print p.mf("He","She")
He

Templates should use the third argument to handle this case properly:

>>> print p.mf("He","She","He or she")
He or she
