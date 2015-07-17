Lino's solution to define a context-aware list of choices for a `ForeignKey`.

Note: This is being worked on ([Issue 100](https://code.google.com/p/lino/issues/detail?id=100)).

For each ForeignKey field, Lino looks whether the model has a corresponding `_choices` method.

Here is an example:

```

class Contact(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey('countries.Country',blank=True,null=True)
    city = models.ForeignKey('countries.City',blank=True,null=True)
    street = models.CharField(max_length=200,blank=True)

    @staticmethod
    def city_choices(country_id):
        if country:
            return City.objects.all(country__id=country).order_by('name')
        return City.objects.all()
```


Lino detects the `city_choices` method in your model, and input forms for a contact will have the list of choices in `city` automatically be linked to the content of the `country` field.

This is one of [Lino's features](LinoFeatures.md).