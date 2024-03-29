#!/usr/local/bin/python
# -*- coding: ISO-8859-1 -*-

## Copyright 2007 Luc Saffre.
## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


preamble = u"""

This example for the Lino Sonbook typesetting software generates the
Estonian version of the Taiz� songbook.  It is work in progress and
not yet finished.  All Taiz� songs are (c) Ateliers et Presses de
Taiz�, FR-71250 Taiz�-Communaut�.

The terms and conditions for using the pdf and midi files generated by
this software are yet to be written. Don't use it in public without
permission.

"""

from lino.songbook import Songbook


sbk=Songbook(#filename="taize-laulik",
             geometryOptions=dict(a5paper=True,
                                  landscape=True,
                                  heightrounded=True,
                                  twoside=True,
                                  margin="12mm",
                                  bindingoffset="4mm"),
             output_dir=r"C:\temp\laulik",
             showTempi=True,
             input_encoding="latin1")

sbk.addtext(text=preamble)
sbk.loadsong("intro")
sbk.loadsong("dans_nos")
sbk.loadsong("wait_for")
sbk.loadsong("bleibet_hier")
sbk.loadsong("ubi_caritas_deus")
sbk.loadsong("bless_the_lord")
sbk.loadsong("gloria_et_in_terra")
sbk.loadsong("notre_ame")
sbk.loadsong("cest_toi")
sbk.loadsong("jesus_le_christ")
sbk.loadsong("laudate_dominum")
sbk.loadsong("oculi_nostri") #,width=140)
sbk.loadsong("de_noche",width=140)
sbk.loadsong("veni_creator_spiritus",width=140)


sbk.loadsongs("""
lajuda 
mane_nobiscum
qui_regarde
il_signore_ti_ristora
exaudi_orationem
""")
sbk.main()

