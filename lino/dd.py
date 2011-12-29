## Copyright 2011 Luc Saffre
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

"""
The name ``dd`` stands for "Data Dictionary". 

See :class:`lino.core.table.Table` etc.

"""

from lino.core.table import fields_list, is_installed, inject_field
from lino.core.table import has_fk, is_installed, get_app
from lino.core.table import Table
#~ from lino.core import table
#~ Table = table.Table

from lino.core.table import summary, summary_row

from lino.core.table import Frame, Calendar

from lino.core.table import RowAction
from lino.core.table import GridEdit, ShowDetailAction
from lino.core.table import InsertRow, DeleteSelected
from lino.core.table import SubmitDetail, SubmitInsert

from lino.core.fields import GenericForeignKey
from lino.core.fields import GenericForeignKeyIdField
from lino.core.fields import IncompleteDateField
from lino.core.fields import DisplayField
from lino.core.fields import VirtualField
from lino.core.fields import PasswordField
from lino.core.fields import MonthField
from lino.core.fields import LinkedForeignKey
from lino.core.fields import QuantityField
from lino.core.fields import HtmlBox, FieldSet, PriceField, RichTextField
#~ from lino.core.fields import MethodField
