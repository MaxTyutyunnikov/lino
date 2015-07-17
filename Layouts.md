A first demo with screenshots in German is [here](20100228.md).

A short introduction using simplified excerpts of code.
You might want to consult the complete source code of [lino.modlib.contacts.models](http://code.google.com/p/lino/source/browse/src/lino/modlib/contacts/models.py).

Let's have a look at the models used in this example.
This is nothing special, just a simple case of a [Django database model](http://docs.djangoproject.com/en/dev/) with inheritance.


```
class Contact(models.Model):
    class Meta:
        abstract = True
        
    name = models.CharField(max_length=200)
    national_id = models.CharField(max_length=200,blank=True)
    street = models.CharField(max_length=200,blank=True)
    street_no = models.CharField(max_length=10,blank=True)
    street_box = models.CharField(max_length=10,blank=True)
    addr1 = models.CharField(max_length=200,blank=True)
    country = models.ForeignKey('countries.Country',blank=True,null=True)
    city = models.ForeignKey('countries.City',blank=True,null=True)
    zip_code = models.CharField(max_length=10,blank=True)
    region = models.CharField(max_length=200,blank=True)
    language = models.ForeignKey('countries.Language',blank=True,null=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    phone = models.CharField(max_length=200,blank=True)
    gsm = models.CharField(max_length=200,blank=True)

    
class Person(Contact):
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200,blank=True)

class Company(Contact):    
    vat_id = models.CharField(max_length=200,blank=True)

```

A Layout in Lino is something like this:

```

from lino import layouts

class ContactPageLayout(layouts.PageLayout):
    box1 = "name"    
    box2 = """national_id:15
              language
              """
    box3 = """country region
              city zip_code:10
              street:25 street_no street_box
              addr1:40
              """
    box4 = """email:40 
              url
              phone
              gsm
              """
    main = """box1 box2
              box3 box4
              remarks:60x6
              """

class PersonPageLayout(ContactPageLayout):
    box1 = "last_name first_name:15 title:10"

class CompanyPageLayout(ContactPageLayout):
    box1 = """name 
    vat_id:12"""

```