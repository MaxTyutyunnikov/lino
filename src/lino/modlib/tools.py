## Copyright 2009 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

from django.db import models
def resolve_model(model,app_label=None):
    # Same logic as in django.db.models.fields.related.add_lazy_relation()
    if not isinstance(model,basestring):
        return model
    try:
        app_label, model_name = model.split(".")
    except ValueError:
        # If we can't split, assume a model in current app
        #app_label = rpt.app_label
        model_name = model
    return models.get_model(app_label,model_name,False)


def resolve_field(name,app_label):
    l = name.split('.')
    if len(l) == 3:
        app_label = l[0]
        del l[0]
    if len(l) == 2:
        #print "models.get_model(",app_label,l[0],False,")"
        model = models.get_model(app_label,l[0],False)
        fld, remote_model, direct, m2m = model._meta.get_field_by_name(l[1])
        assert remote_model is None
        return fld


