# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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
Example usage:

The first five a Belgians:

>>> for i in range(5):
...     print LAST_NAMES_BELGIUM.pop()
Adam
Adami
Adriaen
Adriaensen
Aelter

Next comes a group of five Russians:

>>> for i in range(5):
...     print LAST_NAMES_RUSSIA.pop()
Abezgauz
Aleksandrov
Altukhov
Alvang
Ankundinov

The next group of ten is a mixture of nationalities, for each Belgian comes one foreigner:

>>> LAST_NAMES = Cycler(LAST_NAMES_BELGIUM,LAST_NAMES_RUSSIA,LAST_NAMES_BELGIUM,LAST_NAMES_MUSLIM)

>>> for i in range(10):
...     print LAST_NAMES.pop()
Aelters
Arent
Aelterman
Abad
Aerens
Arnold
Aerts
Abbas
Aertsens
Arshan

Sources:

The raw data (in UPPERCASE variables) was originally copied from 

- LAST_NAMES_BELGIUM : http://www.lavoute.org/debuter/Belgique.htm
- LAST_NAMES_FRANCE : http://www.nom-famille.com/noms-les-plus-portes-en-france.html
- LAST_NAMES_RUSSIA : http://www.meetmylastname.com/prd/articles/24
- MALE_FIRST_NAMES_FRANCE and FEMALE_FIRST_NAMES_FRANCE :
  http://meilleursprenoms.com/site/LesClassiques/LesClassiques.htm
- MALE_FIRST_NAMES_RUSSIA and FEMALE_FIRST_NAMES_RUSSIA : http://www.babynames.org.uk
- MALE_FIRST_NAMES_MUSLIM and FEMALE_FIRST_NAMES_MUSLIM : http://www.babynames.org.uk
- STREETS_OF_LIEGE: http://fr.wikipedia.org/wiki/Liste_des_rues_de_Li%C3%A8ge
  



"""

import re
STREET_RE = re.compile(r"\*\s*\[\[(.+)\]\]\s*$")
from lino.utils import Cycler

def splitter1(s):
    for ln in s.splitlines():
        ln = ln.strip()
        if len(ln) > 1 and ln[0] != '#':
            yield ln

def splitter2(s):
    return [name.strip() for name in s.split(',')]




LAST_NAMES_BELGIUM = u"""
 
A

Adam

Adami

#Adriaenssens

Adriaen

Adriaensen

#Adriaenssen

#Adriencense

#Adriensence

#Adrienssens

Aelter

Aelters

Aelterman

Aerens

Aerts

Aertsens 

Albumazard

Alloo

Alsteen

Andersson

André

Andries

Andriessen

Anthon

Antoine

Appelbaum

Applaer

Arimont

Arquin

Arteman

B

Baert

Bartholomeeus

Bastien 

Bastin

Baugnet

Baugniet

Baugniez

Bauwens

Beauve

Beck

Beckers

Bernard

Bertrand

Bietmé

Blaas

Blankaert

Blanquaert

Blondeel

Blondeeuw

Blondoo

Bodart

Bodson

Boeck

Boesmans

Bogaert

Bogaerts

Bogemans

Booghmans

Borremans

Borsu

Borsus 

Borsut 

Bosmans

Bouch

Bouchhout

Bouillère

Bouillet

Boulanger

Bourton

Bouxin

Brasseur

Brouck

Broucke

Broucq

Broucque

Brouhier

Brug

Bruggesman

Bruynseel 

Bruynseels

Burger

Burghgraeve

Burgmeester

Burton

Burtont

Buyle

C

Calbert 

Callebaut

Callebert 

Callebout

Camby

Cappelaere

Cappelaire 

Cappelier 

Cappeliez 

Cappellier 

Carbonez

Carbonnez

Carlier

Casteau

Castel

Castiaux

Cauderlier

Caudron

Cauvel

Cauvet

Cauvin

Cavard

Ceulemans

Chantry

Charlier

Chêneboit

Chestay

Chestia

Chrispeels

Christiaens

Christoffel

Claes

Claessens

Claeys

Claus

Cléban

Clébant

Clerx

Colinus

Collard

Colleye
Collignon
Collin
Colson
Cool
Cools
Coppens
Corain
Corijn
Corin
Cornelis
Cornet
Corrin
Corring
Corringer
Coryn
Coudyser
Couhysder
Coutijser 
Coutiser 
Crab 
Crabbe
Crama

Crépez

Crespel

Crevisse

Crevits

Crispeel

Crispeels

Crispel

Crispiels

Cuvelier

Cuypers

D

Daan

Daels

Daems

Dalmans

Damard 

Damart

Danis

Dany 

Danys 

Dapvril

Daufresne

Dawance

De Backer

De Bisschop

De Bloedt

De Blonde

De Boeck

De Bosscher

De Bosschere

De Bruyn

De Busschere

De Buyle

De Clercq

De Cock

De Coninck

De Conninck

De Coster

De Cruyenaere

De Cuyper

De Decker

De Doncker

De Draier

De Flandre

De Frankrijker

De Greef

De Griek

De Groot

De Groote

De Guchteneere

De Haese

De Hert

De Hertog

De Hoorne

De Kimpe

De Markgraef

De Meester

De Meulenaer

De Meyer

De Molder

De Munck

De Muynck

De Muyncke

 De Muynek

 De Muynke

De Naeyer

De Nayer 

 De Pannemacker

De Pannemaecker

De Pauss

De Pauw

De Pelsemaeker

De Pester 

De Potter

De Praeter

De Prester

De Ridder

De Ridere

De Rovéréaz

De Rudere

De Sachte

De Saedeleer

De Saert

De Schepper

De Schoone

De Smedt

De Smet

De Smeytere

De Smidt

De Smit 

 De Smyter

De Stracke

De Sueter

De Vette

De Voghels

De Vos

De Vrient

De Wilde

De Winter

Debacker

Debaere

Debakker

Debaut

Debecker

Debekker

Debled

Deboschere

Deboscker

Deboskre

Debosscher

Debosschere

Debusschere

Debuyst

Declerck

Declercq

Decock

Decocq

Decrucq

Decruyenaere

Defaux

Defawe

Degroote

Dehoorne

Dehorne

Dehornes

Deilgat

Dejong

Dejonghe

Dekale

Dekimpe 

Dekoch

Dekuiper

Dekyndt

Delacuvellerie

Delafosse 

Delahaye 

Delahayes 

Delbouille

Delboulle

Delcorps

Delflache

Delfosse

Delgat 

Delhaye

Delhoste 

Delhotte

Delmare

Delmer

Delobbe

Delobe 

Delobes 

Delplace

Delvaux

Demain

Demeiere

Demeyer

Demoor

Demoore

 Demunck

Demunck

Demuynck

Den Ouste

Denaeyer

Denayer

Deneyer

Denis

Denoor

Depannemaecker

Depelsemacker

Depelsemaeker

Depelsenaire 

Depelseneer 

Depercenaire 

Depester 

Depiéreux 

Depierreux 

Depireux 

Depoorter

Depoortere 

Depooter 

Depootere 

Deporter 

Deportere 

Depoterre

Deprez

Deramaix

Deroosse

Desandrouins

Descamps

Deschepper

Desmedt

Desmet

Desmets

Desmeytere

Desmidt

Desmidts 

Desmit

Desmyter

Desmytter

Desmyttere

 Despineto

Després 

Despret 

Desprets 

Despretz 

Desprey 

Desprez 

Destoute

Deswart

Deswarte

Dethier

Deur

Deurwaerder

Devis

Devloo

Devos

Devriend

Dewever

Dewit

Dewitte

Dewyse

D'Haeyer

Dhaeyer

D'Hoeraen

Dhoeraen

D'hoolaege

Dierckx

Dierik

Doeraene

Dolhaeghe

Domiens

Dominicus

Dondaine

Dondeine 

Dondenne 

Dondeyne 

Doolaeg(h)e

Doolaegue

Doolage

Doorn

Doorne

Doorneman

Draier

Dresselaers

Dubled

Dubois

Dumont

Dupont

Duquesnay

Duquesne

Duquesnoy

E

Ebrard

Eeckeman

Eerkens

Erckens

Erk

Erken

Erkens

Etienne

Euvrard

Evert

Evrard

Evras

Evrat

Eyck

Eysermans

F

Fawat

Faweux

Fee

Felix

Flamenck

Floche

Floquet

Fontaine

Fonteyne

Fraigany

Fraigneux

Francoeur

François

Francon

Frankel

Franken

Frankeur

Frans

Fransman

Fransolet

Franzman

Frijer

G

Gabriels

Gadisseur

Gadisseux

Gasthuys

Gaudisseu

Geerts

Gehucht

Geiregat

Geeregat 

Gendebien

Genot

Georges

Gérard

Gerlache

Gerlaxhe 

Germay

Germéa

Germeau

Ghiste

Gilles

Gillet

Gilson

Gits

Giets

Gidts

Geets

Geerts

Glaze

Glazeman

Goethals

Goffin

Gomaert

Gomardt

Goor

Goossens

Goud

Goudman

Goudsmith

Gourdet

Gousson

Graas

Greggs

Gregh

Grégoire

Gregoor

Grewis

Groot

Groote

Grotaers

Guillaume

Guyaux

H

Haesen

Haesevoets

Halasi

Halazy

Hamers

Hanssens

Hardas 

Hardat

Hardy

Heerbrant

Hendrick

Hendrickx

Hendriks

Henry

Herbrand 

Herbrandt 

Herbrant 

Herman

Hermann 

Hermans

Herten

Hertogs

Hertogue

Heylen

Heymans

Heynemans

Heyrman

Hinck

Hinckel

Hincker

Hinkel

Hinkels

Hinkens

Hinker

Hinkle

Hoefnagel 

Hoefnagels 

Holemans

Honnay

Horlin

Houvenaghel

Hoyois

Hubert

Huig

I

Ickx

Istace 

Istasse 

J

Jaak

Jaap

Jacob

Jacobs

Jacques

Jacquet

Jan

Janhes

Jansen

Janssen

Janssens

Jef

Jenot

Jeuniaux

Joire

Jone

Joneau

Jonet

Jongers

Jonné

Jonet

Jonnet

Jordaens

Jorez

Joris

Jorissen

Jozef

Julianus

Julius

Jurgen

K

Kaalman

Kaisin

Keetels

Kenens 

Kenes 

Kenis 

Kennens 

Kennes 

Kennis 

Kesteloot

Ketel

Ketelsmit

Kiecken

Kimpe 

Kinnen 

Klein 

Kleineman

Kleiner 

Kleinerman

Kleinman 

Klerk

Kleynen

Klingeleers

Kobus

Koeck

Konninckx

Koolman

Korring

Kramers

Kreemers

Kuipers

L

Labbez

Lacroix

Laenen 

Laenens 

Lafontaine 

Lambert

Lambrechts

Lanen 

Lanens 

Langlez

Lapayre

Laseur

Laseure

Lauffer

Laurent

Lauwers

Le Mayeur

Le Provost

Leboutte

Lebrun

Leclerc

Leclercq

Lecocq

Lecomte

Ledecq

Leenhard

Leenhart

Lefebvre

Lefèvre

Legrand

Lejeune

Lemaire

Lemmens

Lemonnier

Lemounie

Lenaerts

Lénel 

Lénelle

Lennel 

Léonard

Lepoutre

Leprette

Lepropre

Leroy

Lescohy

Lesoil

Lesoile 

Lesoille 

Levecq

Lewek

Libert

Liens

Liephoudt

Liepot

Liepout

Lieseborghs

Liesenborghs

Lietaer

Lietaert

Lietar

Liétar

Liétard

Liétart

Lievens

Lievesoons 

Lievevrouw 

Lievrouw

Liévrouw

Lievrow 

Linglay

Linglet

Liphout

Lisenborgh

Lisenborgs

Locreille 

Locrel

Locrelle 

Lode

Loo

Lorfèvre

Lorphêvre

Losseau

Losset

Louis

Louzeau

Lowie

Ludovicus

Lugen

Lugens 

Lust

Lustig

Luyer

Luyrik

Luyten

Lyphoudt 

Lyphout

M

Maca

Maertens

Maes

Maessen

Mahieu

Maka

Malchamp 

Malchamps 

Malmedier

Malmedy

Malmendier

Mangon

Maqua

Marchal

Marckx

Marcus

Mardaga

Maréchal

Maria

Mark

Markgraff

Martens

Martin

Martins

Massart

Masson

Mathieu

Mathissen

Mathy

Matthys

Mauchamp 

Mauchamps 

Maurichon

Maurissen

Maurits

Mayeur

Mayeux

Mechelaere

Meert

Meertens

Meester

Meeus

Melaerts 

Mellaerts

Merchié

Merchier

Mergeai

Mergeay

Merjai

Merjay

Mertens

Mertes

Merts 

Mertz 

Meulemans

Meulemeesters

Meunier

Meurice

Mewis

Mewissen

Michaël

Michaux

Michel

Michiels

Mixhel

Mochamps

Moens

Moeyaert 

Moiling

Moinil

Molemans

Molenaers

Monceau

Moncia

Monciaux

Monsay

Monteyne

Moreau

Mouyart

Moyaert 

Mullenders

Munck

Muynck

N

Nachtegael

Nagelmaekers

Nagels

Natus

Neel

Neels

Neuray

Neureau

Neuret

Neurot

Neuts 

Neuven

Neven

Nguyen

Nicolas

Nicolaus

Nicolus

Nijs

Niklaas

Noël

Nuts 

Nuttin

O

Ochin

Olivier

Olyff

P

Paindavaine

Pannaye

Parmentier

Pas

Pauss

Pauwels

Peeters

Pelser

Pelsmaeker

Peschon

Peschoniez

Pester

Petersen

Petit

Pierre

Piet

Pieters

Pietersen

Piette

Pirard

Piron

Pirotte

Plaats

Poels

Poelsmans

Poncelet

Pools

Posson

Potstainer

Potter

Pottiaux

Pottié

Potty

Poyon

Praat

Premereur 

Premmereur

Prevostel

Priesse

Prisse

Proost

Prost

Proust

Putmans

Putmans

Puttemans

Puttemans

Putman 

Q

Quaisin

Quesnay

Quesne

Quesneau

Quesnel

Quesney

Quesnoy

Queval

R

Raes

Ramael

Raucent

Rauscent

Rausin 

Raussain

Raussent

Raussin 

Raveydts

Ravignat

Remy

Renard

Retelet

Ricaart

Ricaert

Ricard

Robaert

Robbert

Robert

Roels

Roland

Rooseels

Roosengardt

Rosseel

Rousseau

S

Saintmaux 

Saint-Maux

Sanctorum

Santilman

Schmitz

Schnock

Schoenmakers

Schoenman

Schoone

Scorier

Scuvie

Scuvie

Segers

Seghers

Seppen

Servais

Shoen

Sijmen

Simoens

Simon

Simons

Sinnesaël

Sinnesal 

Slagmolder

Slagmulder

Slamulder

Smal

Smeets

Smet

Smets

Smit

Smolders

Smulders

Somers

Sottiaux

Spinette

Sprecher

Stas

Stass 

Stassaert 

Stassar 

Stassard 

Stassart 

Stasse 

Stassiaux 

Stassin 

Stassinet 

Statius 

Steculorum

Stefaans

Stercken

Sterckmans

Sterckx

Stevens

Stier

Stiers

Stievens

Stine

Stoffel

Stordair

Stordeur

Stoutmans

Swart

Swarte

T

Tack

Taverner

Teissant

Terreur

Thijs

Thiry

Thissen

Thomas

Thonnisen

Thuiliau

Thuiliaux

Thuiliet

Thys

Tibaut

Timmerman

Timmermans

T'Jampens

Tjampens

Toussaint

Trausch

Tuiliau

Tuiliaux

Tuilliet

Tuin

Tumson

Tweelinckx

U

Urbain

Urting

V

Van Acker

Van Aelter

Van Belle

Van Berckel

Van Bergh

Van Caenegem

Van Caeneghem

Van Daele

Van Damme

Van de Loo

Van de Pas 

Van de Poel

Van de Slijke

Van de Slycke

Van de Veld

Van de Velde

Van den Bergh

Van den Bogaerde

Van den Borne

Van den Bossche

Van den Broeck

Van den Broecke

Van den Camp

Van den Castele

Van den Dael

Van den Dorpe

Van den Tuin

Van Den

Van der Brug

Van der Gucht

Van der Pas 

Van der Slijke

Van der Slikke

Van der Slycke

Van der Vleuten 

Van Doren

Van Dorp

Van Dorpe

Van Dovlaeghe

Van Dyck

Van Engeland

Van Esch

Van Escht

Van Eyck

Van Hecke

Van Hoof

Van Hoorebeke

Van Hoorenbeeck

Van Horenbeck

Van Horenbeeck

 Van Lierde

Van Noye

Van Noÿe

Van Pé

Van Pede

Van Pée

Van Roy

Van Sinaey

Van Slijke

Van Slycke

Van Steerteghem

Van Steerteghen

Van Steirteghem

Van Vleuten 

Vanbattel

Vanbergh

Vandamme

Vandenberghe

Vandenbossche 

Vandenbussche

Vandendorpe

Vandeputte

Vanderhorst

Vanderlinden

Vanderplaetsen

Vandevelde

Vandoolaeghe

Vandorpe

Vanlierde

Vanpé

Vanpede

Vanpée

Vansteertegem

Vecq

Veld

Veldmann

Vellemans

Veraghe

Veraghen

Verbeeck

Verbeke

Verbruggen

Vercammen

Vercheval

Verdoolaeg(h)e

Verhaege

Verhaegen

Verhaeghe

Verhaeghen

Verhaegue

Verhage

Verhagen

Verhaghe

Verhelst

Verheyen

Verhoeven

Verlinden

Vermeer 

Vermeersch

Vermeiren

Vermeren 

Vermeulen

Vermotte 

Verplaetse

Verplancke

Verplancken

Verschueren

Verslijke

Verslycke

Verstraete

Verstraeten

Vervoort

Vet

Vette

Viatour

 Vieutemps 

Vieutems 

Vieuxtemps

Vilain 

Vincent 

Vinchent

Visje

Vlaamsche

Vlaeminck

Vlaemynck

Vlaminck

Vlamynck

Vlemincks

Vleminckx

Vleminx

Vlemynckx

Vogels

Volckaert

Volkaert

Volkaerts

Volkart

Volkert

Voller

Vos

Vossen

Vrank

Vrindt

Vrolijt

Vrolyck

Vullers

W

Wagemans

Wagenmann 

Waghon 

Wagon

Walle

Wastiaux 

Watrigant 

Watriquant 

Watteau 

Watteau

Watteaux 

Watteaux

Wattecamp 

Wattecamps

Wattecant 

Watteel

Wattel

Wattelle

Wattiau 

Wattiaux 

Wattieaux 

Wauters

Weers 

Weerts

Wek

Wevers

Weynen

Wilbaert

Wilfart

Willems

Willock

Willocq

Wilock

Wintgens

Wouter

Wouters

Wuyts

Wylock
Wylocke

Y

Yildirim
Yilmaz

Z

Zadelaar
Zegers
Zeggers
Zègres
"""


LAST_NAMES_FRANCE = u"""
Martin	236 172
Bernard	131 901
Thomas	119 078
Dubois	114 001
Durand	111 510
Robert	106 161
Moreau	103 056
Petit	95 876
Simon	95 733
Michel	93 581
Leroy	88 722
Laurent	85 243
Lefebvre	82 670
Bertrand	75 030
Roux	74 955
David	73 150
Garnier	67 829
Legrand	67 475
Garcia	67 162
Bonnet	66 124
Lambert	65 724
Girard	65 228
Morel	64 537
Andre	64 301
Dupont	63 520
Guerin	62 971
Fournier	61 770
Lefevre	61 662
Rousseau	58 884
Francois	58 409
Fontaine	57 783
Mercier	56 702
Roussel	56 300
Boyer	56 024
Blanc	54 714
Henry	54 212
Chevalier	53 741
Masson	52 966
Clement	51 177
Perrin	50 834
Lemaire	50 038
Dumont	49 834
Meyer	48 796
Marchand	47 763
Joly	47 337
Gauthier	47 218
Mathieu	47 178
Nicolas	46 761
Nguyen	46 605
Robin	46 329
Barbier	45 635
Lucas	44 369
Schmitt	44 128
Duval	44 075
Gerard	43 762
Noel	43 263
Gautier	42 411
Dufour	42 209
Meunier	41 833
Brunet	41 807
Blanchard	41 477
Leroux	41 162
Caron	40 845
Lopez	40 431
Giraud	39 896
Fabre	39 592
Pierre	39 469
Gaillard	39 260
Sanchez	39 133
Riviere	39 018
Renard	37 607
Perez	37 371
Renaud	37 274
Lemoine	37 222
Arnaud	37 173
Jean	36 901
Colin	36 289
Brun	36 159
Philippe	35 922
Picard	35 912
Rolland	35 870
Olivier	35 384
Vidal	34 737
Leclercq	34 630
Aubert	34 477
Hubert	34 429
Bourgeois	34 380
Roy	33 798
Guillaume	33 518
Adam	32 624
Dupuy	31 895
Louis	31 785
Maillard	31 752
Aubry	31 184
Charpentier	30 139
Benoit	30 055
Berger	29 640
Royer	29 425
Poirier	29 345
Dupuis	29 339
Rodriguez	29 330
Jacquet	29 274
Moulin	29 065
Charles	29 041
Lecomte	28 980
Deschamps	28 823
Fernandez	28 547
Guillot	28 526
Collet	28 333
Prevost	28 129
Germain	27 664
Bailly	27 588
Guyot	27 419
Perrot	27 293
Le gall	27 140
Renault	27 138
Le roux	26 551
Vasseur	26 431
Herve	26 272
Gonzalez	26 182
Barre	26 084
Breton	26 057
Huet	25 961
Bertin	25 960
Carpentier	25 809
Lebrun	25 749
Carre	25 435
Boucher	25 365
Menard	25 135
Rey	24 943
Klein	24 750
Weber	24 727
Collin	24 553
Cousin	24 314
Millet	24 310
Tessier	23 978
Leveque	23 737
Le goff	23 704
Lesage	23 599
Marchal	23 525
Leblanc	23 492
Bouchet	23 442
Etienne	23 413
Jacob	23 328
Humbert	23 315
Bouvier	23 290
Leger	23 273
Perrier	23 182
Pelletier	22 952
Remy	22 824
"""


FEMALE_FIRST_NAMES_FRANCE = u"""
Adélaïde, Adèle, Agnès, Alix, Béatrice, Beatrix, Elizabeth, Hélène, Héloïse, Isabeau, Iseult, Irène, Mahaut, Margot, Mathilde, Mélissende, Pétronille, Yolande,
Adèle, Aimée, Alice, Appoline, Augustine, Céleste, Célie, Emma, Élise, Églantine, Eugénie, Irène, Jeanne, Joséphine, Léopoldine, Léontine, Lucie, Louise, Madeleine, Mathilde, Ophélie, Pauline, Rose, Zoé
Albanie, Alexine, Aglaé, Alina, Alma, Angèle, Appoline, Armance, Arthémise, Augustine, Blanche, Célestine, Colombe, Dina, Elia, Émerence, Eulalie, Eugénie, Félicie, Fleurine, Gracianne, Honorine, Jeanne, Léona, Léonie, Léontine, Lilly, Louise, Matilde, Noémi, Pétronille, Philomène, Rose, Salomée, Sidonie, Victoire, Victorine Zélie
"""

MALE_FIRST_NAMES_FRANCE = u"""
Ambroise, Amédée, Anastase, Arthur, Augustin, Aymeric, Béranger, Geoffroy, Grégoire, Guillaume, Léon, Louis, Théodore, Thibaut, Tristan,
Alfred, Alphonse, Amédée, Aristide, Augustin, Barthélémy, Cyprien, Eugène, Ferdinand, Félix, Gustave, Jules, Justin, Léon, Théophile, Victor, Virgile,
Abel, Achille, Aimé, Anatole, Anthime, Auguste, Augustin, Célestin, Edgar, Emile, Ernest, Faustin, Félix, Gaston, Gustave, Jules, Léon, Léopold, Louis, Marceau, Marius, Max, Melchior, Oscar, Philémon, Rubens, Sully, Théodore, Théophile, Victor, Victorin, Wilhem
"""

# copied from http://fr.wikipedia.org/w/index.php?title=Liste_des_rues_de_Li%C3%A8ge&action=edit
STREETS_OF_LIEGE = u"""
{{ébauche|Liège}}
Cet article dresse une liste (incomplète) des voies ([[voirie]]s et [[Place (voie)|places]]) de la [[Ville de Belgique|ville]] de [[Liège]] en [[Belgique]].

{{SommaireCompact}}

==2==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
*[[Place du 20-Août]]
</div>

==A==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">

* [[Rue de l'Abattoir]]
* [[Rue des Abeilles (Liège)|Rue des Abeilles]]
* [[Rue des Acacias (Liège)|Rue des Acacias]]
* [[Rue de l'Académie]]
* [[Avenue Albert Mahiels]]
* [[Rue Ambiorix]]
* [[Rue d'Amercoeur]]
* [[rue des Anglais (Liège)|Rue des Anglais]]
* [[Rue d'Ans]]
* [[Quai des Ardennes]]
* [[Rue Armand Stouls]]
* [[Rue Auguste Hock]]
* [[Rue des Augustins (Liège)|Rue des Augustins]]
* [[Impasse de l'Avenir]]
* [[Boulevard d'Avroy]]
* [[Rue d'Awans]]

</div>

==B==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[La Batte]]<ref>Batte signifiant ''quai'' en [[wallon]], on ne doit donc pas dire quai de la Batte</ref>
* [[Rue Basse-Wez]]
* [[Rue Beauregard (Liège)|Rue Beauregard]]
* [[Place des Béguinages]]
* [[Rue Bernimolin]]
* [[Rue Bidaut]]
* [[Avenue Blonden]]
* [[Rue Bois Gotha]]
* [[Quai Bonaparte]]
* [[Rue Bonne-Fortune]]
* [[Rue Bonne-Nouvelle]]
* [[Rue des Bons Enfants (Liège)|Rue des Bons Enfants]]
* [[Rue du Bosquet (Liège)|Rue du Bosquet]]
* [[Rue de la Boucherie (Liège)]]
* [[Quai de la Boverie]]
* [[Rue de Bruxelles (Liège)|Rue de Bruxelles]]
* [[Montagne de Bueren]]

</div>

==C==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue de Campine]]
* [[Rue des Carmes (Liège)|Rue des Carmes]]
* [[Place des Carmes]]
* [[Rue de la Casquette]]
* [[Place de la Cathédrale]]
* [[Rue de la Cathédrale]]
* [[Boulevard César Thomson]]
* [[Rue des Champs]]
* [[Rue Charles Bartholomez]]
* [[Rue Charles Magnette]]
* [[Avenue Rogier (Liège)|Avenue Charles Rogier]]
* [[Thier de la Chartreuse]]
* [[Rue de Chaudfontaine]]
* [[Rue Chauve-Souris (Liège)|Rue Chauve-Souris]]
* [[Rue de la Cité (Liège)|Rue de la Cité]]
* [[Rue des Clarisses]]
* [[Boulevard de la Constitution]]
* [[Rue du Coq]]
* [[Rue Counotte]]
* [[Rue Cour Petit]]
* [[Place Crèvecœur]]
* [[Rue des Croisiers]]
* [[Rue des Croix-de-Guerre]]
</div>

==D==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue Darchis]]
* [[Rue Dartois]]
* [[Rue Dehin]]
* [[Rue Denis Sotiau]]
* [[Rue Dony]]
* [[Rue Douffet]]
</div>

==E==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Boulevard Émile de Laveleye]]
* [[Avenue Émile Digneffe]]
* [[Rue Émile Gérard]]
* [[Rue Émile Vandervelde (Liège)|Rue Émile Vandervelde]]
* [[Rue En Bois]]
* [[Rue Ernest de Bavière]]
* [[Rue Ernest Solvay (Liège)|Rue Ernest Solvay]]
* [[Rue Éracle]]
* [[Rue Eugène Houdret]]
* [[Rue de l'Étuve (Liège)|Rue de l'Étuve]]
</div>

==F==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Féronstrée]]
* [[Rue de Fétinne]]
* [[Rue Fond Saint-Servais]]
* [[Rue fond des Tawes]]
* [[Rue des Fontaines-Roland]]
* [[Rue des Fossés]]
* [[Rue de Fragnée]]
* [[Place des Franchises]]
* [[Boulevard Frankignoul]]
* [[Ernest-Frédéric Nyst|Rue Frédéric Nyst]]
* [[Rue aux Frênes]]
* [[Boulevard Frère-Orban]]
</div>

==G==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue Gaston Laboulle]]
* [[Rue Gaucet]]
* [[Quai de Gaulle]]
* [[Rue du Général de Gaulle]]
* [[Rue du Général Bertrand]]
* [[Place du Général Leman]]
* [[Rue Georges Simenon]]
* [[Quai Godefroid Kurth]]
* [[Quai de la Goffe]]
* [[Rue de la Goffe]]
* [[Impasse Graindor]]
* [[Rue Gramme (Liège)|Rue Gramme]]
* [[Rue Grande Bêche]]
* [[Rue des Gravillons]]
* [[Rue Grétry (Liège)|Rue Grétry]]
* [[Rue du Gros Gland]]
* [[Place des Guillemins]]
* [[Rue des Guillemins]]
</div>

==H==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue de la Halle]]
* [[Rue de Harlez]]
* [[Rue d'Harscamp]]
* [[Rue du Haut-Pré]]
* [[Place du Haut-Pré]]
* [[Rue Hazinelle]]
* [[Rue Henri Baron]]
* [[Rue Henri Koch (Liège)|Rue Henri Koch]]
* [[Rue Henri Maus (Liège)|Rue Henri Maus]]
* [[Rue Herman Reuleaux]]
* [[Rue de Hesbaye]]
* [[Rue Hocheporte]]
* [[Rue Hors-Château]]
* [[Rue des Houblonnières]]
* [[Rue Hullos]]
</div>

==I==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Place d'Italie (Liège)|Place d'Italie]]
* [[Rue des Ixellois]]
</div>

==J==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue Jambe de Bois]]
* [[Rue du Jardin Botanique]]
* [[Rue Jean Bury]]
* [[Rue Jean d'Outremeuse]]
* [[Rue Jean Haust]]
* [[Rue Joffre]]
* [[Rue de Joie]]
* [[Rue Jonckeu]]
* [[Rue Jondry]]
* [[Rue des Jonquilles (Liège)|Rue des Jonquilles]]
* [[Place Joseph de Bronckart]]
* [[Rue Joseph Demoulin]]
* [[Rue Joseph Henrion]]
* [[Rue Joseph Lacroix]]
* [[Rue Joseph Wauters (Liège) |Rue Joseph Wauters]]

</div>

==L==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue Lairesse]]
* [[Rue de Lantin]]
* [[Rue du Laveu (Liège)|Rue du Laveu]]
* [[Rue de la Légia]]
* [[Rue Lemille]]
* [[Passage Lemonnier]]
* [[Rue Léon Mignon (Liège)|Rue Léon Mignon]] 
* [[Rue Léopold]]
* [[Rue Libotte]]
* [[Rue de Londres (Liège)|Rue de Londres]]
* [[Quai de Longdoz]]
* [[Rue Louis Abry]]
* [[Rue Louis Fraigneux]]
* [[Rue Louvrex]]
* [[Avenue du Luxembourg]]
</div>

==M==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Quai de Maestricht]]
* [[Rue des Maraîchers (Liège)|Rue des Maraîchers]]
* [[Place du Marché (Liège)|Place du Marché]]
* [[Quai Marcellis]]
* [[Quai Mativa]]
* [[Avenue Maurice Destenay]]
* [[Rue Méan]]
* [[Quai sur Meuse]]
* [[Rue Mississippi]] 
* [[Rue du Mont Saint-Martin]]
* [[Rue Montagne Sainte-Walburge]]
</div>

==N==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue de Namur]]
* [[Rue Naniot]]
* [[Rue Natalis]]
* [[Place des Nations-Unies (Liège)|Place des Nations-Unies]]
* [[En Neuvice]]
</div>

==O==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Place de l'Opéra (Liège)|Place de l'Opéra]]
* [[Quai Orban]]
* [[Rue Oscar Rémy]]
* [[Quai de l'Ourthe]]
</div>

==P==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue Paradis (Liège)|Rue Paradis]]
* [[Rue du Parc]]
* [[Rue du Palais (Liège)|Rue du Palais]]
* [[Rue de Paris (Liège)|Rue de Paris]]
* [[Au Péri]]
* [[Boulevard Piercot]]
* [[Rue Pierreuse]]
* [[Rue du Plan Incliné]]
* [[Rue Plumier]]
* [[Rue Pont-d'Avroy]]
* [[Rue Pont-d'Ile]]
* [[Rue du Pot d'Or]]
* [[Potiérue]]
* [[Rue des Prébendiers]]
* [[Rue Publémont]]
* [[Rue Puits-en-Sock]]
* [[Rue du Puits]]
</div>

==R==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue des Récollets (Liège)|Rue des Récollets]]
* [[Rue de la Régence (Liège)|Rue de la Régence]]
* [[Rue Regnier-Poncelet (Liège)|Rue Regnier-Poncelet]]
* [[Avenue Reine Elisabeth]]
* [[Rue des Remparts]]
* [[Place de la République française]]
* [[Rue de la Résistance]]
* [[Quai de la Ribuée]]
* [[Rue des Rivageois]]
* [[Rue Robertson]]
* [[Quai de Rome]]
* [[Quai Roosevelt]]
* [[Rue Roture]]
</div>

==S==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Place Saint-Barthélemy]]
* [[Place Saint-Denis]]
* [[Rue Saint-Gilles (Liège)|Rue Saint-Gilles]]
* [[Place Saint-Jacques (Liège)|Place Saint-Jacques]]
* [[Place Saint-Lambert (Liège)|Place Saint-Lambert]]
* [[Rue Saint-Laurent (Liège)|Rue Saint-Laurent]]
* [[Esplanade Saint-Léonard (Liège)|Esplanade Saint-Léonard]]
* [[Rue Saint-Léonard]]
* [[Rue Sainte-Marie (Liège)|Rue Sainte-Marie]]
* [[Rue Saint-Martin-en-Île]]
* [[Place Saint-Michel (Liège)|Place Saint-Michel]]
* [[Rue Saint-Michel (Liège)|Rue Saint-Michel]]
* [[Place Saint-Paul (Liège)|Place Saint-Paul]]
* [[Rue Saint-Paul (Liège)|Rue Saint-Paul]]
* [[Rue Saint-Pierre (Liège)|Rue Saint-Pierre]]
* [[Rue Saint-Remacle]]
* [[Rue Saint-Remy]]
* [[Rue Saint-Séverin (Liège)|Rue Saint-Séverin]]
* [[Rue Sainte-Croix]]
* [[Rue Sainte-Marguerite (Liège)|Rue Sainte-Marguerite]]
* [[Place Sainte-Véronique]]
* [[Rue Sainte-Véronique]]
* [[Rue Sainte-Walburge]]
* [[Boulevard Saucy]]
* [[Boulevard de la Sauvenière]]
* [[Rue de Sclessin]]
* [[Rue de Seraing]]
* [[Rue de la Sirène]]
* [[Rue Soubre]]
* [[Rue Sous l'Eau]]
* [[Rue de Spa (Liège)|Rue de Spa]]
* [[Rue Stappers]]
* [[Rue de Stavelot]]
* [[Rue Suavius]]
</div>

==T==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Quai des Tanneurs]]
* [[Rue des Tanneurs (Liège)|Rue des Tanneurs]]
* [[Rue des Tawes]]
* [[Rue du Terris (Liège)|Rue du Terris]]
* [[Place du Tertre (Liège)|Place du Tertre]]
* [[Rue du Thier-à-Liège]]
* [[Chaussée de Tongres]]
* [[Rue Tournant Saint-Paul]]
* [[Rue Toussaint Beaujean]]
</div>

* [[Rue de l'Université (Liège)|Rue de l'Université]]
* [[Rue des Urbanistes]]
* [[Impasse des Ursulines (Liège)|Impasse des Ursulines]]

* [[Rue Valdor]]
* [[Quai Édouard van Beneden]]
* [[Rue Varin]]
* [[Rue des Vennes]]
* [[Rue du Vertbois (Liège)|Rue du Vertbois]]
* [[Rue du Vieux Mayeur]]
* [[Impasse du Vieux Pont des Arches]]
* [[Rue Villette]]
* [[Vinâve d'Île]]<ref>Vinâve signifiant ''artère principale'' en [[wallon]], on ne doit donc pas dire rue du Vinâve d'Île</ref>
* [[Rue Volière (Liège)|Rue Volière]]

* [[Rue des Wallons (Liège)|Rue des Wallons]]
* [[Rue de Waroux]]
* [[Rue de Wazon]]
* [[Rue de Wetzlar]]
* [[Rue Wiertz (Liège)|Rue Wiertz]]

* [[Place Xavier Neujean]]


"""

LAST_NAMES_RUSSIA = u"""
A
Abezgauz 
Aleksandrov 
Altukhov 
Alvang 
Ankundinov 
Arent 
Arnold 
Arshan 
Arshun 
Artemieva 
Astafurov 

B
Bardzecki 
Bartoszewicz 
Bashmakov 
Baskov 
Bek-Murzin 
Belskaia 
Berendt 
Berndt 
Bernt 
Berthner 
Bilinskii 
Bleiwas 
Bobrov 
Bogaevskaia 
Bogdanjwa 
Bogdanovich 
Bolokhovskis 
Bondar 
Borenstein 
Borodinskii 
Borovsky 
Borowski 
Botkina 
Budberg 
Budian 
Budkovskiy 
Budliavski 
Burdzecki 
Burundukov 
Buryshkin 
Burzeckaia 

C
Chepelskii 
Cheremisinova 
Cherevin 
Cherkesov 
Cherlin 
Cherlina 
Chernikova 
Cherstvennikov 
Chirkoff 
Chopiak 
Chubinskii 
Chuchin 
Chuzhoi 

D
Dauksza 
Dikau 
Dmitriev 
Domashevich 
Dombrovski 
Dotsenko 
Dvorkin 
Dvorzhetskii 
Dzhigit 

E
Elout 
Entin 

F
Feldberg 
Fialkovskii 
Fiialkov 
Flits 
Frinovskii 

G
Garder 
Gaunshtein 
Gavlik 
Gavrikov 
Gavronskii 
Gelb 
Gepfner 
Gerasimova 
Gerburt 
Gershan 
Gikalov 
Gise 
Giunter 
Glazov 
Glinka 
Glubonin 
Golender 
Golovkin 
Gontmakher 
Gorchakov 
Gorenshtein 
Grabianko 
Gundobin 
Gunter 
Gusarov 
Gutelmakher 
Gutemovskii 
Gutenmakher 
Guttenmakher 

H
Holender 

I
Ialovskaia 
Ialovskii 
Iavlenskaia 
Ioksimovich 
Ioselovich 
Iskander 
Istomin 
Iunter 
Iushkevich 
Ivanov 

K
Kalandarishvili 
Kamarauskas 
Kasianenko 
Kenin 
Khanina 
Khavin 
Kheifets 
Khitrovo 
Khmelnitskii 
Khodkevich 
Khripunov 
Khripunova 
Kintsel 
Kiselow 
Kitaev 
Klopov 
Koliabskaia 
Kologrivov 
Kologrivova 
Komarnitskaia 
Komarov 
Komarovski 
Komarovskii 
Komerovskaia 
Konchin 
Konfer 
Konkin 
Konn 
Konstantinov 
Konstantinova 
Korchagina 
Korchinskaia 
Kosmachevskaia 
Kosovskaia 
Kotko 
Kovalevski 
Kozerskaia 
Kozerski 
Kozlow 
Kozyrskii 
Kriukov 
Kulikovskaia 
Kunitskaia 
Kupchenko 
Kuzmin 

L
Lebel 
Lempitskaia 
Lenevski 
Leontiev 
Lerche 
Levanda 
Levinson 
Levitan 
Levkov 
Levkova 
Likharev 
Likhareva 
Lipinskii 
Lishin 
Lisitskaia 
Lisovskii 
Lukowskaia 

M
Magnovska 
Mahkno 
Maier 
Makarova 
Maklakov 
Maksimov 
Malakhovskii 
Maletski 
Maletskii 
Malinovskii 
Maliszewski 
Maliszkewicz 
Malitzka 
Malitzkii 
Malygin 
Markevich 
Masalsky 
Maslov 
Massalsky 
Matsevich 
Matsevichus 
Matskevich 
Mattel 
Matulevich 
Mayer 
Medvedev 
Medvedeva 
Meier 
Melnikov 
Menshutkin 
Menzhinskii 
Mezentsov 
Mezentsova 
Mikhailov 
Milaszewicz 
Milaszewska 
Milaszewski 
Milkovich 
Milodanovich 
Milosz 
Miloszinski 
Mionchinskaia 
Mirskii 
Misostov 
Miziukov 
Molchanov 
Molotkoff 
Morozov 
Mosalsky 
Moskvin 
Moszynski 
Mozheika 

N
Nazilevskii 
Nebogatov 
Negnevitskii 
Nevelskoi 
Nikonechnaia 
Nisselovich 

O
Oborskaia 
Oborski 
Okecka 
Okkerman 
Olendzskaia 

P
Pankov 
Panushkis 
Parnes 
Parolow 
Paulson 
Pavlovskii 
Pechatnoff 
Petrov 
Petrovskaia 
Petrovskii 
Petrowa 
Piotrovskii 
Pletner 
Plotnitskaia 
Pogoretskaia 
Pogorzelski 
Polivanov 
Polovinkin 
Ponomarev 
Popova 
Popovtsev 
Posiet 
Potemkin 
Pravdin 
Priselkov 
Prokofiev 
Prokopchenko 
Prokopovich 
Pruszynski 
Pumpianskii 
Putilina 

R
Rakhmelevich 
Reikhman 
Reznikov 
Reznikova 
Rodwalski 
Rogusskii 
Rokitskaia 
Roschin 
Rosenthal 
Rowan 
Rusakov 
Rusakova 

S
Saburova 
Seidin 
Semenov 
Shalberov 
Shchepetov 
Shcherbatov 
Shereshevski 
Sheridan 
Shikov 
Shiritlokov 
Shkarov 
Shponarskaia 
Shtadler 
Shtein 
Shubovich 
Shuliakovskii 
Shulkovskii 
Shumakher 
Shvarts 
Siegel 
Simonovich 
Simson 
Siniakov 
Sipiagin 
Sivortsova 
Skipetroff 
Skipetrova 
Slavin 
Slavina 
Smolenskaia 
Smolenskii 
Sobeskaia 
Sobetskaia 
Sokolovskii 
Solomon 
Soloviev 
Somov 
Somova 
Sotravits 
Spektor 
Speshiloff 
Stanevich 
Steinhauer 
Steinheil 
Stenghel 
Stepunin 
Sukhodolskaia 
Sverzhenskii 

T
Talkovskaia 
Tamashevska 
Tereshchenko 
Tetiukov 
Tokmakoff 
Tomilin 
Topczewski 
Topezuvjw 
Topezuvjwa 
Trambetskaia 
Treshchev 
Trombetskaia 
Trubachev 
Trzemin 
Trzheminska 
Tsarev 
Tselikova 
Tsert 
Tsitov 
Turets 
Turetskii 

U
Ukhtomskii 
Umanskii 

V
Vans 
Vargunin 
Vasiliev 
Veis 
Veksler 
Verbukh 
Verden 
Veretennikov 
Vershvovski 
Vikentieva 
Vladimirskii 
Volynski 
Vorobiev 

W
Weinstein 
Werner 
Wittenburg 
Wolkowicz 
Wolowitz 
Worden 

Y
Yakunun 
Yunter 

Z
Zalesskii 
Zalicker 
Zeif 
Zelecker 
Zelichonok 
Zhalobovskaia 
Zheldak 
Zhelobovskaia 
Zilberman 
Zubkin 
Zukov 
Zukowskaia 
Zukowski
"""

FEMALE_FIRST_NAMES_RUSSIA = u"""

Adla
Adleida
Adlesha
Adleta
Adviga
Afanasiia
Afanasiya
Afimia
Afonaseva
Agafia
Agafiia
Agafiya
Agafokliia
Agafonika
Agafya
Agapiia
Agasha
Agashka
Aglaia
Aglaida
Aglaya
Agna
Agnessa
Agnia
Agniia
Agrafena
Agrafina
Agramakova
Agripena
Agripina
Agrippa
Agrippina
Aitugan
Aizdiakova
Akillina
Akiulina
Aksana
Aksinya
Alasa
Albena
Albina
Aleksandra
Alena
Alenka
Alexandra
Alexcia
Alexia
Alexis
Alina
Alma
Alona
Alyssa
Alzbeta
Amelfa
Ampliia
Ana
Anastasia
Anastasiia
Anastasija
Anatassia
Andreea
Andreeva
Andreiana
Andrievicha
Anechka
Aneska
Anfiia
Anfoma
Anfusa
Angelika
Angelina
Angusta
Ania
Animaida
Animaisa
Anina
Anisia
Anisiia
Anisiya
Anisya
Anitchka
Anitsa
Anizka
Anja
Anje
Anjelica
Anjelika
Anka
Ann
Anna
Annastasija
Antonidka
Antonina
Anusia
Anya
Anzhela
Apfiia
Apolinaria
Apolinariia
Apoloniada
Apolosakifa
Ariadna
Arina
Arkhipa
Arkhippa
Artemeva
Artemiia
Asenka
Askitreia
Askitriia
Asya
Augusta
Avdeeva
Avdiushka
Avdotia
Avgusta
Avramova
Baialyn
Baibichia
Bakhteiarova
Balbara
Barbara
Bazhena
Bedche
Bela
Beleka
Belgukovna
Belka
Bella
Belukha
Benka
Bezruchka
Bezubaia
Bezui
Biana
Biata
Bibishkina
Biiata
Biriuta
Blanka
Blausa
Bogdana
Bogukhvala
Bogumezt
Bogumila
Boguslava
Bohdana
Bohumile
Boika
Bolce
Boldina
Bolemila
Boleslava
Bolgarina
Bolgarynia
Bona
Borisova
Boriuta
Bozena
Bozhana
Bozhitsa
Bragina
Branislava
Branizlawa
Bratomila
Bratromila
Bratrumila
Bruna
Budisla
Budizla
Budshka
Budska
Bukhval
Calina
Catarina
Caterina
Catherine
Catina
Catreen
Catrin
Catrina
Catrinia
Catriona
Catryn
Cecislava
Charlotta
Chebotova
Chekhina
Chekhyna
Cheliadina
Chemislava
Chenka
Chernavka
Chernislava
Chernka
Chesislava
Chimislava
Chiona
Chiudka
Chobotova
Chynica
Ciernislava
Clavdia
Cyzarine
Czarina
Czeimislawa
Dalida
Daliunda
Dama
Danilova
Daria
Darina
Daritsa
Darja
Daromila
Darya
Dasha
Datja
Davyd
Davyzha
Davyzheia
Debora
Deda
Dedenia
Dekava
Dekhova
Demidova
Denicha
Deretka
Derska
Derzhena
Derzhka
Desa
Desha
Despa
Dessa
Desta
Detana
Detava
Deva
Devka
Devochka
Devochkina
Devora
Dikana
Dima
Dimitra
Dimut
Dina
Dinah
Dinara
Dmitreeva
Dmitrieva
Dmitrovna
Dobegneva
Dobislava
Dobka
Dobra
Dobrava
Dobreva
Dobromila
Dobroslava
Dobrowest
Dobryna
Doda
Domaslava
Dominika
Domka
Domna
Domnika
Domnikiia
Domnina
Domona
Dorofeia
Doroteya
Dosya
Dounia
Dozene
Dozhene
Draginia
Dragomira
Dragoslawa
Dragushla
Draia
Drga
Drosida
Druzhinina
Dubrava
Dubravka
Duklida
Dunya
Dunyasha
Duscha
Dusha
Dusya
Dvora
Ecatarina
Ecatrinna
Eda
Edviga
Edviva
Efdokia
Effimia
Efimia
Efiopskaia
Efrasiia
Efrosenia
Efrossina
Ekatarina
Ekaterina
Ekatrinna
Ekzuperiia
Elacha
Eleena
Elen
Eleni
Elenya
Elga
Elgiva
Eliaksha
Elikonida
Elina
Elisava
Elisaveta
Elissa
Elizabeth
Elizarova
Elizaveta
Ella
Ellena
Ellina
Elonka
Elzbeta
Elzhbeta
Ennafa
Epestemiia
Epikhariia
Epistima
Eretiia
Ermolina
Erotiida
Ertugana
Esineeva
Euafina
Eufemia
Eugenia
Euprakseia
Eupraksiia
Eva
Evanova
Evdokeia
Evdokia
Evdokiia
Evdokiya
Evdokseia
Evdoksiia
Evelina
Evfaliia
Evfrasiia
Evfroseniia
Evfrosinya
Evgenia
Evgeniia
Evgeniya
Evgenya
Evginia
Evguenia
Evpraksi
Evpraksiia
Evrosena
Evseevskaia
Evsegniia
Evseveia
Evseviia
Evstoliia
Evtropiia
Faina
Fanaila
Fanya
Fatianova
Fausta
Favsta
Fayina
Fedia
Fedka
Fedkina
Fedora
Fedoritsa
Fedorka
Fedorova
Fedosia
Fedosiia
Fedosya
Fedotia
Fedotiia
Fedya
Feia
Feiniia
Fekla
Feklitsa
Fenia
Feodora
Feodosia
Feodosiia
Feoduliia
Feofana
Feoklita
Feoktista
Feona
Feonilla
Feopimta
Feopista
Feopistiia
Feozva
Ferfufiia
Ferufa
Fesalonikiia
Fetenia
Fetinia
Fetiniia
Fevronia
Filikitata
Filippiia
Filitsata
Filofei
Filofinaia
Filonilla
Fimochka
Fiva
Fiveia
Foimina
Fokina
Fomina
Fotina
Fotiniia
Fovro
Fovroneia
Frolova
Frosiniia
Gadina
Gaianiia
Gala
Galenka
Gali
Galina
Galina
Galine
Galochka
Galya
Galyna
Gamana
Gana
Gananiia
Gandaza
Ganna
Gasha
Gema
Genka
Georgieva
Gertruda
Ginechka
Giurgevaia
Gizheurann
Gizla
Glafira
Glasha
Glebovicha
Glikeriia
Glikeriya
Glukeriia
Glukheria
Godava
Golindukha
Goltiaeva
Golubitsa
Gordislava
Gorislava
Gorshedna
Gostena
Gostenia
Gostiata
Gostimira
Goulislava
Govdela
Gravriia
Grekina
Grekinia
Grekyna
Grifina
Grigoreva
Grigorevna
Grigorieva
Groza
Gruba
Grunya
Grusha
Halyna
Helen
Helena
Helenka
Helga
Hema
Henka
Hinezka
Hinica
Hodawa
Hora
Horina
Hosche
Hostena
Hruoza
Iadviga
Iakova
Iakovleva
Iakovlevskaia
Iakun
Iakunova
Iakunovaia
Ianevaia
Ianisha
Ianishe
Ianka
Iarche
Iarena
Iarina
Iarogned
Iaroia
Iarokhna
Iaroslava
Iarshek
Iasynia
Ieliaia
Iev
Ievlia
Ifrosenia
Ignateva
Ignatevskaia
Igoshkova
Iia
Ilariia
Ilia
Ilina
Ilya
Inessa
Inkena
Inna
Ioanna
Iona
Iosifova
Iovilla
Ira
Iraida
Irena
Irene
Irina
Irinia
Irinka
Irisa
Irodia
Irodiia
Isakova
Isidora
Ismagrad
Itka
Iudita
Iuliana
Iuliania
Iulianiia
Iuliia
Iulita
Iulitta
Iuniia
Iurevna
Iustina
Ivana
Ivanova
Ivanovskaia
Iveska
Ivonne
Iziaslava
Izmaragd
Janna
Jarena
Jarene
Jarohna
Jekaterina
Jelena
Jelena
Jelizaveta
Jenica
Jeremia
Jevdokija
Jitka
Julia
Kace
Kacha
Kache
Kachka
Kala
Kaleria
Kaleriia
Kalia
Kalisa
Kalisfena
Kalista
Kalitina
Kallisfeniia
Kallista
Kamenka
Kamle
Kandaza
Kapetolina
Kaptelina
Karen
Karina
Karine
Karinna
Karolina
Karpova
Karpovskaia
Karrine
Karyna
Kasha
Kashka
Kata
Katalena
Katareena
Katarina
Kateena
Katerina
Katerinka
Katherina
Katherine
Katia
Katina
Katinka
Katiya
Katja
Katlina
Katreen
Katreena
Katrene
Katria
Katrien
Katrina
Katrine
Katrusha
Katrya
Katryn
Katryna
Kattrina
Kattryna
Katunia
Katuscha
Katya
Katyenka
Katyushka
Katyuska
Kazdoia
Kerkira
Kharesa
Khariessa
Kharitaniia
Kharitina
Kharitona
Kharitonova
Kheoniia
Khioniia
Khlopyreva
Khovra
Khrana
Khrisiia
Khristeen
Khristen
Khristianova
Khristin
Khristina
Khristine
Khristyana
Khristyna
Khrstina
Khrystina
Khrystyn
Khrystyne
Khvalibud
Khynika
Kikiliia
Kilikeia
Kilikiia
Kiprilla
Kira
Kiraanna
Kiriakiia
Kiriena
Kirilla
Kirilovskaia
Kisa
Kiska
Kitsa
Kittiana
Kiuprila
Kiuriakiia
Kiza
Klasha
Klavdiia
Kleopatra
Klychikha
Knikki
Kogorshed
Koia
Koika
Kolomianka
Konchaka
Konchasha
Konkordiia
Konstantiia
Konstiantina
Konstiantinova
Kora
Koretskaia
Korina
Korotkaia
Korotkova
Korotsek
Korotskovaia
Kosa
Kosenila
Kostenka
Kostya
Kostyusha
Kotik
Kovan
Kovana
Kowan
Kozma
Kozmina
Krabava
Krasa
Krestiia
Kristina
Krivulinaia
Krunevichovna
Krushka
Ksafipa
Ksana
Ksanfippa
Ksanochka
Ksenia
Kseniia
Kseniya
Ksenya
Kshtovtovna
Ksnia
Ksniatintsa
Kudra
Kuna
Kunei
Kunka
Kunko
Kunku
Kuntse
Kuriana
Kuznetsova
Kvasena
Kvetava
Kzhna
Lacey
Lacey
Lada
Laikina
Lala
Lanassa
Lanka
Lara
Lari
Larina
Larisa
Larissa
Larissa
Larochka
Larra
Laryssa
Latskaia
Leia
Leka
Lelik
Lena
Lenina
Lenochka
Lenora
Lenusy
Lenusya
Leonilla
Leonteva
Lepa
Lera
Lerka
Leva
Liba
Libania
Libusa
Lida
Lidena
Lidia
Lidiia
Lidija
Lidiy
Lidiya
Lidka
Lidmila
Lidocha
Lidochka
Lieba
Lila
Lilac
Lilia
Liolya
Lipa
Lisa
Lisanka
Lisaveta
Liseetsa
Lishka
Lisil
Liska
Lisotianka
Liuba
Liubchanina
Liubka
Liubokhna
Liubone
Liubusha
Liudena
Liudmila
Liunharda
Liutarda
Liutsilla
Liza
Lizabeta
Lizanka
Lizette
Ljudmila
Ljudmilla
Lolya
Lotta
Luba
Lubachitsa
Lubmila
Lubmilla
Lubohna
Lubov
Lubusha
Luda
Ludiia
Ludmia
Ludmila
Ludmilla
Ludomia
Luka
Lukeria
Lukerina
Lukerya
Lukiia
Lukina
Lukiria
Lukoianova
Lvovicha
Lyalechka
Lyalya
Lybed
Lydia
Lyeta
Lyuba
Lyubochka
Lyubonka
Lyubov
Lyudmila
Lyudmilla
Lyuha
Lyutsiana

Machko
Machna
Magdalina
Magmeteva
Maiya
Makhna
Makrina
Maksimina
Maksimova
Malana
Malania
Maliusha
Maliuta
Malka
Malona
Malonia
Maluchka
Malusha
Mamelfa
Mamika
Mana
Manechka
Manka
Manya
Mara
Marana
Maremiana
Marfa
Marfutka
Margarita
Margo
Maria
Marian
Marianna
Marianne
Marianskaia
Maricha
Marichinich
Mariia
Marimiana
Marina
Marinka
Marinochka
Marinskaia
Marionilla
Marisha
Maritanna
Maritsa
Marjka
Marka
Markiana
Marnie
Marous
Marta
Martemianova
Marufa
Marulia
Marusya
Marya
Mascha
Masha
Mashenka
Matfeitsa
Matrena
Matrona
Matruna
Matryoshka
Mavra
Maya
Mazcho
Melania
Melaniia
Meletina
Melita
Melitina
Menshikova
Mergivana
Merkureva
Miesha
Mika
Mikhaila
Mikhailova
Mikitina
Mikula
Mikulina
Mila
Milakhna
Milana
Milata
Milava
Milehva
Milekha
Milena
Milenia
Milesa
Mileva
Miliia
Milika
Militsa
Milka
Milleise
Milohna
Milokhna
Miloslava
Miloushka
Miluska
Minodora
Mira
Mirena
Mironova
Miropiia
Miroslava
Mirozlava
Mirra
Misha
Mitrodora
Mizinovskaia
Mlada
Moiko
Morava
Morawa
Mounya
Mousia
Mozyr
Mstislava
Mstislavliaia
Mudri
Muniia
Mura
Muroniia
Muza
Myrra
Myshka
Myslna
Nadeek
Nadeekovaia
Nadejda
Nadenka
Nadia
Nadie
Nadine
Nadiya
Nadja
Nadjenka
Nadya
Nadyenka
Nadysha
Nadyuiska
Naglaya
Na'Kesha
Nakita
Narkissa
Nastasia
Nastasich
Nastasiia
Nastasja
Nastassia
Nastenka
Nastia
Nastiona
Nastionka
Nastiusha
Nastka
Natachia
Natacia
Natalia
Nataliia
Natalja
Natalka
Natalya
Natascha
Natasha
Natashenka
Natashia
Natasia
Natassia
Nathasha
Nazarova
Nebracha
Nebraga
Neda
Nedana
Nedelia
Nekrasa
Nekrasia
Neliuba
Nemilka
Nemka
Neonila
Nesdits
Nesha
Nessa
Nesy
Neta
Netka
Neva
Neza
Nezhatok
Nezhdakha
Nezhka
Nifantova
Nika
Niki
Nikiforova
Nikita
Nikitina
Nikkylia
Nikolena
Niksha
Nimfodora
Nina
Ninel
Ninockha
Ninotchka
Nitasha
Nitca
Nona
Nonna
Nostasia
Nunekhiia
Nyura
Nyusha
Obrezkova
Odigitriia
Odintsova
Ofce
Ofimia
Ogafia
Ogafitsa
Ogashka
Ografena
Ogrifina
Ogrofena
Ogrufena
Ogrufina
Okinfieva
Oksana
Oksana
Oksanochka
Okseniia
Oksinia
Oksiutka
Oktyabrina
Okulina
Olechka
Oleksandra
Olena
Olenitsa
Olenka
Olfereva
Olga
Olginitsa
Olgirdovna
Olgov
Olimpiada
Olisava
Olivera
Olkha
Olya
Olzhbeta
Omelfa
Ondreiana
Onoslava
Ontonia
Ontsiforova
Ontsyforova
Oprosiniia
Orenka
Oria
Orina
Orlenda
Orlitza
Orsha
Orshinaia
Ortemeva
Orya
Osipova
Osliabia
Ostafia
Ostankova
Ostashkova
Osyenya
Ovdeeva
Ovdiukha
Ovdokea
Ovdotia
Ovdotitsa
Ovtsa
Oxana
Paladia
Palasha
Panfilova
Pansemna
Pantislava
Pantyslawa
Panya
Paraaha
Paramona
Parasha
Parasia
Paraskova
Paraskovga
Paraskovgiia
Paraskovia
Paraskoviia
Paroskova
Pasha
Patrova
Paula
Paulina
Pauline
Pavel
Pavla
Pavlova
Pavloveia
Pavlusha
Pchuneia
Pechta
Pelaga
Pelageia
Pelageya
Pelagiia
Perchta
Peredeslava
Perkhta
Perkhte
Perpetuia
Petronila
Petrova
Petrovna
Petsa
Peza
Pheodora
Piama
Piina
Piminova
Pirueva
Plakida
Platonida
Pokinaria
Poladia
Polazhitsa
Polia
Polikseniia
Polinaria
Poliuzhaia
Poloneika
Polotsk
Polotska
Poloudnitsa
Polovinova
Pomnislavka
Pompliia
Ponaria
Popliia
Popova
Poroskova
Poved
Praskovja
Praskovya
Prebrana
Predslava
Predyslava
Preia
Preksedys
Premislava
Prepedigna
Presthlava
Priba
Pribyslava
Priia
Prikseda
Priskilla
Priskula
Proksha
Proniakina
Prosdoka
Proskudiia
Przhibislava
Przybyslawa
Pukhleriia
Pulkheriia
Puna
Puteshineia
Putok
Putokoveia
Rada
Radia
Radivilovna
Radka
Rado
Radok
Radokhna
Radokovaia
Radonia
Radosha
Radoslava
Radosta
Radoste
Radozte
Radslava
Ragneda
Ragosna
Rahil
Raina
Raisa
Raiza
Rajna
Rakhiel
Ratka
Ratslava
Raya
Rechkina
Reicza
Reshunda
Richca
Richica
Richika
Richikha
Richtca
Richza
Riksa
Rima
Ripsimia
Rislava
Rita
Rogned
Roksana
Romanovna
Roscislawa
Roslava
Rossitza
Rostislava
Roza
Rozalia
Rozgneda
Rozhneva
Rufina
Rulza

Rusa
Rusna
Ryska
Sabina
Sacha
Sahsha
Samarina
Sanya
Sapozhnika
Sascha
Sashah
Sashana
Sashenka
Sashenka
Sashia
Sashka
Sausha
Savastian
Savastianova
Sbyslava
Selianka
Selivankov
Selivankova
Semenova
Semenovskaia
Semislava
Senia
Senny
Serafima
Sevastianiia
Sevastiiana
Severina
Sfandra
Shasha
Shcastna
Shchastna
Shedra
Shelovlevaya
Shiriaeva
Shkonka
Shura
Shushanika
Shvakova
Sidorova
Sima
Sina
Sinklitikiia
Siny
Sira
Siuiunbek
Siuiunbeka
Siuiunbuka
Siunbek
Siunbeka
Skameikina
Skonka
Slava
Slavna
Smils
Smina
Smirenka
Snanduliia
Snigurka
Sobina
Sofeia
Sofia
Sofiia
Sofiya
Sonaya
Sonechka
Sonia
Sonia
Sonja
Sonya
Sonyuru
Sonyusha
Sonyushka
Sophi
Sophia
Soroka
Sosanna
Sosfena
Sosipatra
Spasenieva
Spera
Spitoslava
Spitsislava
Stana
Stanislava
Stanka
Starsha
Stasy
Stasya
Stefanida
Stefanidka
Stefanova
Stefanya
Stepanida
Stepanova
Stephania
Stepka
Stesha
Stolma
Stolpolcha
Stopolcha
Stranizlava
Stratka
Strezhena
Strezhislava
Strezislava
Sudehna
Sudekhna
Sudila
Sulislava
Sumorokova
Sunklitikiia
Susana
Svakhna
Svatata
Svatava
Svatochna
Svatohna
Sveisla
Sveta
Svetlana
Svetocha
Svetokhna
Sviatata
Sviatokhna
Sviatoslava
Svoda
Swachnina
Swatawa
Symislava
Syp
Sypovaia
Tacha
Tachia
Tachiana
Tachianna
Tahn
Tahna
Tahnia
Tahniya
Tahnya
Tahsha
Taidula
Taina
Taisha
Taishineia
Taisiia
Tamara
Tamary
Tamera
Tamra
Tamryn
Tana
Tanalia
Tanasha
Tanaya
Tandula
Tanea
Tanechka
Taneya
Tania
Tanija
Tanita
Taniya
Tanja
Tanka
Tanna
Tannia
Tannis
Tanniya
Tannya
Tanya
Tasenka
Tasha
Tashana
Tashia
Tashiana
Tashianna
Tashina
Tashira
Tashiya
Tassa
Tasya
Tata
Tatiana
Tatianka
Tatianna
Tatiiana
Tatjana
Tatsa
Tatyana
Taunia
Taunya
Tavlunbeka
Tawnia
Tayna
Tazia
Teha
Tekh
Tekha
Tekusa
Tesheia
Teshka
Tetka
Tevkel
Tferianka
Thais
Thasha
Tiaga
Tina
Tishka
Tishkina
Titania
Titka
Tiutcheva
Tomila
Tomislava
Tonasha
Tonaya
Tonechka
Tonia
Tonja
Tonniya
Tonnya
Tonya
Torokanova
Toshiana
Tretiakovskaia
Troika
Trpena
Trufena
Tsaritsa
Tsvetkova
Tulna
Tutana
Tvoislava
Tvoyzlava
Ualentina
Uirko
Ulana
Uleia
Ulen'ka
Ulia
Uliaanitsa
Uliana
Ulianiia
Ulianka
Ulianushka
Uliasha
Uliiana
Ulita
Ulyana
Unefiia
Unka
Upritsa
Urshila
Ursula
Ustenia
Ustiniia
Vakhneva
Vakhtina
Valenta
Valentina
Valya
Vania
Vanmra
Vanya
Varenka
Varka
Varsonofia
Vartsislava
Varushka
Varvara
Varya
Varyusha
Vasileva
Vasilevna
Vasilevskaia
Vasilida
Vasilievaia
Vasilii
Vasilina
Vasilisa
Vasilissa
Vasilista
Vasisa
Vassa
Vassillissa
Vasya
Vaviia
Velika
Velislava
Ventseslava
Vera
Verochka
Veronika
Veronikeia
Vershina
Veruschka
Vetenega
Veveia
Viachenega
Victoria
Vida
Vika
Vikashenka
Viktoria
Viktoriya
Vila
Vilena
Vilenina
Vilma
Vilna
Virineia
Vironikiia
Vishemila
Vitalya
Vitasa
Vitko
Vitla
Vitoslava
Vivka
Vlada
Vladaia
Vladilena
Vladilenaova
Vladimira
Vladisava
Vladka
Vladlena
Vlaikha
Vlastika
Vlcena
Vlschet
Vogna
Voina
Voislava
Volodimerna
Volotka
Volotkoveia
Volotok
Vonda
Voyzlava
Vrata
Vratislava
Vrkhuslava
Vrotsislava
Vrsanka
Vseslava
Vukosava
Vukoslava
Vyesna
Vysheslava
Vyshia
Wannon
Warvara
Wava
Welislawa
Wierga
Wissa
Witoslava
Wiwka
Wladyka
Woina
Wrata
Wratislava
Wrocislawa
Xenia
Yalena
Yalenchka
Yalens
Yekaterina
Yelena
Yeva
Yevdokiya
Yevfrosinya
Yevgenya
Yogenya
Yovanka
Yulenka
Yulia
Yulianiya
Yulika
Yuliy
Yuliya
Yulya
Yusmara
Zabela
Zakharia
Zakharieva
Zakharina
Zamiatina
Zaneta
Zaritsa
Zasha
Zavidovicha
Zavorokhina
Zbina
Zbinka
Zbiska
Zbynek
Zbynko
Zbyshka
Zdena
Zdeslava
Zdislava
Zdzislaba
Zena
Zenaida
Zenaide
Zenechka
Zenochka
Zeny
Zenya
Zhanna
Zhdana
Zhena
Zhenya
Zhirava
Zhivana
Zhona
Zhonka
Zima
Zina
Zinaida
Zinerva
Zinoviia
Znata
Zofeia
Zoia
Zoika
Zoya
Zoyenka
Ztrezena
Zvatata
Zvenislava


"""

MALE_FIRST_NAMES_RUSSIA = u"""
Adrik
Akim
Alek
Aleksandr
Aleksi
Aleksis
Alexei
Alik
Aloyoshenka
Aloysha
Anatolii
Andrei
Andrusha
Andrya
Anstice
Antinko
Anton
Antosha
Arman
Avel
Bogdashha
Bohdan
Bolodenka
Boris
Boris
Boris
Borya
Boryenka
Brends
Brody
Burian
Cheslav
Czar
Danya
Demyan
Dima
Dimitri
Edik
Eduard
Egor
Egor
Evgenii
Fabi
Faddei
Fadey
Fadeyka
Fedor
Fedya
Fedyenka
Feliks
Filip
Fjodor
Fjodor
Foma
Fredek
Fyodor
Ganya
Gav
Gavrel
Gavrie
Gavril
Gavril
Gavrilovich
Gennadi
Gregori
Grigor
Grigori
Grigorii
Grisha
Hedeon
Helge
Igor
Igoryok
Ilya
Ioakim
Iov
Ivan
Ivano
Jascha
Jasha
Jeirgif
Jermija
Jov
Jurg
Karolek
Kiril
Kirill
Kliment
Konstantin
Konstantine
Kostya
Laurente
Leonide
Lev
Levka
Luka
Lukyan
Maks
Maksim
Maksimillian
Marko
Markov
Matvey
Matysh
Maxim
Michail
Mikhail
Mikhail
Misha
Mishe
Moriz
Motka
Naum
Nicolai
Nikolai
Oleg
Oleg
Olezka
Ony
Oral
Orel
Orell
Oriel
Orrel
Osip
Pabiyan
Pavel
Pavel
PavIpv
Pavlik
Pavlo
Pavlusha
Pavlushka
Pavlya
Petenka
Petrov
Petya
Pyotr
Roman
Romochka
Rurik
Rurik
Sacha
Sacha
Sanya
Sasha
Semyon
Serge
Sergei
Serguei
Seriozha
Seriozhenka
Sevastian
Shashenka
Shura
Shurik
Shurochka
Slavik
Stanislov

Stefan
Stephan
Stepka
Tamryn
Tasha
Tolenka
Tolya
Tosya
Tusya
Uri
Uriah
Urie
Ustin
Vadim
Valerii
Valerik
Vanechka
Vanya
Vanyusha
Vas
Vasilii
Vasily
Vassi
Vassily
Vasya
Viktor
Vitaliy
Vitenka
Vladik
Vladilen
Vladilen
Vladislav
Vladmir
Vladmiri
Vladya
Volody
Vyacheslav
Yakov
Yaremka
Yasha
Yefrem
Yerik
Yevgeni
Yura
Yuri
Yurii
Yurik
Yurochka
Zhenechka
Zhenya
Zhorah
Ziven
Zivon
Zory
"""

MALE_FIRST_NAMES_MUSLIM = u"""
Aabdeen
Aabid
Aadam
Aadil
Aaish
Aakif
Aamir
Aaqil
Aarif
Aasim
Aatif
Aayid
Abbaad
Abbaas
Abdul Azeez
Abdul Baari
Abdul Baasid
Abdul Fattaah
Abdul Ghafoor
Abdul Ghani
Abdul Haadi
Abdul Hai
Abdul Hakeem
Abdul Haleem
Abdul Hameed
Abdul Jabbaar
Abdul Jaleel
Abdul Kader
Abdul Kareem
Abdul Khaliq
Abdul Lateef
Abdul Maalik
Abdul Majeed
Abdul Noor
Abdul Qayyoom
Abdul Quddoos
Abdul Rauf
Abdul Waahid
Abdul Wadood
Abdul Wahaab
Abdullah
Abdur Raheem
Abdur Rahmaan
Abdur Raqeeb
Abdur Rasheed
Abdur Razzaaq
Abdus Salam
Abdus Samad
Abdut Tawwab
Abood
Abyad
Adeeb
Adham
Adnaan
Afeef
Ahmed
Aiman
Akram
Alawi
Ali
Amaan
Amaanullah
Ameen
Ameer
Amjad
Ammaar
Amru
Anas
Annnees
Anwar
Aqeel
Arafaat
Arhab
Arkaan
Arshad
Asad
Aseel
Asghar
Ashqar
Ashraf
Aslam
Asmar
Awad
Awf
Awn
Awni
Ayyoob
Azhaar
Azmi
Azzaam
Baahir
Baaqir
Baasim
Badr
Badraan
Badri
Badruddeen
Baheej
Bakar
Bandar
Basheer
Bassaam
Bassil
Bilaal
Bishr
Burhaan
Daamir
Daawood
Daif
Daifallah
Daleel
Dhaafir
Dhaahir
Dhaakir
Dhaki
Dhareef
Faadi
Faadil
Faai Z
Faaid
Faaiq
Faalih
Faaris
Faarooq
Faatih
Faatin
Fahd
Faheem
Fahmi
Faisal
Faraj
Farajallah
Fareed
Farhaan
Fateen
Fat'hi
Fawwaaz
Fawz
Fawzi
Fayyaad
Fikri
Fuaad
Furqaan
Ghaali
Ghaalib
Ghaamid
Ghaazi
Ghassaan
Haafil
Haajid
Haamid
Haani
Haarith
Haaroon
Haashid
Haashim
Haatim
Haazim
Haitham
Hakam
Hamad
Hamdaan
Hamdi
Hamood
Hamza
Haneef
Hanlala
Hasan
Hazm
Hibbaan
Hilaal
Hilmi
Hishaam
Hudhaifa
Humaid
Humaidaan
Huraira
Husaam
Husain
Husni
Ibrahim
Idrees
Ihaab
Ikram
Ilyaas
Imaad
Imraan
Irfaan
Isaam
Ishaaq
Ismad
Ismaeel
Iyaad
Izzaddeen
Izzat
Jaabir
Jaad
Jaadallah
Jaarallah
Jaasim
Jaasir
Jafar
Jalaal
Jam,Aan
Jamaal
Jameel
Jareer
Jasoor
Jawaad
Jawhar
Jihaad
Jiyaad
Jubair
Jumail
Junaid
Kaalim
Kaamil
Kaarim
Kabeer
Kaleem
Kamaal
Kamaaluddeen
Kameel
Kanaan
Katheer
Khaalid
Khairi
Khaleefa
Khaleel
Labeeb
Labeeb
Luqmaan
Lutfi
Luwai
Ma,Roof
Maahir
Maaiz
Maa'iz
Maajid
Maazin
Mahboob
Mahdi
Mahfooz
Mahmood
Mahuroos
Maisara
Maisoon
Majdi
Mamdooh
Mamoon
Mansoor
Marwaan
Marzooq
Mashal
Masood
Mastoor
Mawdood
Mazeed
Miqdaad
Miqdaam
Misfar
Mishaari
Moosha
Mu,Aawiya
Muaaid
Muammar
Mubarak
Mubashshir
Mudrik
Mufeed
Muhaajir
Muhammad
Muhsin
Muhyddeen
Mujahid
Mukarram
Mukhtaar
Mundhir
Muneeb
Muneef
Muneer
Munjid
Munsif
Muntasir
Murshid
Musaaid
Mus'ab
Musaddiq
Musheer
Mushtaaq
Muslih
Muslim
Mustaba
Mutammam
Mutasim
Mu'taz
Muthanna
Mutlaq
Muzammil
Naadir
Naaif
Naaji
Naasif
Naasiruddeen
Naazil
Naazim
Nabeeh
Nabeel
Nadeem
Nadheer
Najeeb
Najeem
Naseem
Naseer
Nashat
Nassaar
Nawaar
Nawf
Nawfal
Nazmi
Neeshaan
Nizaam
Nizaar
Noori
Nu'maan
Numair
Qaaid
Qaasim
Qais
Quraish
Qutb
Raadi
Raafi
Raaid
Raaji
Raakaan
Raamiz
Raashid
Rabi
Rafeeq
Raihaan
Rajaa
Rajab
Ramalaan
Ramzi
Rashaad
Rasheeq
Rayyaan
Razeen
Rida
Ridwaan
Rifaah
Rifat
Riyaal
Rushdi
Rushdi
Ruwaid
Saabiq
Saabir
Saadiq
Saahir
Saajid
Saalih
Saalim
Saami
Saamir
Sabaah
Sabri
Sad
Sadi
Sadoon
Saeed
Safar
Safwaan
Sahl
Saif
Sakeen
Salaah
Saleel
Saleem
Saleet
Salmaan
Samir
Saood
Saqr
Shaafi
Shaaheen
Shaahir
Shaakir
Shaamikh
Shaamil
Shabaan
Shaddaad
Shafeeq
Shaheed
Shaheed
Shaheer
Shakeel
Shameem
Shaqeeq
Sharaf
Sharaf
Shawqi
Shihaab
Shuaib
Shujaa
Shukri
Shuraih
Siddeeqi
Sidqi
Silmi
Siraaj
Sirajuddeen
Subhi
Sufyaan
Suhaib
Suhail
Sulaimaan
Sultan
Suwailim
Taaha
Taahir
Taaj
Taajuddeen
Taalib
Taamir
Taariq
Taiseer
Talaal
Talha
Tameem
Tammaam
Taqi
Tareef
Tawfeeq
Tawheed
Tayyib
Thaamir
Thaaqib
Tufail
Turki
Ubaida
Umair
Umar
Unais
Uqbah
Usaama
Uthmaa N
Uwais
Waail
Waatiq
Waddaah
Wajdi
Wajeeb
Wajeeh
Waleed
Waseef
Waseem
Wisaam
Yaasir
Ya'eesh
Yahya
Ya'qoob
Yoonus
Yoosuf
Yusri
Zaahid
Zaahir
Zaaid
Zaamil
Zaghlool
Zaid
Zaidaan
Zain
Zainuddeen
Zakariyya
Zaki
Zameel
Zayyaan
Ziyaad
Zubair
Zufar
Zuhair
Zuraara
"""

FEMALE_FIRST_NAMES_MUSLIM = u"""
Aadila
Aaida
Aaisha
Aamina
Aanisa
Aarifa
Aasima
Aasiya
Aatifa
Aatika
Aayaat
Abeer
Adeeba
Adhraaa
Afaaf
Afeefa
Afnaan
Afraah
Ahlaam
Aliyya
Almaasa
Amaani
Amal
Amatullah
Ameena
Ameera
Amniyya
Anbara
Aneesa
Aqeela
Ariyya
Arwa
Aseela
Asmaa
Atheer
Atiyya
Awaatif
Awda
Azeema
Azeeza
Azza
Fakeeha
Faraah
Fareeda
Farha
Farhaana
Farhat
Faseeha
Fateena
Fat'hiyaa
Fawqiyya
Fawzaana
Fawzia
Fidda
Fikra
Fikriyya
Firdaus
Fuaada
Gaitha
Ghaada
Ghaaliba
Ghaaliya
Ghaaziya
Ghaidaa
Ghazaala
Ghuzaila
Haafiza
Haajara
Haakima
Haala
Haamida
Haaniya
Haaritha
Haazima
Habeeba
Hadbaaa
Hadeel
Hadiyya
Hafsa
Haibaa
Haifaaa
Hakeema
Haleema
Hamaama
Hamda
Hamdoona
Hameeda
Hamna
Hamsa
Hanaaa
Hanaan
Haniyya
Hanoona
Hasana
Haseena
Hasnaa
Hawraa
Hazeela
Hiba
Hikma
Hilmiyya
Himma
Hishma
Hissa
Hiwaaya
Huda
Hujja
Humaina
Humaira
Husniyya
Huwaida
Ibtisaama
Iffat
Ilhaam
Imtinaan
Inaaya
Insaaf
Intisaar
Israa
Izza
Jadeeda
Jaleela
Jameela
Jannat
Jasra
Jawhara
Jeelaan
Juhaina
Jumaana
Jumaima
Juwairiya
Kaatima
Kaazima
Kabeera
Kameela
Kareema
Kawkab
Kawthar
Khaalida
Khadeeja
Khaira
Khairiya
Khaleela
Khawla
Khulood
Kifaaya
Kinaana
Kulthum
Laaiqa
Labeeba
Laila
Lateefa
Layaali
Lubaaba
Lubna
Lutfiyya
Maajida
Maariya
Maazina
Madeeha
Mahaa
Mahbooba
Mahdeeya
Mahdhoodha
Mahfoodha
Mahmooda
Maimoona
Maisara
Majdiyya
Majeeda
Maleeha
Maleeka
Manaahil
Manaal
Manaara
Mardiyya
Marjaana
Marwa
Marzooqa
Mas'ooda
Masroora
Mastoora
Mawhiba
Mawzoona
Mayyaada
Mazeeda
Minnah
Misbaah
Miska
Mubaaraka
Mubeena
Mudrika
Mufeeda
Mufliha
Muhjar
Mu'hsina
Mujaahida
Mumina
Mu'mina
Mumtaaza
Muna
Muneefa
Muneera
Munisa
Muntaha
Musfira
Musheera
Mushtaaqa
Mutee'a
Muzaina
Muzna
Naadiya
Naafoora
Naaifa
Naaila
Nabeeha
Nabeela
Nada
Nadeera
Nadheera
Nadiyya
Nafeesa
Nahla
Najaat
Najeeba
Najeema
Najiyya
Najlaa
Najma
Najwa
Nakheel
Nameera
Naqaa
Naqiyya
Naseeba
Naseefa
Naseema
Naseera
Nasreen
Nawaal
Nawaar
Nawfa
Nawwaara
Nazeeha
Nazeema
Nazmiyya
Nisma
Noora
Nooriyya
Nuha
Nu'ma
Nusaiba
Nuzha
Qaaida
Qamraaa
Qisma
Raabia
Raabiya
Raadiya
Raafida
Raaida
Raaniya
Rabdaa
Radiyya
Radwa
Rafeeda
Rafeeqa
Raheema
Rahma
Raihaana
Raita
Ramla
Ramza
Ramziyya
Randa
Rashaa
Rasheeda
Rasheeqa
Rawda
Rayyana
Razeena
Reema
Rif'a
Rifqa
Rihaab
Rumaana
Ruqayya
Rutaiba
Ruwaida
Saabiqa
Saabira
Saafiyya
Saahira
Saajida
Saaliha
Saalima
Saamiqa
Saamyya
Saara
Sabaaha
Sabeeha
Sabeeka
Sabiyya
Sabreen
Sabriyya
Sadeeda
Sadeeqa
Safaaa
Safiyya
Safwa
Sahar
Sahheeda
Sahla
Sajaa
Sajiyya
Sakeena
Saleema
Salma
Salwa
Sameeha
Sameera
Samraa
Sanaaa
Sanad
Sawada
Shaafia
Shaahida
Shaahira
Shaakira
Shaamila
Shabeeba
Shadhaa
Shafaaa
Shafee'a
Shafeeqa
Shahaada
Shahaama
Shaheera
Shahla
Shaimaaa
Shajee'a
Shakeela
Shakoora
Sham'a
Shamaail
Shameema
Shaqeeqa
Shareefa
Shukriyya
Siddeeqa
Sireen
Sitaara
Suhaa
Suhaad
Suhaila
Sukaina
Sulama
Sultana
Sumaita
Sumayya
Sumbula
Sundus
Taaliba
Taamira
Tahaani
Tahiyya
Tahleela
Tamanna
Tameema
Taqiyya
Tareefa
Tasneem
Tawfeeqa
Tawheeda
Tayyiba
Thaabita
Thaamira
Thamra
Thanaa
Tharwa
Tuhfa
Tulaiha
Turfa
Ulyaa
Umaima
Umaira
Ummu Kulthoom
Urwa
Waajida
Wadee'a
Wadha
Wafaaa
Waheeba
Waheeda
Wajdiyya
Wajeeha
Waleeda
Waliyya
Waneesa
Warda
Wardiyya
Waseema
Wasmaaa
Widdad
Yaasmeen
Yaasmeena
Zaahira
Zaaida
Zahra
Zahraaa
Zainab
Zaitoona
Zakiyya
Zarqaa
Zeena
Zubaida
Zuhaira
Zuhra
Zuhriyaa
Zulfa
Zumruda
"""

LAST_NAMES_MUSLIM = u"""
Abad
Abbas
Abbasi
Abdalla
Abdallah
Abdella
Abdelnour
Abdelrahman
Abdi
Abdo
Abdoo
Abdou
Abdul
Abdulla
Abdullah
Abed
Abid
Abood
Aboud
Abraham
Abu
Adel
Afzal
Agha
Ahmad
Ahmadi
Ahmed
Ahsan
Akbar
Akbari
Akel
Akhtar
Akhter
Akram
Alam
Ali
Allam
Allee
Alli
Ally
Aly
Aman
Amara
Amber
Ameen
Amen
Amer
Amin
Amini
Amir
Amiri
Ammar
Ansari
Anwar
Arafat
Arif
Arshad
Asad
Ashraf
Aslam
Asmar
Assad
Assaf
Atallah
Attar
Awan
Aydin
Ayoob
Ayoub
Ayub
Azad
Azam
Azer
Azimi
Aziz
Azizi
Azzam
Azzi
Bacchus
Baccus
Bacho
Baddour
Badie
Badour
Bagheri
Bahri
Baig
Baksh
Baluch
Bangura
Barakat
Bari
Basa
Basha
Bashara
Basher
Bashir
Baten
Begum
Ben
Beshara
Bey
Beydoun
Bilal
Bina
Burki
Can
Chahine
Dada
Dajani
Dallal
Daoud
Dar
Darwish
Dawood
Demian
Dia
Diab
Dib
Din
Doud
Ebrahim
Ebrahimi
Edris
Eid
Elamin
Elbaz
El-Sayed
Emami
Fadel
Fahmy
Fahs
Farag
Farah
Faraj
Fares
Farha
Farhat
Farid
Faris
Farman
Farooq
Farooqui
Farra
Farrah
Farran
Fawaz
Fayad
Firman
Gaber
Gad
Galla
Ghaffari
Ghanem
Ghani
Ghattas
Ghazal
Ghazi
Greiss
Guler
Habeeb
Habib
Habibi
Hadi
Hafeez
Hai
Haidar
Haider
Hakeem
Hakim
Halaby
Halim
Hallal
Hamad
Hamady
Hamdan
Hamed
Hameed
Hamid
Hamidi
Hammad
Hammoud
Hana
Hanif
Hannan
Haq
Haque
Hares
Hariri
Harron
Harroun
Hasan
Hasen
Hashem
Hashemi
Hashim
Hashmi
Hassan
Hassen
Hatem
Hoda
Hoque
Hosein
Hossain
Hosseini
Huda
Huq
Husain
Hussain
Hussein
Ibrahim
Idris
Imam
Iman
Iqbal
Irani
Ishak
Ishmael
Islam
Ismael
Ismail
Jabara
Jabbar
Jabbour
Jaber
Jabour
Jafari
Jaffer
Jafri
Jalali
Jalil
Jama
Jamail
Jamal
Jamil
Jan
Javed
Javid
Kaba
Kaber
Kabir
Kader
Kaiser
Kaleel
Kalil
Kamal
Kamali
Kamara
Kamel
Kanan
Karam
Karim
Karimi
Kassem
Kazemi
Kazi
Kazmi
Khalaf
Khalid
Khalifa
Khalil
Khalili
Khan
Khatib
Khawaja
Koroma
Laham
Latif
Lodi
Lone
Madani
Mady
Mahdavi
Mahdi
Mahfouz
Mahmood
Mahmoud
Mahmud
Majeed
Majid
Malak
Malek
Malik
Mannan
Mansoor
Mansour
Mansouri
Mansur
Maroun
Masih
Masood
Masri
Massoud
Matar
Matin
Mattar
Meer
Meskin
Miah
Mian

Mina
Minhas
Mir
Mirza
Mitri
Moghaddam
Mohamad
Mohamed
Mohammad
Mohammadi
Mohammed
Mohiuddin
Molla
Momin
Mona
Morad
Moradi
Mostafa
Mourad
Mousa
Moussa
Moustafa
Mowad
Muhammad
Muhammed
Munir
Murad
Musa
Mussa
Mustafa
Naderi
Nagi
Naim
Naqvi
Nasir
Nasr
Nasrallah
Nasser
Nassif
Nawaz
Nazar
Nazir
Neman
Niazi
Noor
Noorani
Noori
Nour
Nouri
Obeid
Odeh
Omar
Omer
Othman
Ozer
Parsa
Pasha
Pashia
Pirani
Popal
Pour
Qadir
Qasim
Qazi
Quadri
Raad
Rabbani
Rad
Radi
Radwan
Rafiq
Rahaim
Rahaman
Rahim
Rahimi
Rahman
Rahmani
Rais
Ramadan
Ramin
Rashed
Rasheed
Rashid
Rassi
Rasul
Rauf
Rayes
Rehman
Rehmann
Reza
Riaz
Rizk
Saab
Saad
Saade
Saadeh
Saah
Saba
Saber
Sabet
Sabir
Sadek
Sader
Sadiq
Sadri
Saeed
Safar
Safi
Sahli
Saidi
Sala
Salaam
Saladin
Salah
Salahuddin
Salam
Salama
Salame
Salameh
Saleem
Saleh
Salehi
Salek
Salem
Salih
Salik
Salim
Salloum
Salman
Samaan
Samad
Samara
Sami
Samra
Sani
Sarah
Sarwar
Sattar
Satter
Sawaya
Sayed
Selim
Semaan
Sesay
Shaban
Shabazz
Shad
Shaer
Shafi
Shah
Shahan
Shaheed
Shaheen
Shahid
Shahidi
Shahin
Shaikh
Shaker
Shakir
Shakoor
Sham
Shams
Sharaf
Shareef
Sharif
Shariff
Sharifi
Shehadeh
Shehata
Sheikh
Siddiqi
Siddique
Siddiqui
Sinai
Soliman
Soltani
Srour
Sulaiman
Suleiman
Sultan
Sultana
Syed
Sylla
Tabatabai
Tabet
Taha
Taheri
Tahir
Tamer
Tariq
Tawil
Toure
Turay
Uddin
Ullah
Usman
Vaziri
Vohra
Wahab
Wahba
Waheed
Wakim
Wali
Yacoub
Yamin
Yasin
Yassin
Younan
Younes
Younis
Yousef
Yousif
Youssef
Yousuf
Yusuf
Zadeh
Zafar
Zaher
Zahra
Zaidi
Zakaria
Zaki
Zaman
Zamani
Zia

"""



def streets_of_liege():
    def fn():
        #~ streets = []
        for ln in STREETS_OF_LIEGE.splitlines():
            if ln and ln[0] == '*':
                m = re.match(STREET_RE, ln)
                if m:
                    s = m.group(1).strip()
                    if '|' in s:
                        s = s.split('|')[1]
                    yield s
                    #~ streets.append(s)
    return Cycler(fn())

            
LAST_NAMES_RUSSIA = Cycler(splitter1(LAST_NAMES_RUSSIA))
MALE_FIRST_NAMES_RUSSIA = Cycler(splitter1(MALE_FIRST_NAMES_RUSSIA))
FEMALE_FIRST_NAMES_RUSSIA = Cycler(splitter1(FEMALE_FIRST_NAMES_RUSSIA))

#~ def last_names_russia():
    #~ return Cycler(splitter1(LAST_NAMES_RUSSIA))
#~ def male_first_names_russia():
    #~ return Cycler(splitter1(MALE_FIRST_NAMES_RUSSIA))
#~ def female_first_names_russia():
    #~ return Cycler(splitter1(FEMALE_FIRST_NAMES_RUSSIA))
            
LAST_NAMES_MUSLIM = Cycler(splitter1(LAST_NAMES_MUSLIM))
MALE_FIRST_NAMES_MUSLIM = Cycler(splitter1(MALE_FIRST_NAMES_MUSLIM))
FEMALE_FIRST_NAMES_MUSLIM = Cycler(splitter1(FEMALE_FIRST_NAMES_MUSLIM))

#~ def last_names_muslim():
    #~ return Cycler(splitter1(LAST_NAMES_MUSLIM))
#~ def male_first_names_muslim():
    #~ return Cycler(splitter1(MALE_FIRST_NAMES_MUSLIM))
#~ def female_first_names_muslim():
    #~ return Cycler(splitter1(FEMALE_FIRST_NAMES_MUSLIM))

      
LAST_NAMES_BELGIUM = Cycler(splitter1(LAST_NAMES_BELGIUM))
MALE_FIRST_NAMES_FRANCE = Cycler(splitter2(MALE_FIRST_NAMES_FRANCE))
FEMALE_FIRST_NAMES_FRANCE = Cycler(splitter2(FEMALE_FIRST_NAMES_FRANCE))

#~ def last_names_belgium():
    #~ return Cycler(splitter1(LAST_NAMES_BELGIUM))
#~ def male_first_names_france():
    #~ return Cycler([name.strip() for name in MALE_FIRST_NAMES_FRANCE.split(',')])
#~ def female_first_names_france():
    #~ return Cycler([name.strip() for name in FEMALE_FIRST_NAMES_FRANCE.split(',')]))
    
#~ def belgians():
    #~ yield [
      #~ LAST_NAMES_BELGIUM.pop(),
      #~ MALE_FIRST_NAMES_FRANCE.pop(),
      #~ FEMALE_FIRST_NAMES_FRANCE.pop()]
      
#~ def muslims():
    #~ yield [
      #~ LAST_NAMES_MUSLIM.pop(),
      #~ MALE_FIRST_NAMES_MUSLIM.pop(),
      #~ FEMALE_FIRST_NAMES_MUSLIM.pop()]
      
#~ def russians():
    #~ yield [
      #~ LAST_NAMES_RUSSIA.pop(),
      #~ MALE_FIRST_NAMES_RUSSIA.pop(),
      #~ FEMALE_FIRST_NAMES_RUSSIA.pop()]
      
if False:
    last_names = []
    for ln in demo.LAST_NAMES_FRANCE.splitlines():
        if ln:
            a = ln.split()
            if len(a) == 3:
                last_names.append(a[0].strip())
            elif len(a) == 4:
                last_names.append(a[0].strip()+' '+a[1].strip())




def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

