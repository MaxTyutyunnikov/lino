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
Fills the cbss.Purposes table from 
http://www.bcss.fgov.be/binaries/documentation/fr/documentation/general/lijst_hoedanigheidscodes.pdf

"""

from lino.utils.babel import babel_values
from lino.tools import resolve_model

#~ SECTORS = u"""
#~ 1 Fonds des accidents du travail | Fonds voor arbeidsongevallen | 
#~ 5 Office national des pensions | Rijksdienst voor pensioenen | 
#~ 6 Fonds des maladies professionnelles | Fonds voor beroepsziekten | 
#~ 7 Office national d’allocations familiales pour travailleurs salariés | Rijksdienst voor kinderbijslag voor werknemers | 
#~ 9 Caisse de secours et de prévoyance en faveur des marins | Hulp- en voorzorgskas voor zeevarenden | 
#~ 10 Office National des vacances annuelles | Rijksdienst voor jaarlijkse vakantie | 
#~ 11 Soins de santé | Gezondheidszorg | 
#~ 12 Office National de Sécurité Sociale | Rijksdienst voor Sociale Zekerheid | 
#~ 13 ONSS des administrations provinciales et locales | rsz van de provinciale en plaatselijke overheidsdiensten | 
#~ 14 SIGEDIS | SIGEDIS | 
#~ 15 Institut National d’Assurances sociales pour travailleurs indépendants | Rijksinstituut voor de sociale verzekeringen der zelfstandigen | 
#~ 16 SPF Sécurité sociale  | FOD Sociale zekerheid | 
#~ 17 Centre Public d’Action Sociale | Openbaar Centrum voor Maatschappelijk Welzijn | Öffentliches Sozialhilfezentrum
#~ 18 Office National de l’Emploi | Rijksdienst voor arbeidsvoorzienning | 
#~ 19 SPF Santé publique et environnement | FOD Volksgezondheid en leefmilieu | 
#~ """

PURPOSES = u"""
1 10 INDEMNISATION AUX VICTIMES | VERGOEDING AAN SLACHTOFFERS
1 20 RENTES DES AYANTS DROIT  | RENTEN AAN RECHTHEBBENDEN
1 30 PAIEMENTS À DES TIERS & AUTRES CORRESPONDANTS | BETALINGEN AAN DERDEN EN ANDERE CORRESPONDENTEN
1 40 TRAVAILLEURS ASSIMILÉS - CARRIÈRE INCOMPLÈTE | GELIJKGESTELDE WERKNEMERS - ONVOLLEDIGE LOOPBAAN
1 50 Débiteurs  | debiteuren
5 1 PREMIER CONTACT  | EERSTE CONTACT
5 10 DOSSIER ESTIMATION  | RAMINGDOSSIER
5 20 DOSSIER ATTRIBUTION  | TOEKENNINGSDOSSIER
5 30 ATTRIBUTION GRAPA  | TOEKENNING IGO
5 31 COHABITANT GRAPA  | SAMENWONENDE IGO
5 100 DOSSIER PAIEMENT  | BETALINGSDOSSIER
5 110 DOSSIER PAIEMENT RESIDUAIRE  | BETALINGSDOSSIER RESIDUAIR RECHT
5 150 DOSSIER CADASTRE  | DOSSIER KADASTER
5 500 Dossier échange bilatéral  | Dossier bilaterale uitwisseling
6 10 INDEMNISATION AUX VICTIMES  | VERGOEDING AAN SLACHTOFFERS
6 20 RENTES DES AYANTS DROIT  | RENTEN AAN RECHTHEBBENDEN
6 30 PAIEMENTS À DES TIERS & AUTRES CORRESPONDANTS | BETALINGEN AAN DERDEN EN ANDERE CORRESPONDENTEN
6 40 TRAVAILLEURS ASSIMILÉS - CARRIÈRE INCOMPLÈTE | GELIJKGESTELDE WERKNEMERS - ONVOLLEDIGE LOOPBAAN
6 50 FEMME ENCEINTE ECART2E  | VERWIJDERDE ZWANGERE VROUW
7 101 BÉNÉFICIAIRE  | RECHTHEBBENDE
7 102 ALLOCATAIRE TYPE 1  | BIJSLAGTREKKENDE TYPE 1
7 103 ALLOCATAIRE TYPE 2  | BIJSLAGTREKKENDE TYPE 2
7 104 ENFANT BÉNÉFICIAIRE  | RECHTGEVEND KIND
7 105 TIERCE PERSONNE TYPE 1  | DERDE PERSOON TYPE 1
7 106 TIERCE PERSONNE TYPE 2  | DERDE PERSOON TYPE 2
7 107 PERSONNE EN RECHERCHE  | PERSOON IN ONDERZOEK
9 2 AYANT DROIT À UNE INTERVENTION MAJORÉE DE L’ASSURANCE SOINS DE SANTÉ (TITULAIRE OU BÉNÉFICIAIRE) | RECHTHEBBENDE OP VERHOOGDE TUSSENKOMST IN HET KADER VAN DE GEZONDHEIDSZORG (TITULARIS OF GERECHTIGDE)
9 12 AYANT DROIT À UNE INTERVENTION MAJORÉE DE L’ASSURANCE SOINS DE SANTÉ (PERSONNE À CHARGE) | RECHTHEBBENDE OP VERHOOGDE TUSSENKOMST IN HET KADER VAN DE GEZONDHEIDSZORG (PERSOON TEN LASTE)
10 10 OUVRIER | ARBEIDER
11 1 ASSURABILITÉ SOINS DE SANTÉ | VERZEKERBAARHEID GENEESKUNDIGE VERZORGING
11 2 PERSONNE AVEC DOSSIER INDEMNITÉ | PERSOON MET DOSSIER ARBEIDSONGESCHIKTHEID
12 2 MEMBRE DU PERSONNEL | PERSONEELSLID
12 10 SALARIÉ | WERKNEMER
12 30 DIMONA | DIMONA
12 40 ENQUETE EMPLOYEUR | ONDERZOEK WERKGEVER
13 10 TRAVAILLEUR | WERKNEMER
13 30 DIMONA | DIMONA
14 10 SALARIÉ AVEC TENUE DE COMPTE PENSION | WERKNEMER MET PENSIOENREKENING
14 21 SALARIÉ SANS TENUE DE COMPTE PENSION | WERKNEMER ZONDER PENSIOENREKENING
14 30 TRAVAILLEUR POUR QUI UNE DÉCLARATION DIMONA A ÉTÉ FAITE | WERKNEMER VOOR WIE EEN DIMONA-AANGIFTE WERD VERRICHT
14 50 Carrière fonctionnaires, employées contractuels | Loopbaan ambtenaren, contractuele werknemers
15 1 DOSSIER EN EXAMEN  | DOSSIER IN ONDERZOEK
15 2 STATUT SOCIAL DE TRAVAILLEUR INDÉPENDANT | SOCIAAL STATUUT VAN ZELFSTANDIGE
15 3 BÉNÉFICIAIRE DES ALLOCATIONS FAMILIALES SECTEUR INDÉPENDANTS | RECHTGEVEND KIND OP GEZINSBIJSLAG SECTOR ZELFSTANDIGEN
15 6 (EX-)CONJOINT DE L’INDÉPENDANT, AYANT DROIT DANS LE STATUT SOCIAL DES INDÉPENDANTS | (EX-)PARTNER VAN DE ZELFSTANDIGE, RECHTHEBBENDE IN HET SOCIAAL STATUUT DER ZELFSTANDIGEN
15 7 ACTEUR QUI PEUT INFLUENCER LA DETERMINATION DU DROIT AUX PRESTATIONS FAMILIALES | ACTOR DIE EEN INVLOED KAN UITOEFENEN OP HET BEPALEN VAN HET RECHT OP GEZINSBIJSLAG
15 8 ALLOCATAIRE (PRESTATIONS FAMILIALES) | BIJSLAGTREKKENDE (GEZINSBIJSLAG)
16 1 PERSONNE HANDICAPÉE (ALLOCATION)  | PERSOON MET EEN HANDICAP (TEGEMOETKOMING)
16 2 ENFANT HANDICAPÉ  | KIND MET EEN HANDICAP
16 3 RECONNAISSANCE MEDICALE  | MEDISCHE ERKENNING
16 4 PERSONNE AVEC LAQUELLE LA PERSONNE HANDICAPÉE FORME UN MÉNAGE | PERSOON MET WIE DE PERSOON MET EEN HANDICAP EEN GEZIN VORMT
16 5 DOSSIER BENEFICIAIRE D’UNE ALLOCATION D’INTEGRATION / ALLOCATION DE REMPLACEMENT DE REVENU | DOSSIER GERECHTIGDE OP INKOMENSVERVANGENDE TEGEMOETKOMING / INTEGRATIETEGEMOETKOMING
16 6 PERSONNE FAISANT PARTIE DU MENAGE D’UNE PERSONNE HANDICAPEE BENEFICIANT D’UNE ALLOCATION D’INTEGRATION / ALLOCATION DE REMPLACEMENT DE REVENU | PERSOON DIE EEN HUISHOUDEN VORMT MET DE PERSOON MET EEN HANDICAP IN HET KADER VAN EEN DOSSIER INKOMENSVERVANGENDE TEGEMOETKOMING / INTEGRATIETEGEMOETKOMING
16 7 DOSSIER BENEFICIAIRE D’UNE ALLOCATION D’AIDE AUX PERSONNES AGEES | DOSSIER GERECHTIGDE OP TEGEMOETKOMING VOOR HULP AAN BEJAARDEN
16 8 PERSONNE FAISANT PARTIE DU MENAGE D’UNE PERSONNE HANDICAPEE BENEFICIANT D’UNE ALLOCATION D’AIDE AUX PERSONNES AGEES | PERSOON DIE HUISHOUDEN VORMT MET DE PERSOON MET EEN HANDICAP IN HET KADER VAN DE TEGEMOETKOMING VOOR HULP AAN BEJAARDEN
18 1 CHÔMEUR CONTRÔLÉ | GECONTROLEERDE WERKLOZE
18 2 TRAVAILLEUR EN INTERRUPTION DE CARRIÈRE | WERKNEMER IN LOOPBAANONDERBREKING
18 3 TRAVAILLEUR VICTIME D’UNE FERMETURE D’ENTREPRISE | WERKNEMER SLACHTOFFER VAN EEN SLUITING VAN EEN ONDERNEMING
18 4 DEMANDEUR D’EMPLOI  | WERKZOEKENDE
18 5 MEMBRE DU PERSONNEL ONEM  | PERSONEELSLID RVA
19 1 DOSSIER ACTIF  | ACTIEF DOSSIER
19 2 DOSSIER INACTIF  | NIET-ACTIEF DOSSIER
19 10 MÉDECIN  | GENEESHEER
19 20 PHARMACIEN  | APOTHEKER
19 21 ASSISTANT-PHARMACEUTICA-TECHNIQUE  | FARMACEUTISCH-TECHNISCH ASSISTENT
19 30 DENTISTE  | TANDARTS
19 40 ACCOUCHEUSE  | VROEDVROUW
19 41 INFIRMIER  | VERPLEGER
19 42 AIDE-SOIGNANT  | ZORGKUNDIGE
19 50 KINÉSITHÉRAPEUTE  | KINESITHERAPEUT
19 51 ORTHESISTE  | ORTHESIST
19 54 PROTHESISTE  | PROTHESIST
19 57 AUDIOLOGUE  | AUDIOLOOG
19 58 LOGOPÈDES  | LOGOPEDISTEN
19 59 ORTHOPTISTES  | ORTHOPTISTEN
19 60 PODOLOGUE  | PODOLOOG
19 61 ORTHOPÉDISTES  | ORTHOPEDISTEN
19 62 BANDAGISTES  | BANDAGISTEN
19 63 DISPENSATEURS D’IMPLANTS  | VERSTREKKERS VAN IMPLANTATEN
19 64 ERGOTHÉRAPEUTE  | ERGOTHERAPEUT
19 65 DIÉTÉTICIEN  | DIETIST
19 66 OPTICIENS  | OPTICIENS
19 67 AUDICIENS  | AUDICIENS
19 68 PHARMACIENS BIOLOGISTES  | APOTHEKERS-BIOLOGEN
19 69 TECHNOLOGUE DE LABORATOIRE  | LABORATORIUMTECHNOLOOG
19 70 PUÉRICULTRICE  | KINDERVERZORGSTER
19 71 TECHNOLOGUE EN IMAGERIE MEDICALE  | TECHNOLOOG MEDISCHE BEELDVORMING
19 80 AMBULANCIER (TRANSPORT NON-URGENT DE PATIENT) | AMBULANCIER (NIET-DRINGEND PATIENTENVERVOER )
19 99 PROFESSIONNEL DE SANTE POTENTIEL  | POTENTIELE GEZONDHEIDSZORGBEOEFENAAR

*  902 Inscription provisoire | Voorlopige inschrijving | Provisorische Einschreibung
*  999 NISS remplacé | INSZ vervangen | NISS ersetzt
*  0   Inscription définitive | Definitieve inschrijvinG | Definitive Einschreibung
17 1 Dossier en examen | Dossier in onderzoek | Akte in Untersuchung
17 2 Revenu d’intégration | Leefloon | Eingliederungseinkommen
17 3 Équivalent revenu d’intégration | Equivalent leefloon | Gleichgestelltes Eingliederungseinkommen
17 4 Autre aide | Andere hulp | Sonstige Hilfe
17 5 Cohabitant | Inwonende | Mitbewohner
17 6 Personne occupée par le biais d’un CPAS | Persoon tewerkgesteld via OCMW | Durch das ÖSHZ beschäftigte Person
17 7 Médiation collective de dettes / accompagnement budgétaire | Collectieve schuldbemiddeling / budgetbegeleiding | Schuldnerberatung
17 8 Dossiers de service | Dienstendossier | Dienstakte
17 9 Autres formes d’accompagnement | Andere vormen van begeleiding | Sonstige Begleitungsformen
17 11 Encadrant | Encadrant | Begleiter
17 12 Participant | Deelnemer | Teilnehmer
17 20 Collaborateur en enquête | Medewerker in onderzoek | Mitarbeiter auf Probe
17 21 Collaborateur (définitif) | Medewerker (definitif) | Mitarbeiter (definitiv)
17 40 Bénéficiaire de l’allocation de chauffage | Begunstigde verwarmingstoelage | Heizkostenbeihilfe
"""

def objects():
    Sector = resolve_model('cbss.Sector')
    #~ for ln in SECTORS.splitlines():
        #~ if ln:
            #~ a = ln.split(None,1)
            #~ labels = [s.strip() for s in a[1].split('|')]
            #~ if len(labels) != 3:
                #~ raise Exception("Line %r : labels is %r" %(ln,labels))
            #~ if not labels[2]:
                #~ labels[2] = labels[0]
            #~ yield Sector(code=int(a[0]),**babel_values('name',fr=labels[0],nl=labels[1],de=labels[2]))
            
    Purpose = resolve_model('cbss.Purpose')
    for ln in PURPOSES.splitlines():
        if ln:
            a = ln.split(None,2)
            #~ assert a[0] in ('*', '17')
            sc = a[0]
            if sc == '*': 
                sc = None
            else:
                #~ sector = Sector.objects.get(code=int(sc))
                sc = int(sc)
            labels = [s.strip() for s in a[2].split('|')]
            if len(labels) == 2:
                labels.append(labels[0])
            elif len(labels) != 3:
                raise Exception("Line %r : labels is %r" %(ln,labels))
            yield Purpose(sector_code=sc,code=int(a[1]),**babel_values('name',fr=labels[0],nl=labels[1],de=labels[2]))
            