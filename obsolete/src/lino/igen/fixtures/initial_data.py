﻿#  
from lino.plugins.countries import *
from lino.utils.instantiator import Instantiator

language = Instantiator(Language,"id name").build
country = Instantiator(Country,"isocode name").build

def objects():

    yield language('et','Estonian')
    yield language('en','English')
    yield language('de','German')
    yield language('fr','German')
    yield language('nl','Dutch')

    yield country('ee',"Estonia")
    yield country('be',"Belgium")
    yield country('de',"Germany")
    yield country('fr',"France")
    yield country('nl',"Netherlands")


