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
Inserts the "INS codes" to Cities and Countries
"""

#~ import logging
#~ logger = logging.getLogger(__name__)


from django.conf import settings
from lino.utils.babel import babel_values
from lino.tools import resolve_model
from lino.utils import dblogger as logger



COUNTRIES = '''
101 'Albanie', 'Albanië', 'Albanien'
102 'Andorre', 'Andorra', 'Andorra'
103 'Allemagne (Rép.féd.)', 'Duitsland (Bondsrep.)', 'Deutschland (Bundesrep.)'
104 'Allemagne (Rép. dém.)', 'Duitsland (Dem. rep.)', 'Deutschland (Dem. Rep.)'
105 'Autriche', 'Oostenrijk', 'Österreich'
106 'Bulgarie', 'Bulgarije', 'Bulgarien'
107 'Chypre', 'Cyprus', 'Zypern'
108 'Danemark', 'Denemarken', 'Dänemark'
109 'Espagne', 'Spanje', 'Spanien'
110 'Finlande', 'Finland', 'Finnland'
111 'France', 'Frankrijk', 'Frankreich'
112 'Royaume-Uni', 'Verenigd Koninkrijk', 'Vereinigtes Königreich'
113 'Luxembourg (Grand-Duché)', 'Luxemburg (Groot-Hertogdom)', 'Luxemburg (Grossherzogtum)'
114 'Grèce', 'Griekenland', 'Griechenland'
115 'Hongrie ( Rép. )', 'Hongarije ( Rep. )', 'Ungarn ( Rep. )'
116 'Irlande', 'Ierland', 'Irland'
117 'Islande', 'Ijsland', 'Island'
118 'Liechtenstein', 'Liechtenstein', 'Liechtenstein'
119 'Malte', 'Malta', 'Malta'
120 'Monaco', 'Monaco', 'Monaco'
121 'Norvège', 'Noorwegen', 'Norwegen'
122 'Pologne ( Rép. )', 'Polen ( Rep. )', 'Polen ( Rep. )'
123 'Portugal', 'Portugal', 'Portugal'
124 'Roumanie', 'Roemenië', 'Rumänien'
125 'Saint-Marin', 'San Marino', 'San Marino'
126 'Suède', 'Zweden', 'Schweden'
127 'Suisse', 'Zwitserland', 'Schweiz'
128 'Italie', 'Italië', 'Italien'
129 'Pays-Bas', 'Nederland', 'Niederlande'
130 'Tchécoslovaquie', 'Tsjecho-Slovakije', 'Tschechoslowakei'
131 'Union d.Rép.Soc.Soviét.', 'Unie d. Socialist. Sovjetrep.', 'Un.der Sozialist. Sowjetrep.'
132 'Serbie-et-Monténégro', 'Servië en Montenegro', 'Serbien und Montenegro'
133 'Cité du Vatican (Saint-Siège)', 'Vatikaanstad (Heilige Stoel)', 'Vatikanstadt (Heiliger Stuhl)'
134 'Allemagne', 'Duitsland', 'Deutschland'
135 'Lettonie', 'Letland', 'Lettland'
136 'Estonie', 'Estland', 'Estland'
137 'Lituanie', 'Litouwen', 'Litauen'
138 'Hongrie(République)', 'Hongarije(Republiek)', 'Ungarn (Republik)'
139 'Pologne(République)', 'Polen(Republiek)', 'Polen(Republik)'
140 'République Tchèque', 'Tsjechische Republiek', 'Tschechische Republik'
141 'Slovaquie', 'Slowakije', 'Slowakei'
142 'Bélarus', 'Wit-Rusland', 'Weissrussland'
143 'Ukraine', 'Oekraïne', 'Ukraine'
144 'Moldova (Rép de)', 'Moldavië (Rep)', 'Moldau (Rep)'
145 'Fédération de Russie', 'Russische Federatie', 'Russische Föderation'
146 'Croatie', 'Kroatië', 'Kroatien'
147 'Slovénie', 'Slovenië', 'Slowenien'
148 'Macédoine (Ex-République yougoslave de)', 'Macedonië (Voorm. Joegoslavische Rep.)', 'Mazedonien(ehemalige jugoslawische Rep)'
149 'Bosnie-Herzégovine', 'Bosnië en Herzegovina', 'Bosnien und Herzegowina'
150 'Belgique', 'België', 'Belgien'
151 'Monténégro', 'Montenegro', 'Montenegro'
152 'Serbie', 'Servië', 'Serbien'
153 'Kosovo', 'Kosovo', 'Kosovo'
169 'Yougoslavie', 'Joegoslavië', 'Jugoslawien'
170 'Allemagne ( Rép. dém. )', 'Duitsland ( Dem. rep. )', 'Deutschland ( Dem. Rep. )'
171 'Tchécoslovaquie', 'Tsjecho-Slowakije', 'Tschechoslowakei'
172 'Union d. Rép. Soc. Soviét.', 'Unie d. Socialist. Sovjetrep.', 'Un. der Sozialist. Sowjetrep.'
173 'Allemagne', 'Duitsland', 'Deutschland'
180 'Gibraltar (Royaume-Uni)', 'Gibraltar (Verenigd Koninkrijk)', 'Gibraltar (Vereinigtes Königreich)'
201 'Myanmar (Union de)', 'Myanmar (Unie van)', 'Myanmar (Union)'
202 'Rép. Khmer du Cambodge', 'Khmerische Rep. Cambodja', 'Khmerische Rep. (Kambodscha)'
203 'Sri Lanka', 'Sri Lanka', 'Sri Lanka'
204 'Taïwan', 'Taiwan', 'Taiwan'
205 'Singapour', 'Singapore', 'Singapur'
206 'Corée du Sud (République de)', 'Zuid-Korea (Republiek)', 'Südkorea (Republik)'
207 'Inde', 'India', 'Indien'
208 'Indonésie', 'Indonesië', 'Indonesien'
209 'Japon', 'Japan', 'Japan'
210 'Laos(république démocratique populaire)', 'Laos (Democratische Volksrepubliek)', 'Laos (Demokratische Volksrepublik)'
211 'Cambodge', 'Cambodja', 'Kambodscha'
212 'Malaisie', 'Maleisië', 'Malaysia'
213 'Népal', 'Nepal', 'Nepal'
214 'Philippines', 'Filipijnen', 'Philippinen'
215 'Timor-Leste (République démocratique)', 'Oost-Timor (Democratische Republiek)', 'Timor-Leste (Demokratische Republik)'
216 'Cambodge(Royaume du)', 'Cambodja(Koninkrijk)', 'Kambodscha(Königreich)'
217 'Vietnam du Sud', 'Zuid-Viëtnam', 'Südvietnam'
218 'Chine', 'China', 'China'
219 'Corée du Nord (Rép. pop. dém. de)', 'Noord-Korea (Dem. Volksrep.)', 'Nordkorea (Demokratische Volksrepublik)'
220 'République socialiste du Vietnam', 'Socialistische Republiek Vietnam', 'Sozialistische Republik Vietnam'
221 'Mongolie', 'Mongolië', 'Mongolei'
222 'Maldives', 'Maldiven', 'Malediven'
223 'Bhoutan', 'Bhutan', 'Bhutan'
224 'Brunéi Darussalam', 'Brunei Darussalam', 'Brunei Darussalam'
225 'Kazakhstan', 'Kazachstan', 'Kasachstan'
226 'Kirghizistan', 'Kirgizstan', 'Kirgisistan'
227 'Ouzbékistan', 'Oezbekistan', 'Usbekistan'
228 'Tadjikistan', 'Tadzjikistan', 'Tadschikistan'
229 'Turkménistan', 'Turkmenistan', 'Turkmenistan'
230 'Chine(Hong-Kong SAR)', 'China(Hongkong SAR)', 'China(Hong Kong SAR)'
231 'Chine(Macao SAR)', 'China(Macau SAR)', 'China(Macau SAR)'
234 'Hong-Kong', 'Hong-Kong', 'Hong-Kong'
235 'Thaïlande', 'Thailand', 'Thailand'
237 'Bangladesh', 'Bangladesh', 'Bangladesch'
249 'Arménie', 'Armenië', 'Armenien'
250 'Azerbaïdjan', 'Azerbeidzjan', 'Aserbaidschan'
251 'Afghanistan', 'Afghanistan', 'Afghanistan'
252 'Arabie Saoudite', 'Saoedi-Arabië', 'Saudi-Arabien'
253 'Géorgie', 'Georgië', 'Georgien'
254 'Iraq', 'Irak', 'Irak'
255 'Iran (République Islamique d\')', 'Iran (Islamitische Republiek)', 'Iran (Islamische Republik)'
256 'Israël', 'Israël', 'Israel'
257 'Jordanie', 'Jordanië', 'Jordanien'
258 'Liban', 'Libanon', 'Libanon'
259 'Pakistan', 'Pakistan', 'Pakistan'
260 'Emirats arabes unis', 'Verenigde Arabische Emiraten', 'Vereinigte Arabische Emirate'
261 'Syrie (République Arabe)', 'Syrië (Arabische Republiek)', 'Syrien (Arabische Republik)'
262 'Turquie', 'Turkije', 'Türkei'
263 'Yemen(Rép.arabe)', 'Jemen(Arabische Rep.)', 'Jemen(Arabische Rep.)'
264 'Koweït', 'Koeweit', 'Kuwait'
265 'Yemen(Rép.démocrat.popul.)', 'Jemen(Dem.Volksrep.)', 'Jemen(Dem.Volksrep.)'
266 'Oman', 'Oman', 'Oman'
267 'Qatar', 'Qatar', 'Katar'
268 'Bahreïn', 'Bahrein', 'Bahrain'
269 'Abu Dhabi', 'Abu Dhabi', 'Abu Dhabi'
270 'Yemen(Rép.du)', 'Jemen(Rep.)', 'Jemen(Rep.)'
271 'Palestine', 'Palestina', 'Palästina'
279 'Vietnam du Sud', 'Zuid-Vietnam', 'Südvietnam'
280 'Hong-Kong(Royaume-Uni)', 'Hongkong(Verenigd Koninkrijk)', 'Hong Kong(Vereinigtes Königreich)'
281 'Macao(Portugal)', 'Macau(Portugal)', 'Macau(Portugal)'
282 'Timor', 'Timor', 'Timor'
283 'Palestine', 'Palestinië', 'Palestinien'
301 'Lesotho', 'Lesotho', 'Lesotho'
302 'Botswana', 'Botswana', 'Botsuana'
303 'Burundi', 'Burundi', 'Burundi'
304 'Cameroun', 'Kameroen', 'Kamerun'
305 'République Centrafricaine', 'Centraal-Afrikaanse Republiek', 'Zentralafrikanische Republik'
306 'Congo (Rép. dém.)', 'Congo (Dem. Rep.)', 'Kongo (Dem. Rep.)'
307 'Congo(Rép. pop. du)', 'Congo(Volksrep.)', 'Kongo(Volksrep.)'
308 'Burkina Faso', 'Burkina Faso', 'Burkina Faso'
309 'Côte d\'Ivoire', 'Ivoorkust', 'Côte d\'Ivoire'
310 'Bénin', 'Benin', 'Benin'
311 'Ethiopie', 'Ethiopië', 'Äthiopien'
312 'Gabon', 'Gabon', 'Gabun'
313 'Gambie', 'Gambia', 'Gambia'
314 'Ghana', 'Ghana', 'Ghana'
315 'Guinée', 'Guinee', 'Guinea'
316 'Haute-Volta', 'Opper-Volta', 'Obervolta'
317 'Maurice', 'Mauritius', 'Mauritius'
318 'Libéria', 'Liberia', 'Liberia'
319 'Mali', 'Mali', 'Mali'
320 'Sénégal', 'Senegal', 'Senegal'
321 'Niger', 'Niger', 'Niger'
322 'Nigéria', 'Nigeria', 'Nigeria'
323 'Ouganda', 'Oeganda', 'Uganda'
324 'Madagascar', 'Madagaskar', 'Madagaskar'
325 'Afrique du Sud', 'Zuid-Afrika', 'Südafrika'
326 'Rhodésie', 'Rhodesië', 'Rhodesien'
327 'Rwanda (Rép.)', 'Rwanda (Rep.)', 'Ruanda (Rep.)'
328 'Sierra Leone', 'Sierra Leone', 'Sierra Leone'
329 'Somalie', 'Somalië', 'Somalia'
331 'Ngwane (Royaume du Swaziland)', 'Ngwane (Koninkrijk Swaziland)', 'Ngwane (Königreich Swaziland)'
332 'Tanzanie(Rép.Unie de)', 'Tanzania Verenigde Rep.', 'Tansania(Vereinigte Rep.)'
333 'Tchad', 'Tsjaad', 'Tschad'
334 'Togo', 'Togo', 'Togo'
335 'Zambie', 'Zambia', 'Sambia'
336 'Kenya', 'Kenia', 'Kenia'
337 'Guinée équatoriale', 'Equatoriaal-Guinea', 'Äquatorialguinea'
338 'Guinée-Bissau', 'Guinea-Bissau', 'Guinea-Bissau'
339 'Cap VertIles du', 'Kaapverdische Eilanden', 'Kapverdische Inseln'
340 'Mozambique', 'Mozambique', 'Mozambik'
341 'Angola', 'Angola', 'Angola'
342 'Seychelles(Iles)', 'Seychellen(Eilanden)', 'Seychellen'
343 'Archipel des Comores', 'Archipel van de Comoren', 'Komoren - Archipel'
344 'Zimbabwe', 'Zimbabwe', 'Zimbabwe'
345 'République de Djibouti', 'Republiek Djibouti', 'Republik Djibouti'
346 'Sao Tomé et Principe (Rép. dém. de)', 'Sao Tomé en Principe (Dem. Rep.)', 'Sao Tomé und Principe (Dem. Rep.)'
347 'Swaziland', 'Swaziland', 'Swasiland'
348 'Sénégambie', 'Senegambia', 'Senegambia'
349 'Erythrée', 'Eritrea', 'Eritrea'
351 'Algérie', 'Algerije', 'Algerien'
352 'Egypte', 'Egypte', 'Ägypten'
353 'Libye (Jamahiriya arabe libyenne)', 'Libië (Libisch-Arabische Jamahiriyah)', 'Libyen (Libysch-Arabische Dschamahirija)'
354 'Maroc', 'Marokko', 'Marokko'
355 'Mauritanie', 'Mauritanië', 'Mauretanien'
356 'Soudan', 'Soedan', 'Sudan'
357 'Tunisie', 'Tunesië', 'Tunesien'
358 'Malawi', 'Malawi', 'Malawi'
359 'Congo belge', 'Belgisch Kongo', 'Belgisch-Kongo'
360 'Ruanda', 'Roeanda', 'Ruanda'
361 'Urundi', 'Urundi', 'Urundi'
362 'Congo (Rép. du)', 'Kongo (Rep.)', 'Kongo (Rep.)'
364 'Zaïre (République du)', 'Zaïre (Republiek)', 'Zaire (Republik)'
380 'Afars et Issas', 'Afars en Issas', 'Afars und Issas'
381 'Angola', 'Angola', 'Angola'
382 'Cabinda', 'Cabinda', 'Cabinda'
383 'Mozambique', 'Mozambique', 'Mozambique'
384 'Namibie', 'Namibie', 'Namibia'
385 'Iles du Cap Vert', 'Kaapverdische Eilanden', 'Kapverdische Inseln'
386 'Archipel des Comores', 'Archipel van de Comoren', 'Kamora-Archipel'
387 'Réunion (France)', 'Réunion (Frankrijk)', 'Réunion (Frankreich)'
388 'Sahara occidental', 'Westelijke Sahara', 'West-Sahara'
389 'Sainte-Hélène (Royaume-Uni)', 'Sint-Helena (Verenigd Koninkrijk)', 'Sankt Helena (Vereinigtes Königreich)'
390 'Seychelles (Iles)', 'Seychellen (Eilanden)', 'Seychellen'
391 'Guinée portugaise', 'Portugees Guinea', 'Portugiesisch-Guinea'
392 'Fernando Poo', 'Fernando Poo', 'Fernando Poo'
393 'Ile de Santhomé', 'Eiland van Santhomé', 'San-Thomé-Insel'
395 'Swaziland', 'Swaziland', 'Swasiland'
396 'Transkei', 'Transkei', 'Transkei'
397 'Bophutatswana', 'Bophutatswana', 'Bophutatswana'
398 'Iles Canaries (Espagne)', 'Canarische Eilanden (Spanje)', 'Kanarische Inseln (Spanien)'
399 'Madère (Portugal)', 'Madeira (Portugal)', 'Madeira (Portugal)'
401 'Canada', 'Canada', 'Kanada'
402 'Etats-Unis d\'Amérique', 'Verenigde Staten van Amerika', 'Vereinigte Staaten von Amerika'
411 'Costa Rica', 'Costa Rica', 'Costa Rica'
412 'Cuba', 'Cuba', 'Kuba'
413 'Guatémala', 'Guatemala', 'Guatemala'
414 'Honduras', 'Honduras', 'Honduras'
415 'Jamaïque', 'Jamaica', 'Jamaika'
416 'Mexique', 'Mexico', 'Mexiko'
417 'Nicaragua', 'Nicaragua', 'Nicaragua'
418 'Panama', 'Panama', 'Panama'
419 'Haïti', 'Haïti', 'Haiti'
420 'République Dominicaine', 'Dominicaanse Republiek', 'Dominikanische Republik'
421 'El Salvador', 'El Salvador', 'El Salvador'
422 'Trinité-et-Tobago', 'Trinidad en Tobago', 'Trinidad und Tobago'
423 'Barbade', 'Barbados', 'Barbados'
424 'Antilles britanniques', 'Britse Antillen', 'Britische Antillen'
425 'Bahamas', 'Bahamas', 'Bahamas'
426 'Grenade', 'Grenada', 'Grenada'
427 'Dominique (République)', 'Dominica (Republiek)', 'Dominica (Republik)'
428 'Sainte Lucie', 'Saint Lucia', 'St. Lucia'
429 'Saint-Vincent-et-les-Grenadines', 'Saint Vincent en de Grenadines', 'St. Vincent und die Grenadinen'
430 'Belize', 'Belize', 'Belize'
431 'St. Kitts et Nevis', 'St. Kitts en Nevis', 'St. Kitts und Nevis'
480 'Ile de Dominica', 'Dominica(Eiland)', 'Dominika-Insel'
481 'Antilles françaises', 'Franse Antillen', 'Franzosische Antillen'
482 'Antilles néerlandaises', 'Nederlandse Antillen', 'Niederländische Antillen'
483 'Antilles américaines', 'Amerikaanse Antillen', 'Antillen(U.S.A.)'
484 'Bahamas', 'Bahama\'s', 'Bahamas'
485 'Bermudes (Royaume-Uni)', 'Bermuda (Verenigd Koninkrijk)', 'Bermudas (Vereinigtes Königreich)'
486 'Iles Vierges', 'Maagdeneilanden', 'Jungferninseln'
487 'Porto-Rico (Etats Unis)', 'Puerto Rico (Verenigde Staten)', 'Puerto Rico (Vereinigte Staaten)'
488 'Iles Turks et Caïques (Royaume-Uni)', 'Turks- en Caicoseilanden (V.K.)', 'Türken und Caicos Inseln (V.K.)'
489 'Belize(R.U.)', 'Belize(V.K.)', 'Belize(V.K.)'
490 'Anguilla (Royaume-Uni)', 'Anguilla (Verenigd Koninkrijk)', 'Anguilla (Vereinigtes Königreich)'
491 'Antigua(R.U.)', 'Antigua(V.K.)', 'Antigua(V.K.)'
492 'Iles Caïmanes (Royaume-uni)', 'Caymaneilanden (Verenigd Koninkrijk)', 'Kaiman Inseln (Vereinigtes Königreich)'
493 'Montserrat (Royaume-Uni)', 'Montserrat (Verenigd Koninkrijk)', 'Montserrat (Vereinigtes Königreich)'
494 'Kitts and Nevis(R.U.)', 'Kitts and Nevis(V.K.)', 'Kitts and Nevis(V.K.)'
495 'Saint-Pierre-et-Miquelon (France)', 'Saint-Pierre en Miquelon (Frankrijk)', 'Saint-Pierre und Miquelon (Frankreich)'
496 'Guadeloupe (France)', 'Guadeloupe (Frankrijk)', 'Guadeloupe (Frankreich)'
497 'Martinique (France)', 'Martinique (Frankrijk)', 'Martinique (Frankreich)'
498 'Le Groenland(D.K.)', 'Groenland(D.K.)', 'Grönland(D.K.)'
511 'Argentine', 'Argentinië', 'Argentinien'
512 'Bolivie', 'Bolivia', 'Bolivien'
513 'Brésil', 'Brazilië', 'Brasilien'
514 'Chili', 'Chili', 'Chile'
515 'Colombie', 'Colombia', 'Kolumbien'
516 'Equateur', 'Ecuador', 'Ecuador'
517 'Paraguay', 'Paraguay', 'Paraguay'
518 'Pérou', 'Peru', 'Peru'
519 'Uruguay', 'Uruguay', 'Uruguay'
520 'Venezuela', 'Venezuela', 'Venezuela'
521 'Guyana', 'Guyana', 'Guyana'
522 'Surinam', 'Suriname', 'Surinam'
580 'Iles Falkland (Royaume-Uni)', 'Falklandeilanden (Verenigd Koninkrijk)', 'Falklandinseln(Vereinigtes Königreich)'
581 'Guyane Française (France)', 'Frans-Guyana (Frankrijk)', 'Französisch-Guayana (Frankreich)'
582 'Honduras britannique', 'Brits Honduras', 'Britisch-Honduras'
583 'Guyane hollandaise', 'Nederlands-Guyana', 'Niederländisch-Guyana'
602 'Micronésie (Etats fédérés de)', 'Micronesia (Federale Staten van)', 'Mikronesien (Föderierte Staaten von)'
603 'Iles Marshall (République des)', 'Marshalleilanden (Republiek der)', 'Marshallinseln (Republik)'
611 'Australie', 'Australië', 'Australien'
613 'Nouvelle-Zélande', 'Nieuw-Zeeland', 'Neuseeland'
614 'Samoa occidentales', 'West-Samoa', 'West-Samoa'
615 'Nauru', 'Nauru', 'Nauru'
616 'Tonga', 'Tonga', 'Tonga'
617 'Fidji', 'Fiji', 'Fidschi'
618 'Nouvelles-Hébrides', 'Nieuwe Hebriden', 'Neue Hebriden'
619 'Papouasie-Nouvelle-Guinée', 'Papoea-Nieuw-Guinea', 'Papua-Neuguinea'
620 'Pacifique Iles du', 'Stille Oceaan Eilanden', 'Inseln des pazif. Ozeans'
621 'Tuvalu', 'Tuvalu', 'Tuvalu'
622 'Iles Gilbert', 'Gilberteilanden', 'Gilbertinseln'
623 'Iles Salomon', 'Salomonseilanden', 'Salomonen'
624 'Vanuatu', 'Vanuatu', 'Vanuatu'
679 'Palau', 'Palau', 'Palau'
680 'Archipel des Carolines', 'Archipel der Carolinen', 'Karolinenarchipel'
681 'Guam (Etats-Unis)', 'Guam (Verenigde Staten)', 'Guam (Vereinigte Staaten)'
682 'Hawaï', 'Hawaï', 'Hawai'
683 'Nouvelle-Calédonie (France)', 'Nieuw-Caledonië (Frankrijk)', 'Neukaledonien (Frankreich)'
684 'Polynésie française (France)', 'Frans-Polynesië (Frankrijk)', 'Französisch-Polynesien (Frankreich)'
685 'Niue-ile(N-Z.)', 'Niue-eiland(N-Z.)', 'Niue-Insel(N-Z.)'
686 'Tokelau (Nouvelle-Zélande)', 'Tokelau-eilanden (Nieuw-Zeeland)', 'Tokelau (Neuseeland)'
687 'Cook(N-Z.)', 'Cook(N-Z.)', 'Cook(N-Z.)'
688 'Tahiti', 'Tahiti', 'Tahiti'
689 'Wallis et Futuna (France)', 'Wallis en Futuna (Frankrijk)', 'Wallis und Futuna (Frankreich)'
690 'Samoa américaines (Etats-Unis)', 'Amerikaans-Samoa (Verenigde Staten)', 'Amerikanisch-Samoa (Vereinigte Staaten)'
691 'Territ sous tutelle américaine', 'Grondgeb.onder Amerik.voogdij', 'Gebiet unter Amerik.Vormundschaft'
692 'Pitcairn (Royaume-Uni)', 'Pitcairneilanden (Verenigd Koninkrijk)', 'Pitcairninseln(Vereinigtes Königreich)'
693 'Territ.dép.de l\'Australie', 'Grondgeb.afh.van Australië', 'Gebiet abhängig von Australien'
694 'Territ.dép.de la Nelle Zélande', 'Grondgeb.afh. van Nieuw-Zeeland', 'Gebiet abhängig von Neuseeland'
999 'Indéterminé', 'Onbepaald', 'Unbestimmt'
'''

#Code Postal;Nom;Code INS;nom Commune;Code Région;Région
CITIES = u"""
1000;Brussel;21004;BRUXELLES;3;Bruxelles
1000;Bruxelles;21004;BRUXELLES;3;Bruxelles
1010;Cité Administrative de l'Etat;21004;BRUXELLES;3;Bruxelles
1010;Rijksadministratief Centrum;21004;BRUXELLES;3;Bruxelles
1011;Vlaamse Raad - Vlaams Parlement;21004;BRUXELLES;3;Bruxelles
1020;Brussel (Laken);21004;BRUXELLES;3;Bruxelles
1020;Bruxelles (Laeken);21004;BRUXELLES;3;Bruxelles
1020;Laeken (Bruxelles);21004;BRUXELLES;3;Bruxelles
1020;Laken (Brussel);21004;BRUXELLES;3;Bruxelles
1030;Brussel (Schaarbeek);21015;SCHAERBEEK;3;Bruxelles
1030;Bruxelles (Schaerbeek);21015;SCHAERBEEK;3;Bruxelles
1030;Schaarbeek;21015;SCHAERBEEK;3;Bruxelles
1030;Schaerbeek;21015;SCHAERBEEK;3;Bruxelles
1040;Brussel (Etterbeek);21005;ETTERBEEK;3;Bruxelles
1040;Bruxelles (Etterbeek);21005;ETTERBEEK;3;Bruxelles
1040;Etterbeek;21005;ETTERBEEK;3;Bruxelles
1041;International Press Center;21005;ETTERBEEK;3;Bruxelles
1047;Europees Parlement;21005;ETTERBEEK;3;Bruxelles
1047;Parlement Européen;21005;ETTERBEEK;3;Bruxelles
1050;Brussel (Elsene);21009;IXELLES;3;Bruxelles
1050;Bruxelles (Ixelles);21009;IXELLES;3;Bruxelles
1050;Elsene;21009;IXELLES;3;Bruxelles
1050;Ixelles;21009;IXELLES;3;Bruxelles
1060;Brussel (Sint-Gillis);21013;SAINT-GILLES;3;Bruxelles
1060;Bruxelles (Saint-Gilles);21013;SAINT-GILLES;3;Bruxelles
1060;Saint-Gilles;21013;SAINT-GILLES;3;Bruxelles
1060;Sint-Gillis;21013;SAINT-GILLES;3;Bruxelles
1070;Anderlecht;21001;ANDERLECHT;3;Bruxelles
1070;Brussel (Anderlecht);21001;ANDERLECHT;3;Bruxelles
1070;Bruxelles (Anderlecht);21001;ANDERLECHT;3;Bruxelles
1080;Brussel (Sint-Jans-Molenbeek);21012;MOLENBEEK-SAINT-JEAN;3;Bruxelles
1080;Bruxelles (Molenbeek-Saint-Jean);21012;MOLENBEEK-SAINT-JEAN;3;Bruxelles
1080;Molenbeek-Saint-Jean;21012;MOLENBEEK-SAINT-JEAN;3;Bruxelles
1080;Sint-Jans-Molenbeek;21012;MOLENBEEK-SAINT-JEAN;3;Bruxelles
1081;Brussel (Koekelberg);21011;KOEKELBERG;3;Bruxelles
1081;Bruxelles (Koekelberg);21011;KOEKELBERG;3;Bruxelles
1081;Koekelberg;21011;KOEKELBERG;3;Bruxelles
1082;Berchem-Sainte-Agathe;21003;BERCHEM-SAINTE-AGATHE;3;Bruxelles
1082;Brussel (Sint-Agatha-Berchem);21003;BERCHEM-SAINTE-AGATHE;3;Bruxelles
1082;Bruxelles (Berchem-Sainte-Agathe);21003;BERCHEM-SAINTE-AGATHE;3;Bruxelles
1082;Sint-Agatha-Berchem;21003;BERCHEM-SAINTE-AGATHE;3;Bruxelles
1083;Brussel (Ganshoren);21008;GANSHOREN;3;Bruxelles
1083;Bruxelles (Ganshoren);21008;GANSHOREN;3;Bruxelles
1083;Ganshoren;21008;GANSHOREN;3;Bruxelles
1090;Brussel (Jette);21010;JETTE;3;Bruxelles
1090;Bruxelles (Jette);21010;JETTE;3;Bruxelles
1090;Jette;21010;JETTE;3;Bruxelles
1110;NAVO - NATO;21010;JETTE;3;Bruxelles
1110;OTAN - NATO;21010;JETTE;3;Bruxelles
1120;Brussel (Neder-Over-Heembeek);21004;BRUXELLES;3;Bruxelles
1120;Bruxelles (Neder-Over-Heembeek);21004;BRUXELLES;3;Bruxelles
1120;Neder-Over-Heembeek (Bru.);21004;BRUXELLES;3;Bruxelles
1130;Brussel (Haren);21004;BRUXELLES;3;Bruxelles
1130;Bruxelles (Haeren);21004;BRUXELLES;3;Bruxelles
1130;Haren (Bruxelles);21004;BRUXELLES;3;Bruxelles
1130;Haren (Brussel);21004;BRUXELLES;3;Bruxelles
1140;Brussel (Evere);21006;EVERE;3;Bruxelles
1140;Bruxelles (Evere);21006;EVERE;3;Bruxelles
1140;Evere;21006;EVERE;3;Bruxelles
1150;Brussel (Sint-Pieters-Woluwe);21018;WOLUWE-SAINT-LAMBERT;3;Bruxelles
1150;Bruxelles (Woluwe-Saint-Pierre);21018;WOLUWE-SAINT-LAMBERT;3;Bruxelles
1150;Sint-Pieters-Woluwe;21018;WOLUWE-SAINT-LAMBERT;3;Bruxelles
1150;Woluwe-Saint-Pierre;21018;WOLUWE-SAINT-LAMBERT;3;Bruxelles
1160;Auderghem;21002;AUDERGHEM;3;Bruxelles
1160;Brussel (Oudergem);21002;AUDERGHEM;3;Bruxelles
1160;Bruxelles (Auderghem);21002;AUDERGHEM;3;Bruxelles
1160;Oudergem;21002;AUDERGHEM;3;Bruxelles
1170;Brussel (Watermaal-Bosvoorde);21017;WATERMAEL-BOITSFORT;3;Bruxelles
1170;Bruxelles (Watermael-Boitsfort);21017;WATERMAEL-BOITSFORT;3;Bruxelles
1170;Watermaal-Bosvoorde;21017;WATERMAEL-BOITSFORT;3;Bruxelles
1170;Watermael-Boitsfort;21017;WATERMAEL-BOITSFORT;3;Bruxelles
1180;Brussel (Ukkel);21016;UCCLE;3;Bruxelles
1180;Bruxelles (Uccle);21016;UCCLE;3;Bruxelles
1180;Uccle;21016;UCCLE;3;Bruxelles
1180;Ukkel;21016;UCCLE;3;Bruxelles
1190;Brussel (Vorst);21007;FOREST;3;Bruxelles
1190;Bruxelles (Forest);21007;FOREST;3;Bruxelles
1190;Forest;21007;FOREST;3;Bruxelles
1190;Vorst;21007;FOREST;3;Bruxelles
1200;Brussel (Sint-Lambrechts-Woluwe);21018;WOLUWE-SAINT-LAMBERT;3;Bruxelles
1200;Bruxelles (Woluwe-Saint-Lambert);21018;WOLUWE-SAINT-LAMBERT;3;Bruxelles
1200;Sint-Lambrechts-Woluwe;21018;WOLUWE-SAINT-LAMBERT;3;Bruxelles
1200;Woluwe-Saint-Lambert;21018;WOLUWE-SAINT-LAMBERT;3;Bruxelles
1210;Brussel (Sint-Joost-ten-Node);21014;SAINT-JOSSE-TEN-NOODE;3;Bruxelles
1210;Bruxelles (Saint-Josse-ten-Noode);21014;SAINT-JOSSE-TEN-NOODE;3;Bruxelles
1210;Saint-Josse-ten-Noode;21014;SAINT-JOSSE-TEN-NOODE;3;Bruxelles
1210;Sint-Joost-ten-Node;21014;SAINT-JOSSE-TEN-NOODE;3;Bruxelles
1300;Limal;25112;WAVRE;2;Wallonie
1300;Wavre;25112;WAVRE;2;Wallonie
1301;Bierges;25112;WAVRE;2;Wallonie
1310;La Hulpe;25050;LA HULPE;2;Wallonie
1315;Glimes;25043;INCOURT;2;Wallonie
1315;Incourt;25043;INCOURT;2;Wallonie
1315;Opprebais;25043;INCOURT;2;Wallonie
1315;Pičtrebais;25043;INCOURT;2;Wallonie
1315;Roux-Miroir;25043;INCOURT;2;Wallonie
1320;Beauvechain;25005;BEAUVECHAIN;2;Wallonie
1320;Hamme-Mille;25005;BEAUVECHAIN;2;Wallonie
1320;l'Ecluse;25005;BEAUVECHAIN;2;Wallonie
1320;Nodebais;25005;BEAUVECHAIN;2;Wallonie
1320;Tourinnes-la-Grosse;25005;BEAUVECHAIN;2;Wallonie
1325;Bonlez;25018;CHAUMONT-GISTOUX;2;Wallonie
1325;Chaumont-Gistoux;25018;CHAUMONT-GISTOUX;2;Wallonie
1325;Corroy-le-Grand;25018;CHAUMONT-GISTOUX;2;Wallonie
1325;Dion-Valmont;25018;CHAUMONT-GISTOUX;2;Wallonie
1325;Longueville;25018;CHAUMONT-GISTOUX;2;Wallonie
1330;Rixensart;25091;RIXENSART;2;Wallonie
1331;Rosičres;25091;RIXENSART;2;Wallonie
1332;Genval;25091;RIXENSART;2;Wallonie
1340;Ottignies;25121;OTTIGNIES-LOUVAIN-LA-NEUVE;2;Wallonie
1340;Ottignies-Louvain-la-Neuve;25121;OTTIGNIES-LOUVAIN-LA-NEUVE;2;Wallonie
1341;Céroux-Mousty;25121;OTTIGNIES-LOUVAIN-LA-NEUVE;2;Wallonie
1342;Limelette;25121;OTTIGNIES-LOUVAIN-LA-NEUVE;2;Wallonie
1348;Louvain-la-Neuve;25121;OTTIGNIES-LOUVAIN-LA-NEUVE;2;Wallonie
1350;Enines;25120;ORP-JAUCHE;2;Wallonie
1350;Folx-les-Caves;25120;ORP-JAUCHE;2;Wallonie
1350;Jandrain-Jandrenouille;25120;ORP-JAUCHE;2;Wallonie
1350;Jauche;25120;ORP-JAUCHE;2;Wallonie
1350;Marilles;25120;ORP-JAUCHE;2;Wallonie
1350;Noduwez;25120;ORP-JAUCHE;2;Wallonie
1350;Orp-Jauche;25120;ORP-JAUCHE;2;Wallonie
1350;Orp-le-Grand;25120;ORP-JAUCHE;2;Wallonie
1357;Hélécine;25118;HELECINE;2;Wallonie
1357;Linsmeau;25118;HELECINE;2;Wallonie
1357;Neerheylissem;25118;HELECINE;2;Wallonie
1357;Opheylissem;25118;HELECINE;2;Wallonie
1360;Malčves-Sainte-Marie-Wastines;25084;PERWEZ;2;Wallonie
1360;Orbais;25084;PERWEZ;2;Wallonie
1360;Perwez;25084;PERWEZ;2;Wallonie
1360;Thorembais-les-Béguines;25084;PERWEZ;2;Wallonie
1360;Thorembais-Saint-Trond;25084;PERWEZ;2;Wallonie
1367;Autre-Eglise;25122;RAMILLIES;2;Wallonie
1367;Bomal (Bt.);25122;RAMILLIES;2;Wallonie
1367;Geest-Gérompont-Petit-Rosičre;25122;RAMILLIES;2;Wallonie
1367;Gérompont;25122;RAMILLIES;2;Wallonie
1367;Grand-Rosičre-Hottomont;25122;RAMILLIES;2;Wallonie
1367;Huppaye;25122;RAMILLIES;2;Wallonie
1367;Mont-Saint-André;25122;RAMILLIES;2;Wallonie
1367;Ramillies;25122;RAMILLIES;2;Wallonie
1370;Dongelberg;25048;JODOIGNE;2;Wallonie
1370;Jauchelette;25048;JODOIGNE;2;Wallonie
1370;Jodoigne;25048;JODOIGNE;2;Wallonie
1370;Jodoigne-Souveraine;25048;JODOIGNE;2;Wallonie
1370;Lathuy;25048;JODOIGNE;2;Wallonie
1370;Mélin;25048;JODOIGNE;2;Wallonie
1370;Piétrain;25048;JODOIGNE;2;Wallonie
1370;Saint-Jean-Geest;25048;JODOIGNE;2;Wallonie
1370;Saint-Remy-Geest;25048;JODOIGNE;2;Wallonie
1370;Zétrud-Lumay;25048;JODOIGNE;2;Wallonie
1380;Couture-Saint-Germain;25119;LASNE;2;Wallonie
1380;Lasne;25119;LASNE;2;Wallonie
1380;Lasne-Chapelle-Saint-Lambert;25119;LASNE;2;Wallonie
1380;Maransart;25119;LASNE;2;Wallonie
1380;Ohain;25119;LASNE;2;Wallonie
1380;Plancenoit;25119;LASNE;2;Wallonie
1390;Archennes;25037;GREZ-DOICEAU;2;Wallonie
1390;Biez;25037;GREZ-DOICEAU;2;Wallonie
1390;Bossut-Gottechain;25037;GREZ-DOICEAU;2;Wallonie
1390;Grez-Doiceau;25037;GREZ-DOICEAU;2;Wallonie
1390;Nethen;25037;GREZ-DOICEAU;2;Wallonie
1400;Monstreux;25072;NIVELLES;2;Wallonie
1400;Nivelles;25072;NIVELLES;2;Wallonie
1401;Baulers;25072;NIVELLES;2;Wallonie
1402;Thines;25072;NIVELLES;2;Wallonie
1404;Bornival;25072;NIVELLES;2;Wallonie
1410;Waterloo;25110;WATERLOO;2;Wallonie
1420;Braine-l'Alleud;25014;BRAINE-L ALLEUD;2;Wallonie
1421;Ophain-Bois-Seigneur-Isaac;25014;BRAINE-L ALLEUD;2;Wallonie
1428;Lillois-Witterzée;25014;BRAINE-L ALLEUD;2;Wallonie
1430;Bierghes;25123;REBECQ;2;Wallonie
1430;Quenast;25123;REBECQ;2;Wallonie
1430;Rebecq;25123;REBECQ;2;Wallonie
1430;Rebecq-Rognon;25123;REBECQ;2;Wallonie
1435;Corbais;25068;MONT-SAINT-GUIBERT;2;Wallonie
1435;Hévillers;25068;MONT-SAINT-GUIBERT;2;Wallonie
1435;Mont-Saint-Guibert;25068;MONT-SAINT-GUIBERT;2;Wallonie
1440;Braine-le-Chāteau;25015;BRAINE-LE-CHATEAU;2;Wallonie
1440;Wauthier-Braine;25015;BRAINE-LE-CHATEAU;2;Wallonie
1450;Chastre;25117;CHASTRE;2;Wallonie
1450;Chastre-Villeroux-Blanmont;25117;CHASTRE;2;Wallonie
1450;Cortil-Noirmont;25117;CHASTRE;2;Wallonie
1450;Gentinnes;25117;CHASTRE;2;Wallonie
1450;Saint-Géry;25117;CHASTRE;2;Wallonie
1457;Nil-Saint-Vincent-Saint-Martin;25124;WALHAIN;2;Wallonie
1457;Tourinnes-Saint-Lambert;25124;WALHAIN;2;Wallonie
1457;Walhain;25124;WALHAIN;2;Wallonie
1457;Walhain-Saint-Paul;25124;WALHAIN;2;Wallonie
1460;Ittre;25044;ITTRE;2;Wallonie
1460;Virginal-Samme;25044;ITTRE;2;Wallonie
1461;Haut-Ittre;25044;ITTRE;2;Wallonie
1470;Baisy-Thy;25031;GENAPPE;2;Wallonie
1470;Bousval;25031;GENAPPE;2;Wallonie
1470;Genappe;25031;GENAPPE;2;Wallonie
1471;Loupoigne;25031;GENAPPE;2;Wallonie
1472;Vieux-Genappe;25031;GENAPPE;2;Wallonie
1473;Glabais;25031;GENAPPE;2;Wallonie
1474;Ways;25031;GENAPPE;2;Wallonie
1476;Houtain-le-Val;25031;GENAPPE;2;Wallonie
1480;Clabecq;25105;TUBIZE;2;Wallonie
1480;Oisquercq;25105;TUBIZE;2;Wallonie
1480;Saintes;25105;TUBIZE;2;Wallonie
1480;Tubize;25105;TUBIZE;2;Wallonie
1490;Court-Saint-Etienne;25023;COURT-SAINT-ETIENNE;2;Wallonie
1495;Marbais (Bt.);25107;VILLERS-LA-VILLE;2;Wallonie
1495;Mellery;25107;VILLERS-LA-VILLE;2;Wallonie
1495;Sart-Dames-Avelines;25107;VILLERS-LA-VILLE;2;Wallonie
1495;Tilly;25107;VILLERS-LA-VILLE;2;Wallonie
1495;Villers-la-Ville;25107;VILLERS-LA-VILLE;2;Wallonie
1500;Halle;23027;HAL;1;Flandre
1501;Buizingen;23027;HAL;1;Flandre
1502;Lembeek;23027;HAL;1;Flandre
1540;Herfelingen;23032;HERNE;1;Flandre
1540;Herne;23032;HERNE;1;Flandre
1541;Sint-Pieters-Kapelle (Bt.);23032;HERNE;1;Flandre
1547;Bever;23009;BIEVENE;1;Flandre
1547;Bievene;23009;BIEVENE;1;Flandre
1560;Hoeilaart;23033;HOEILAART;1;Flandre
1570;Galmaarden;23023;GAMMERAGES;1;Flandre
1570;Tollembeek;23023;GAMMERAGES;1;Flandre
1570;Vollezele;23023;GAMMERAGES;1;Flandre
1600;Oudenaken;23077;SINT-PIETERS-LEEUW;1;Flandre
1600;Sint-Laureins-Berchem;23077;SINT-PIETERS-LEEUW;1;Flandre
1600;Sint-Pieters-Leeuw;23077;SINT-PIETERS-LEEUW;1;Flandre
1601;Ruisbroek (Bt.);23077;SINT-PIETERS-LEEUW;1;Flandre
1602;Vlezenbeek;23077;SINT-PIETERS-LEEUW;1;Flandre
1620;Drogenbos;23098;DROGENBOS;1;Flandre
1630;Linkebeek;23100;LINKEBEEK;1;Flandre
1640;Rhode-Saint-Genese;23101;RHODE-SAINT-GENESE;1;Flandre
1640;Sint-Genesius-Rode;23101;RHODE-SAINT-GENESE;1;Flandre
1650;Beersel;23003;BEERSEL;1;Flandre
1651;Lot;23003;BEERSEL;1;Flandre
1652;Alsemberg;23003;BEERSEL;1;Flandre
1653;Dworp;23003;BEERSEL;1;Flandre
1654;Huizingen;23003;BEERSEL;1;Flandre
1670;Bogaarden;23064;PEPINGEN;1;Flandre
1670;Heikruis;23064;PEPINGEN;1;Flandre
1670;Pepingen;23064;PEPINGEN;1;Flandre
1671;Elingen;23064;PEPINGEN;1;Flandre
1673;Beert;23064;PEPINGEN;1;Flandre
1674;Bellingen;23064;PEPINGEN;1;Flandre
1700;Dilbeek;23016;DILBEEK;1;Flandre
1700;Sint-Martens-Bodegem;23016;DILBEEK;1;Flandre
1700;Sint-Ulriks-Kapelle;23016;DILBEEK;1;Flandre
1701;Itterbeek;23016;DILBEEK;1;Flandre
1702;Groot-Bijgaarden;23016;DILBEEK;1;Flandre
1703;Schepdaal;23016;DILBEEK;1;Flandre
1730;Asse;23002;ASSE;1;Flandre
1730;Bekkerzeel;23002;ASSE;1;Flandre
1730;Kobbegem;23002;ASSE;1;Flandre
1730;Mollem;23002;ASSE;1;Flandre
1731;Relegem;23002;ASSE;1;Flandre
1731;Zellik;23002;ASSE;1;Flandre
1740;Ternat;23086;TERNAT;1;Flandre
1741;Wambeek;23086;TERNAT;1;Flandre
1742;Sint-Katherina-Lombeek;23086;TERNAT;1;Flandre
1745;Mazenzele;23060;OPWIJK;1;Flandre
1745;Opwijk;23060;OPWIJK;1;Flandre
1750;Gaasbeek;23104;LENNIK;1;Flandre
1750;Lennik;23104;LENNIK;1;Flandre
1750;Sint-Kwintens-Lennik;23104;LENNIK;1;Flandre
1750;Sint-Martens-Lennik;23104;LENNIK;1;Flandre
1755;Gooik;23024;GOOIK;1;Flandre
1755;Kester;23024;GOOIK;1;Flandre
1755;Leerbeek;23024;GOOIK;1;Flandre
1755;Oetingen;23024;GOOIK;1;Flandre
1760;Onze-Lieve-Vrouw-Lombeek;23097;ROOSDAAL;1;Flandre
1760;Pamel;23097;ROOSDAAL;1;Flandre
1760;Roosdaal;23097;ROOSDAAL;1;Flandre
1760;Strijtem;23097;ROOSDAAL;1;Flandre
1761;Borchtlombeek;23097;ROOSDAAL;1;Flandre
1770;Liedekerke;23044;LIEDEKERKE;1;Flandre
1780;Wemmel;23102;WEMMEL;1;Flandre
1785;Brussegem;23052;MERCHTEM;1;Flandre
1785;Hamme (Bt.);23052;MERCHTEM;1;Flandre
1785;Merchtem;23052;MERCHTEM;1;Flandre
1790;Affligem;23105;AFFLIGEM;1;Flandre
1790;Essene;23105;AFFLIGEM;1;Flandre
1790;Hekelgem;23105;AFFLIGEM;1;Flandre
1790;Teralfene;23105;AFFLIGEM;1;Flandre
1800;Peutie;23088;VILVORDE;1;Flandre
1800;Vilvoorde;23088;VILVORDE;1;Flandre
1804;Cargovil;23088;VILVORDE;1;Flandre
1820;Melsbroek;23081;STEENOKKERZEEL;1;Flandre
1820;Perk;23081;STEENOKKERZEEL;1;Flandre
1820;Steenokkerzeel;23081;STEENOKKERZEEL;1;Flandre
1830;Machelen (Bt.);23047;MACHELEN;1;Flandre
1831;Diegem;23047;MACHELEN;1;Flandre
1840;Londerzeel;23045;LONDERZEEL;1;Flandre
1840;Malderen;23045;LONDERZEEL;1;Flandre
1840;Steenhuffel;23045;LONDERZEEL;1;Flandre
1850;Grimbergen;23025;GRIMBERGEN;1;Flandre
1851;Humbeek;23025;GRIMBERGEN;1;Flandre
1852;Beigem;23025;GRIMBERGEN;1;Flandre
1853;Strombeek-Bever;23025;GRIMBERGEN;1;Flandre
1860;Meise;23050;MEISE;1;Flandre
1861;Wolvertem;23050;MEISE;1;Flandre
1880;Kapelle-op-den-Bos;23039;KAPELLE-OP-DEN-BOS;1;Flandre
1880;Nieuwenrode;23039;KAPELLE-OP-DEN-BOS;1;Flandre
1880;Ramsdonk;23039;KAPELLE-OP-DEN-BOS;1;Flandre
1910;Berg (Bt.);23038;KAMPENHOUT;1;Flandre
1910;Buken;23038;KAMPENHOUT;1;Flandre
1910;Kampenhout;23038;KAMPENHOUT;1;Flandre
1910;Nederokkerzeel;23038;KAMPENHOUT;1;Flandre
1930;Nossegem;23094;ZAVENTEM;1;Flandre
1930;Zaventem;23094;ZAVENTEM;1;Flandre
1931;Brucargo;23094;ZAVENTEM;1;Flandre
1932;Sint-Stevens-Woluwe;23094;ZAVENTEM;1;Flandre
1933;Sterrebeek;23094;ZAVENTEM;1;Flandre
1934;Brussel X-Luchthaven Remailing;23094;ZAVENTEM;1;Flandre
1934;Bruxelles X-Aeroport Remailing;23094;ZAVENTEM;1;Flandre
1950;Kraainem;23099;KRAAINEM;1;Flandre
1970;Wezembeek-Oppem;23103;WEZEMBEEK-OPPEM;1;Flandre
1980;Eppegem;23096;ZEMST;1;Flandre
1980;Zemst;23096;ZEMST;1;Flandre
1981;Hofstade (Bt.);23096;ZEMST;1;Flandre
1982;Elewijt;23096;ZEMST;1;Flandre
1982;Weerde;23096;ZEMST;1;Flandre
2000;Antwerpen;11002;ANVERS;1;Flandre
2018;Antwerpen;11002;ANVERS;1;Flandre
2020;Antwerpen;11002;ANVERS;1;Flandre
2030;Antwerpen;11002;ANVERS;1;Flandre
2040;Antwerpen;11002;ANVERS;1;Flandre
2040;Berendrecht;11002;ANVERS;1;Flandre
2040;Lillo;11002;ANVERS;1;Flandre
2040;Zandvliet;11002;ANVERS;1;Flandre
2050;Antwerpen;11002;ANVERS;1;Flandre
2060;Antwerpen;11002;ANVERS;1;Flandre
2070;Burcht;11056;ZWIJNDRECHT;1;Flandre
2070;Zwijndrecht;11056;ZWIJNDRECHT;1;Flandre
2100;Deurne (Antwerpen);11002;ANVERS;1;Flandre
2110;Wijnegem;11050;WIJNEGEM;1;Flandre
2140;Borgerhout (Antwerpen);11002;ANVERS;1;Flandre
2150;Borsbeek (Antw.);11008;BRASSCHAAT;1;Flandre
2160;Wommelgem;11052;WOMMELGEM;1;Flandre
2170;Merksem (Antwerpen);11002;ANVERS;1;Flandre
2180;Ekeren (Antwerpen);11002;ANVERS;1;Flandre
2200;Herentals;13011;HERENTALS;1;Flandre
2200;Morkhoven;13011;HERENTALS;1;Flandre
2200;Noorderwijk;13011;HERENTALS;1;Flandre
2220;Hallaar;12014;HEIST-OP-DEN-BERG;1;Flandre
2220;Heist-op-den-Berg;12014;HEIST-OP-DEN-BERG;1;Flandre
2221;Booischot;12014;HEIST-OP-DEN-BERG;1;Flandre
2222;Itegem;12014;HEIST-OP-DEN-BERG;1;Flandre
2222;Wiekevorst;12014;HEIST-OP-DEN-BERG;1;Flandre
2223;Schriek;12014;HEIST-OP-DEN-BERG;1;Flandre
2230;Herselt;13013;HERSELT;1;Flandre
2230;Ramsel;13013;HERSELT;1;Flandre
2235;Houtvenne;13016;HULSHOUT;1;Flandre
2235;Hulshout;13016;HULSHOUT;1;Flandre
2235;Westmeerbeek;13016;HULSHOUT;1;Flandre
2240;Massenhoven;11054;ZANDHOVEN;1;Flandre
2240;Viersel;11054;ZANDHOVEN;1;Flandre
2240;Zandhoven;11054;ZANDHOVEN;1;Flandre
2242;Pulderbos;11054;ZANDHOVEN;1;Flandre
2243;Pulle;11054;ZANDHOVEN;1;Flandre
2250;Olen;13029;OLEN;1;Flandre
2260;Oevel;13049;WESTERLO;1;Flandre
2260;Tongerlo (Antw.);13049;WESTERLO;1;Flandre
2260;Westerlo;13049;WESTERLO;1;Flandre
2260;Zoerle-Parwijs;13049;WESTERLO;1;Flandre
2270;Herenthout;13012;HERENTHOUT;1;Flandre
2275;Gierle;13019;LILLE;1;Flandre
2275;Lille;13019;LILLE;1;Flandre
2275;Poederlee;13019;LILLE;1;Flandre
2275;Wechelderzande;13019;LILLE;1;Flandre
2280;Grobbendonk;13010;GROBBENDONK;1;Flandre
2288;Bouwel;13010;GROBBENDONK;1;Flandre
2290;Vorselaar;13044;VORSELAAR;1;Flandre
2300;Turnhout;13040;TURNHOUT;1;Flandre
2310;Rijkevorsel;13037;RIJKEVORSEL;1;Flandre
2320;Hoogstraten;13014;HOOGSTRATEN;1;Flandre
2321;Meer;13014;HOOGSTRATEN;1;Flandre
2322;Minderhout;13014;HOOGSTRATEN;1;Flandre
2323;Wortel;13014;HOOGSTRATEN;1;Flandre
2328;Meerle;13014;HOOGSTRATEN;1;Flandre
2330;Merksplas;13023;MERKSPLAS;1;Flandre
2340;Beerse;13004;BEERSE;1;Flandre
2340;Vlimmeren;13004;BEERSE;1;Flandre
2350;Vosselaar;13046;VOSSELAAR;1;Flandre
2360;Oud-Turnhout;13031;OUD-TURNHOUT;1;Flandre
2370;Arendonk;13001;ARENDONK;1;Flandre
2380;Ravels;13035;RAVELS;1;Flandre
2381;Weelde;13035;RAVELS;1;Flandre
2382;Poppel;13035;RAVELS;1;Flandre
2387;Baarle-Hertog;13002;BAERLE-DUC;1;Flandre
2390;Malle;11057;MALLE;1;Flandre
2390;Oostmalle;11057;MALLE;1;Flandre
2390;Westmalle;11057;MALLE;1;Flandre
2400;Mol;13025;MOL;1;Flandre
2430;Eindhout;13053;LAAKDAL;1;Flandre
2430;Laakdal;13053;LAAKDAL;1;Flandre
2430;Vorst (Kempen);13053;LAAKDAL;1;Flandre
2431;Varendonk;13053;LAAKDAL;1;Flandre
2431;Veerle;13053;LAAKDAL;1;Flandre
2440;Geel;13008;GEEL;1;Flandre
2450;Meerhout;13021;MEERHOUT;1;Flandre
2460;Kasterlee;13017;KASTERLEE;1;Flandre
2460;Lichtaart;13017;KASTERLEE;1;Flandre
2460;Tielen;13017;KASTERLEE;1;Flandre
2470;Retie;13036;RETIE;1;Flandre
2480;Dessel;13006;DESSEL;1;Flandre
2490;Balen;13003;BALEN;1;Flandre
2491;Olmen;13003;BALEN;1;Flandre
2500;Koningshooikt;12021;LIERRE;1;Flandre
2500;Lier;12021;LIERRE;1;Flandre
2520;Broechem;11035;RANST;1;Flandre
2520;Emblem;11035;RANST;1;Flandre
2520;Oelegem;11035;RANST;1;Flandre
2520;Ranst;11035;RANST;1;Flandre
2530;Boechout;11004;BOECHOUT;1;Flandre
2531;Vremde;11004;BOECHOUT;1;Flandre
2540;Hove;11021;HOVE;1;Flandre
2547;Lint;11025;LINT;1;Flandre
2550;Kontich;11024;KONTICH;1;Flandre
2550;Waarloos;11024;KONTICH;1;Flandre
2560;Bevel;12026;NIJLEN;1;Flandre
2560;Kessel;12026;NIJLEN;1;Flandre
2560;Nijlen;12026;NIJLEN;1;Flandre
2570;Duffel;12009;DUFFEL;1;Flandre
2580;Beerzel;12029;PUTTE;1;Flandre
2580;Putte;12029;PUTTE;1;Flandre
2590;Berlaar;12002;BERLAAR;1;Flandre
2590;Gestel;12002;BERLAAR;1;Flandre
2600;Berchem (Antwerpen);11002;ANVERS;1;Flandre
2610;Wilrijk (Antwerpen);11002;ANVERS;1;Flandre
2620;Hemiksem;11018;HEMIKSEM;1;Flandre
2627;Schelle;11038;SCHELLE;1;Flandre
2630;Aartselaar;11001;AARTSELAAR;1;Flandre
2640;Mortsel;11029;MORTSEL;1;Flandre
2650;Edegem;11013;EDEGEM;1;Flandre
2660;Hoboken (Antwerpen);11002;ANVERS;1;Flandre
2800;Mechelen;12025;MALINES;1;Flandre
2800;Walem;12025;MALINES;1;Flandre
2801;Heffen;12025;MALINES;1;Flandre
2811;Hombeek;12025;MALINES;1;Flandre
2811;Leest;12025;MALINES;1;Flandre
2812;Muizen (Mechelen);12025;MALINES;1;Flandre
2820;Bonheiden;12005;BONHEIDEN;1;Flandre
2820;Rijmenam;12005;BONHEIDEN;1;Flandre
2830;Blaasveld;12040;WILLEBROEK;1;Flandre
2830;Heindonk;12040;WILLEBROEK;1;Flandre
2830;Tisselt;12040;WILLEBROEK;1;Flandre
2830;Willebroek;12040;WILLEBROEK;1;Flandre
2840;Reet;11037;RUMST;1;Flandre
2840;Rumst;11037;RUMST;1;Flandre
2840;Terhagen;11037;RUMST;1;Flandre
2845;Niel;11030;NIEL;1;Flandre
2850;Boom;11005;BOOM;1;Flandre
2860;Sint-Katelijne-Waver;12035;SINT-KATELIJNE-WAVER;1;Flandre
2861;Onze-Lieve-Vrouw-Waver;12035;SINT-KATELIJNE-WAVER;1;Flandre
2870;Breendonk;12030;PUURS;1;Flandre
2870;Liezele;12030;PUURS;1;Flandre
2870;Puurs;12030;PUURS;1;Flandre
2870;Ruisbroek (Antw.);12030;PUURS;1;Flandre
2880;Bornem;12007;BORNEM;1;Flandre
2880;Hingene;12007;BORNEM;1;Flandre
2880;Mariekerke (Bornem);12007;BORNEM;1;Flandre
2880;Weert;12007;BORNEM;1;Flandre
2890;Lippelo;12034;SINT-AMANDS;1;Flandre
2890;Oppuurs;12034;SINT-AMANDS;1;Flandre
2890;Sint-Amands;12034;SINT-AMANDS;1;Flandre
2900;Schoten;11040;SCHOTEN;1;Flandre
2910;Essen;11016;ESSEN;1;Flandre
2920;Kalmthout;11022;KALMTHOUT;1;Flandre
2930;Brasschaat;11008;BRASSCHAAT;1;Flandre
2940;Hoevenen;11044;STABROEK;1;Flandre
2940;Stabroek;11044;STABROEK;1;Flandre
2950;Kapellen (Antw.);11024;KONTICH;1;Flandre
2960;Brecht;11009;BRECHT;1;Flandre
2960;Sint-Job-in-'t-Goor;11009;BRECHT;1;Flandre
2960;Sint-Lenaarts;11009;BRECHT;1;Flandre
2970;'s Gravenwezel;11039;SCHILDE;1;Flandre
2970;Schilde;11039;SCHILDE;1;Flandre
2980;Halle (Kempen);11055;ZOERSEL;1;Flandre
2980;Zoersel;11055;ZOERSEL;1;Flandre
2990;Loenhout;11053;WUUSTWEZEL;1;Flandre
2990;Wuustwezel;11053;WUUSTWEZEL;1;Flandre
3000;Leuven;24062;LOUVAIN;1;Flandre
3001;Heverlee;24062;LOUVAIN;1;Flandre
3010;Kessel-Lo (Leuven);24062;LOUVAIN;1;Flandre
3012;Wilsele;24062;LOUVAIN;1;Flandre
3018;Wijgmaal (Brabant);24062;LOUVAIN;1;Flandre
3020;Herent;24038;HERENT;1;Flandre
3020;Veltem-Beisem;24038;HERENT;1;Flandre
3020;Winksele;24038;HERENT;1;Flandre
3040;Huldenberg;24045;HULDENBERG;1;Flandre
3040;Loonbeek;24045;HULDENBERG;1;Flandre
3040;Neerijse;24045;HULDENBERG;1;Flandre
3040;Ottenburg;24045;HULDENBERG;1;Flandre
3040;Sint-Agatha-Rode;24045;HULDENBERG;1;Flandre
3050;Oud-Heverlee;24086;OUD-HEVERLEE;1;Flandre
3051;Sint-Joris-Weert;24086;OUD-HEVERLEE;1;Flandre
3052;Blanden;24086;OUD-HEVERLEE;1;Flandre
3053;Haasrode;24086;OUD-HEVERLEE;1;Flandre
3054;Vaalbeek;24086;OUD-HEVERLEE;1;Flandre
3060;Bertem;24009;BERTEM;1;Flandre
3060;Korbeek-Dijle;24009;BERTEM;1;Flandre
3061;Leefdaal;24009;BERTEM;1;Flandre
3070;Kortenberg;24055;KORTENBERG;1;Flandre
3071;Erps-Kwerps;24055;KORTENBERG;1;Flandre
3078;Everberg;24055;KORTENBERG;1;Flandre
3078;Meerbeek;24055;KORTENBERG;1;Flandre
3080;Duisburg;24104;TERVUREN;1;Flandre
3080;Tervuren;24104;TERVUREN;1;Flandre
3080;Vossem;24104;TERVUREN;1;Flandre
3090;Overijse;23062;OVERIJSE;1;Flandre
3110;Rotselaar;24094;ROTSELAAR;1;Flandre
3111;Wezemaal;24094;ROTSELAAR;1;Flandre
3118;Werchter;24094;ROTSELAAR;1;Flandre
3120;Tremelo;24109;TREMELO;1;Flandre
3128;Baal;24109;TREMELO;1;Flandre
3130;Begijnendijk;24007;BEGIJNENDIJK;1;Flandre
3130;Betekom;24007;BEGIJNENDIJK;1;Flandre
3140;Keerbergen;24048;KEERBERGEN;1;Flandre
3150;Haacht;24033;HAACHT;1;Flandre
3150;Tildonk;24033;HAACHT;1;Flandre
3150;Wespelaar;24033;HAACHT;1;Flandre
3190;Boortmeerbeek;24014;BOORTMEERBEEK;1;Flandre
3191;Hever;24014;BOORTMEERBEEK;1;Flandre
3200;Aarschot;24001;AARSCHOT;1;Flandre
3200;Gelrode;24001;AARSCHOT;1;Flandre
3201;Langdorp;24001;AARSCHOT;1;Flandre
3202;Rillaar;24001;AARSCHOT;1;Flandre
3210;Linden;24066;LUBBEEK;1;Flandre
3210;Lubbeek;24066;LUBBEEK;1;Flandre
3211;Binkom;24066;LUBBEEK;1;Flandre
3212;Pellenberg;24066;LUBBEEK;1;Flandre
3220;Holsbeek;24043;HOLSBEEK;1;Flandre
3220;Kortrijk-Dutsel;24043;HOLSBEEK;1;Flandre
3220;Sint-Pieters-Rode;24043;HOLSBEEK;1;Flandre
3221;Nieuwrode;24043;HOLSBEEK;1;Flandre
3270;Scherpenheuvel;24134;MONTAIGU-ZICHEM;1;Flandre
3270;Scherpenheuvel-Zichem;24134;MONTAIGU-ZICHEM;1;Flandre
3271;Averbode;24134;MONTAIGU-ZICHEM;1;Flandre
3271;Zichem;24134;MONTAIGU-ZICHEM;1;Flandre
3272;Messelbroek;24134;MONTAIGU-ZICHEM;1;Flandre
3272;Testelt;24134;MONTAIGU-ZICHEM;1;Flandre
3290;Deurne (Bt.);24020;DIEST;1;Flandre
3290;Diest;24020;DIEST;1;Flandre
3290;Schaffen;24020;DIEST;1;Flandre
3290;Webbekom;24020;DIEST;1;Flandre
3293;Kaggevinne;24020;DIEST;1;Flandre
3294;Molenstede;24020;DIEST;1;Flandre
3300;Bost;24107;TIRLEMONT;1;Flandre
3300;Goetsenhoven;24107;TIRLEMONT;1;Flandre
3300;Hakendover;24107;TIRLEMONT;1;Flandre
3300;Kumtich;24107;TIRLEMONT;1;Flandre
3300;Oorbeek;24107;TIRLEMONT;1;Flandre
3300;Oplinter;24107;TIRLEMONT;1;Flandre
3300;Sint-Margriete-Houtem (Tienen);24107;TIRLEMONT;1;Flandre
3300;Tienen;24107;TIRLEMONT;1;Flandre
3300;Vissenaken;24107;TIRLEMONT;1;Flandre
3320;Hoegaarden;24041;HOEGAARDEN;1;Flandre
3320;Meldert (Bt.);24041;HOEGAARDEN;1;Flandre
3321;Outgaarden;24041;HOEGAARDEN;1;Flandre
3350;Drieslinter;24133;LINTER;1;Flandre
3350;Linter;24133;LINTER;1;Flandre
3350;Melkwezer;24133;LINTER;1;Flandre
3350;Neerhespen;24133;LINTER;1;Flandre
3350;Neerlinter;24133;LINTER;1;Flandre
3350;Orsmaal-Gussenhoven;24133;LINTER;1;Flandre
3350;Overhespen;24133;LINTER;1;Flandre
3350;Wommersom;24133;LINTER;1;Flandre
3360;Bierbeek;24011;BIERBEEK;1;Flandre
3360;Korbeek-Lo;24011;BIERBEEK;1;Flandre
3360;Lovenjoel;24011;BIERBEEK;1;Flandre
3360;Opvelp;24011;BIERBEEK;1;Flandre
3370;Boutersem;24016;BOUTERSEM;1;Flandre
3370;Kerkom;24016;BOUTERSEM;1;Flandre
3370;Neervelp;24016;BOUTERSEM;1;Flandre
3370;Roosbeek;24016;BOUTERSEM;1;Flandre
3370;Vertrijk;24016;BOUTERSEM;1;Flandre
3370;Willebringen;24016;BOUTERSEM;1;Flandre
3380;Bunsbeek;24137;GLABBEEK;1;Flandre
3380;Glabbeek-Zuurbemde;24137;GLABBEEK;1;Flandre
3381;Kapellen (Bt.);24137;GLABBEEK;1;Flandre
3384;Attenrode;24137;GLABBEEK;1;Flandre
3390;Houwaart;24135;TIELT-WINGE;1;Flandre
3390;Sint-Joris-Winge;24135;TIELT-WINGE;1;Flandre
3390;Tielt (Bt.);24135;TIELT-WINGE;1;Flandre
3390;Tielt-Winge;24135;TIELT-WINGE;1;Flandre
3391;Meensel-Kiezegem;24135;TIELT-WINGE;1;Flandre
3400;Eliksem;24059;LANDEN;1;Flandre
3400;Ezemaal;24059;LANDEN;1;Flandre
3400;Laar;24059;LANDEN;1;Flandre
3400;Landen;24059;LANDEN;1;Flandre
3400;Neerwinden;24059;LANDEN;1;Flandre
3400;Overwinden;24059;LANDEN;1;Flandre
3400;Rumsdorp;24059;LANDEN;1;Flandre
3400;Wange;24059;LANDEN;1;Flandre
3401;Waasmont;24059;LANDEN;1;Flandre
3401;Walsbets;24059;LANDEN;1;Flandre
3401;Walshoutem;24059;LANDEN;1;Flandre
3401;Wezeren;24059;LANDEN;1;Flandre
3404;Attenhoven;24059;LANDEN;1;Flandre
3404;Neerlanden;24059;LANDEN;1;Flandre
3440;Budingen;24130;LEAU;1;Flandre
3440;Dormaal;24130;LEAU;1;Flandre
3440;Halle-Booienhoven;24130;LEAU;1;Flandre
3440;Helen-Bos;24130;LEAU;1;Flandre
3440;Zoutleeuw;24130;LEAU;1;Flandre
3450;Geetbets;24028;GEETBETS;1;Flandre
3450;Grazen;24028;GEETBETS;1;Flandre
3454;Rummen;24028;GEETBETS;1;Flandre
3460;Assent;24008;BEKKEVOORT;1;Flandre
3460;Bekkevoort;24008;BEKKEVOORT;1;Flandre
3461;Molenbeek-Wersbeek;24008;BEKKEVOORT;1;Flandre
3470;Kortenaken;24054;KORTENAKEN;1;Flandre
3470;Ransberg;24054;KORTENAKEN;1;Flandre
3471;Hoeleden;24054;KORTENAKEN;1;Flandre
3472;Kersbeek-Miskom;24054;KORTENAKEN;1;Flandre
3473;Waanrode;24054;KORTENAKEN;1;Flandre
3500;Hasselt;71022;HASSELT;1;Flandre
3500;Sint-Lambrechts-Herk;71022;HASSELT;1;Flandre
3501;Wimmertingen;71022;HASSELT;1;Flandre
3510;Kermt (Hasselt);71022;HASSELT;1;Flandre
3510;Spalbeek;71022;HASSELT;1;Flandre
3511;Kuringen;71022;HASSELT;1;Flandre
3511;Stokrooie;71022;HASSELT;1;Flandre
3512;Stevoort;71022;HASSELT;1;Flandre
3520;Zonhoven;71066;ZONHOVEN;1;Flandre
3530;Helchteren;72039;HOUTHALEN-HELCHTEREN;1;Flandre
3530;Houthalen;72039;HOUTHALEN-HELCHTEREN;1;Flandre
3530;Houthalen-Helchteren;72039;HOUTHALEN-HELCHTEREN;1;Flandre
3540;Berbroek;71024;HERCK-LA-VILLE;1;Flandre
3540;Donk;71024;HERCK-LA-VILLE;1;Flandre
3540;Herk-de-Stad;71024;HERCK-LA-VILLE;1;Flandre
3540;Schulen;71024;HERCK-LA-VILLE;1;Flandre
3545;Halen;71020;HALEN;1;Flandre
3545;Loksbergen;71020;HALEN;1;Flandre
3545;Zelem;71020;HALEN;1;Flandre
3550;Heusden (Limb.);71070;HEUSDEN-ZOLDER;1;Flandre
3550;Heusden-Zolder;71070;HEUSDEN-ZOLDER;1;Flandre
3550;Zolder;71070;HEUSDEN-ZOLDER;1;Flandre
3560;Linkhout;71037;LUMMEN;1;Flandre
3560;Lummen;71037;LUMMEN;1;Flandre
3560;Meldert (Limb.);71037;LUMMEN;1;Flandre
3570;Alken;73001;ALKEN;1;Flandre
3580;Beringen;71004;BERINGEN;1;Flandre
3581;Beverlo;71004;BERINGEN;1;Flandre
3582;Koersel;71004;BERINGEN;1;Flandre
3583;Paal;71004;BERINGEN;1;Flandre
3590;Diepenbeek;71011;DIEPENBEEK;1;Flandre
3600;Genk;71016;GENK;1;Flandre
3620;Gellik;73042;LANAKEN;1;Flandre
3620;Lanaken;73042;LANAKEN;1;Flandre
3620;Neerharen;73042;LANAKEN;1;Flandre
3620;Veldwezelt;73042;LANAKEN;1;Flandre
3621;Rekem;73042;LANAKEN;1;Flandre
3630;Eisden;73107;MAASMECHELEN;1;Flandre
3630;Leut;73107;MAASMECHELEN;1;Flandre
3630;Maasmechelen;73107;MAASMECHELEN;1;Flandre
3630;Mechelen-aan-de-Maas;73107;MAASMECHELEN;1;Flandre
3630;Meeswijk;73107;MAASMECHELEN;1;Flandre
3630;Opgrimbie;73107;MAASMECHELEN;1;Flandre
3630;Vucht;73107;MAASMECHELEN;1;Flandre
3631;Boorsem;73107;MAASMECHELEN;1;Flandre
3631;Uikhoven;73107;MAASMECHELEN;1;Flandre
3640;Kessenich;72018;KINROOI;1;Flandre
3640;Kinrooi;72018;KINROOI;1;Flandre
3640;Molenbeersel;72018;KINROOI;1;Flandre
3640;Ophoven;72018;KINROOI;1;Flandre
3650;Dilsen-Stokkem;72041;DILSEN-STOKKEM;1;Flandre
3650;Elen;72041;DILSEN-STOKKEM;1;Flandre
3650;Lanklaar;72041;DILSEN-STOKKEM;1;Flandre
3650;Rotem;72041;DILSEN-STOKKEM;1;Flandre
3650;Stokkem;72041;DILSEN-STOKKEM;1;Flandre
3660;Opglabbeek;71047;OPGLABBEEK;1;Flandre
3665;As;71002;AS;1;Flandre
3668;Niel-bij-As;71002;AS;1;Flandre
3670;Ellikom;72040;MEEUWEN-GRUITRODE;1;Flandre
3670;Gruitrode;72040;MEEUWEN-GRUITRODE;1;Flandre
3670;Meeuwen;72040;MEEUWEN-GRUITRODE;1;Flandre
3670;Meeuwen-Gruitrode;72040;MEEUWEN-GRUITRODE;1;Flandre
3670;Neerglabbeek;72040;MEEUWEN-GRUITRODE;1;Flandre
3670;Wijshagen;72040;MEEUWEN-GRUITRODE;1;Flandre
3680;Maaseik;72021;MAASEIK;1;Flandre
3680;Neeroeteren;72021;MAASEIK;1;Flandre
3680;Opoeteren;72021;MAASEIK;1;Flandre
3690;Zutendaal;71067;ZUTENDAAL;1;Flandre
3700;Berg (Limb.);73083;TONGRES;1;Flandre
3700;Diets-Heur;73083;TONGRES;1;Flandre
3700;Haren (Tongeren);73083;TONGRES;1;Flandre
3700;Henis;73083;TONGRES;1;Flandre
3700;Kolmont (Tongeren);73083;TONGRES;1;Flandre
3700;Koninksem;73083;TONGRES;1;Flandre
3700;Lauw;73083;TONGRES;1;Flandre
3700;Mal;73083;TONGRES;1;Flandre
3700;Neerrepen;73083;TONGRES;1;Flandre
3700;Nerem;73083;TONGRES;1;Flandre
3700;Overrepen (Kolmont);73083;TONGRES;1;Flandre
3700;Piringen (Haren);73083;TONGRES;1;Flandre
3700;Riksingen;73083;TONGRES;1;Flandre
3700;Rutten;73083;TONGRES;1;Flandre
3700;'s Herenelderen;73083;TONGRES;1;Flandre
3700;Sluizen;73083;TONGRES;1;Flandre
3700;Tongeren;73083;TONGRES;1;Flandre
3700;Vreren;73083;TONGRES;1;Flandre
3700;Widooie (Haren);73083;TONGRES;1;Flandre
3717;Herstappe;73028;HERSTAPPE;1;Flandre
3720;Kortessem;73040;KORTESSEM;1;Flandre
3721;Vliermaalroot;73040;KORTESSEM;1;Flandre
3722;Wintershoven;73040;KORTESSEM;1;Flandre
3723;Guigoven;73040;KORTESSEM;1;Flandre
3724;Vliermaal;73040;KORTESSEM;1;Flandre
3730;Hoeselt;73032;HOESELT;1;Flandre
3730;Romershoven;73032;HOESELT;1;Flandre
3730;Sint-Huibrechts-Hern;73032;HOESELT;1;Flandre
3730;Werm;73032;HOESELT;1;Flandre
3732;Schalkhoven;73032;HOESELT;1;Flandre
3740;Beverst;73006;BILZEN;1;Flandre
3740;Bilzen;73006;BILZEN;1;Flandre
3740;Eigenbilzen;73006;BILZEN;1;Flandre
3740;Grote-Spouwen;73006;BILZEN;1;Flandre
3740;Hees;73006;BILZEN;1;Flandre
3740;Kleine-Spouwen;73006;BILZEN;1;Flandre
3740;Mopertingen;73006;BILZEN;1;Flandre
3740;Munsterbilzen;73006;BILZEN;1;Flandre
3740;Rijkhoven;73006;BILZEN;1;Flandre
3740;Rosmeer;73006;BILZEN;1;Flandre
3740;Spouwen;73006;BILZEN;1;Flandre
3740;Waltwilder;73006;BILZEN;1;Flandre
3742;Martenslinde;73006;BILZEN;1;Flandre
3746;Hoelbeek;73006;BILZEN;1;Flandre
3770;Genoelselderen;73066;RIEMST;1;Flandre
3770;Herderen;73066;RIEMST;1;Flandre
3770;Kanne;73066;RIEMST;1;Flandre
3770;Membruggen;73066;RIEMST;1;Flandre
3770;Millen;73066;RIEMST;1;Flandre
3770;Riemst;73066;RIEMST;1;Flandre
3770;Val-Meer;73066;RIEMST;1;Flandre
3770;Vlijtingen;73066;RIEMST;1;Flandre
3770;Vroenhoven;73066;RIEMST;1;Flandre
3770;Zichen-Zussen-Bolder;73066;RIEMST;1;Flandre
3790;Fourons;73109;FOURONS;1;Flandre
3790;Fouron-Saint-Martin;73109;FOURONS;1;Flandre
3790;Moelingen;73109;FOURONS;1;Flandre
3790;Mouland;73109;FOURONS;1;Flandre
3790;Sint-Martens-Voeren;73109;FOURONS;1;Flandre
3790;Voeren;73109;FOURONS;1;Flandre
3791;Remersdaal;73109;FOURONS;1;Flandre
3792;Fouron-Saint-Pierre;73109;FOURONS;1;Flandre
3792;Sint-Pieters-Voeren;73109;FOURONS;1;Flandre
3793;Teuven;73109;FOURONS;1;Flandre
3798;Fouron-le-Comte;73109;FOURONS;1;Flandre
3798;'s Gravenvoeren;73109;FOURONS;1;Flandre
3800;Aalst (Limb.);71053;SAINT-TROND;1;Flandre
3800;Brustem;71053;SAINT-TROND;1;Flandre
3800;Engelmanshoven;71053;SAINT-TROND;1;Flandre
3800;Gelinden;71053;SAINT-TROND;1;Flandre
3800;Groot-Gelmen;71053;SAINT-TROND;1;Flandre
3800;Halmaal;71053;SAINT-TROND;1;Flandre
3800;Kerkom-bij-Sint-Truiden;71053;SAINT-TROND;1;Flandre
3800;Ordingen;71053;SAINT-TROND;1;Flandre
3800;Sint-Truiden;71053;SAINT-TROND;1;Flandre
3800;Zepperen;71053;SAINT-TROND;1;Flandre
3803;Duras;71053;SAINT-TROND;1;Flandre
3803;Gorsem;71053;SAINT-TROND;1;Flandre
3803;Runkelen;71053;SAINT-TROND;1;Flandre
3803;Wilderen;71053;SAINT-TROND;1;Flandre
3806;Velm;71053;SAINT-TROND;1;Flandre
3830;Berlingen;73098;WELLEN;1;Flandre
3830;Wellen;73098;WELLEN;1;Flandre
3831;Herten;73098;WELLEN;1;Flandre
3832;Ulbeek;73098;WELLEN;1;Flandre
3840;Bommershoven (Haren);73009;LOOZ;1;Flandre
3840;Borgloon;73009;LOOZ;1;Flandre
3840;Broekom;73009;LOOZ;1;Flandre
3840;Gors-Opleeuw;73009;LOOZ;1;Flandre
3840;Gotem;73009;LOOZ;1;Flandre
3840;Groot-Loon;73009;LOOZ;1;Flandre
3840;Haren (Borgloon);73009;LOOZ;1;Flandre
3840;Hendrieken;73009;LOOZ;1;Flandre
3840;Hoepertingen;73009;LOOZ;1;Flandre
3840;Jesseren (Kolmont);73009;LOOZ;1;Flandre
3840;Kerniel;73009;LOOZ;1;Flandre
3840;Kolmont (Borgloon);73009;LOOZ;1;Flandre
3840;Kuttekoven;73009;LOOZ;1;Flandre
3840;Rijkel;73009;LOOZ;1;Flandre
3840;Voort;73009;LOOZ;1;Flandre
3850;Binderveld;71045;NIEUWERKERKEN;1;Flandre
3850;Kozen;71045;NIEUWERKERKEN;1;Flandre
3850;Nieuwerkerken (Limb.);71045;NIEUWERKERKEN;1;Flandre
3850;Wijer;71045;NIEUWERKERKEN;1;Flandre
3870;Batsheers;73022;HEERS;1;Flandre
3870;Bovelingen;73022;HEERS;1;Flandre
3870;Gutschoven;73022;HEERS;1;Flandre
3870;Heers;73022;HEERS;1;Flandre
3870;Heks;73022;HEERS;1;Flandre
3870;Horpmaal;73022;HEERS;1;Flandre
3870;Klein-Gelmen;73022;HEERS;1;Flandre
3870;Mechelen-Bovelingen;73022;HEERS;1;Flandre
3870;Mettekoven;73022;HEERS;1;Flandre
3870;Opheers;73022;HEERS;1;Flandre
3870;Rukkelingen-Loon;73022;HEERS;1;Flandre
3870;Vechmaal;73022;HEERS;1;Flandre
3870;Veulen;73022;HEERS;1;Flandre
3890;Boekhout;71017;GINGELOM;1;Flandre
3890;Gingelom;71017;GINGELOM;1;Flandre
3890;Jeuk;71017;GINGELOM;1;Flandre
3890;Kortijs;71017;GINGELOM;1;Flandre
3890;Montenaken;71017;GINGELOM;1;Flandre
3890;Niel-bij-Sint-Truiden;71017;GINGELOM;1;Flandre
3890;Vorsen;71017;GINGELOM;1;Flandre
3891;Borlo;71017;GINGELOM;1;Flandre
3891;Buvingen;71017;GINGELOM;1;Flandre
3891;Mielen-Boven-Aalst;71017;GINGELOM;1;Flandre
3891;Muizen (Limb.);71017;GINGELOM;1;Flandre
3900;Overpelt;72029;OVERPELT;1;Flandre
3910;Neerpelt;72025;NEERPELT;1;Flandre
3910;Sint-Huibrechts-Lille;72025;NEERPELT;1;Flandre
3920;Lommel;72020;LOMMEL;1;Flandre
3930;Achel;72037;HAMONT-ACHEL;1;Flandre
3930;Hamont;72037;HAMONT-ACHEL;1;Flandre
3930;Hamont-Achel;72037;HAMONT-ACHEL;1;Flandre
3940;Hechtel;72038;HECHTEL-EKSEL;1;Flandre
3940;Hechtel-Eksel;72038;HECHTEL-EKSEL;1;Flandre
3941;Eksel;72038;HECHTEL-EKSEL;1;Flandre
3945;Ham;71069;HAM;1;Flandre
3945;Kwaadmechelen;71069;HAM;1;Flandre
3945;Oostham;71069;HAM;1;Flandre
3950;Bocholt;72003;BOCHOLT;1;Flandre
3950;Kaulille;72003;BOCHOLT;1;Flandre
3950;Reppel;72003;BOCHOLT;1;Flandre
3960;Beek;72004;BREE;1;Flandre
3960;Bree;72004;BREE;1;Flandre
3960;Gerdingen;72004;BREE;1;Flandre
3960;Opitter;72004;BREE;1;Flandre
3960;Tongerlo (Limb.);72004;BREE;1;Flandre
3970;Leopoldsburg;71034;BOURG-LEOPOLD;1;Flandre
3971;Heppen;71034;BOURG-LEOPOLD;1;Flandre
3980;Tessenderlo;71057;TESSENDERLO;1;Flandre
3990;Grote-Brogel;72030;PEER;1;Flandre
3990;Kleine-Brogel;72030;PEER;1;Flandre
3990;Peer;72030;PEER;1;Flandre
3990;Wijchmaal;72030;PEER;1;Flandre
4000;Glain;62063;LIEGE;2;Wallonie
4000;Ličge;62063;LIEGE;2;Wallonie
4000;Rocourt;62063;LIEGE;2;Wallonie
4020;Bressoux;62063;LIEGE;2;Wallonie
4020;Jupille-sur-Meuse;62063;LIEGE;2;Wallonie
4020;Ličge;62063;LIEGE;2;Wallonie
4020;Wandre;62063;LIEGE;2;Wallonie
4030;Grivegnée;62063;LIEGE;2;Wallonie
4030;Ličge;62063;LIEGE;2;Wallonie
4031;Angleur;62063;LIEGE;2;Wallonie
4032;Chźnée;62063;LIEGE;2;Wallonie
4040;Herstal;62051;HERSTAL;2;Wallonie
4041;Milmort;62051;HERSTAL;2;Wallonie
4041;Vottem;62051;HERSTAL;2;Wallonie
4042;Liers;62051;HERSTAL;2;Wallonie
4050;Chaudfontaine;62022;CHAUDFONTAINE;2;Wallonie
4051;Vaux-sous-Chčvremont;62022;CHAUDFONTAINE;2;Wallonie
4052;Beaufays;62022;CHAUDFONTAINE;2;Wallonie
4053;Embourg;62022;CHAUDFONTAINE;2;Wallonie
4100;Boncelles;62096;SERAING;2;Wallonie
4100;Seraing;62096;SERAING;2;Wallonie
4101;Jemeppe-sur-Meuse;62096;SERAING;2;Wallonie
4102;Ougrée;62096;SERAING;2;Wallonie
4120;Ehein;62121;NEUPRE;2;Wallonie
4120;Neupré;62121;NEUPRE;2;Wallonie
4120;Rotheux-Rimičre;62121;NEUPRE;2;Wallonie
4121;Neuville-en-Condroz;62121;NEUPRE;2;Wallonie
4122;Plainevaux;62121;NEUPRE;2;Wallonie
4130;Esneux;62032;ESNEUX;2;Wallonie
4130;Tilff;62032;ESNEUX;2;Wallonie
4140;Dolembreux;62100;SPRIMONT;2;Wallonie
4140;Gomzé-Andoumont;62100;SPRIMONT;2;Wallonie
4140;Rouvreux;62100;SPRIMONT;2;Wallonie
4140;Sprimont;62100;SPRIMONT;2;Wallonie
4141;Louveigné;62100;SPRIMONT;2;Wallonie
4160;Anthisnes;61079;ANTHISNES;2;Wallonie
4161;Villers-aux-Tours;61079;ANTHISNES;2;Wallonie
4162;Hody;61079;ANTHISNES;2;Wallonie
4163;Tavier;61079;ANTHISNES;2;Wallonie
4170;Comblain-au-Pont;62026;COMBLAIN-AU-PONT;2;Wallonie
4171;Poulseur;62026;COMBLAIN-AU-PONT;2;Wallonie
4180;Comblain-Fairon;61024;HAMOIR;2;Wallonie
4180;Comblain-la-Tour;61024;HAMOIR;2;Wallonie
4180;Hamoir;61024;HAMOIR;2;Wallonie
4181;Filot;61024;HAMOIR;2;Wallonie
4190;Ferričres;61019;FERRIERES;2;Wallonie
4190;My;61019;FERRIERES;2;Wallonie
4190;Vieuxville;61019;FERRIERES;2;Wallonie
4190;Werbomont;61019;FERRIERES;2;Wallonie
4190;Xhoris;61019;FERRIERES;2;Wallonie
4210;Burdinne;61010;BURDINNE;2;Wallonie
4210;Hannźche;61010;BURDINNE;2;Wallonie
4210;Lamontzée;61010;BURDINNE;2;Wallonie
4210;Marneffe;61010;BURDINNE;2;Wallonie
4210;Oteppe;61010;BURDINNE;2;Wallonie
4217;Héron;61028;HERON;2;Wallonie
4217;Lavoir;61028;HERON;2;Wallonie
4217;Waret-l'Evźque;61028;HERON;2;Wallonie
4218;Couthuin;61028;HERON;2;Wallonie
4219;Acosse;64075;WASSEIGES;2;Wallonie
4219;Ambresin;64075;WASSEIGES;2;Wallonie
4219;Meeffe;64075;WASSEIGES;2;Wallonie
4219;Wasseiges;64075;WASSEIGES;2;Wallonie
4250;Boėlhe;64029;GEER;2;Wallonie
4250;Geer;64029;GEER;2;Wallonie
4250;Hollogne-sur-Geer;64029;GEER;2;Wallonie
4250;Lens-Saint-Servais;64029;GEER;2;Wallonie
4252;Omal;64029;GEER;2;Wallonie
4253;Darion;64029;GEER;2;Wallonie
4254;Ligney;64029;GEER;2;Wallonie
4257;Berloz;64008;BERLOZ;2;Wallonie
4257;Corswarem;64008;BERLOZ;2;Wallonie
4257;Rosoux-Crenwick;64008;BERLOZ;2;Wallonie
4260;Avennes;64015;BRAIVES;2;Wallonie
4260;Braives;64015;BRAIVES;2;Wallonie
4260;Ciplet;64015;BRAIVES;2;Wallonie
4260;Fallais;64015;BRAIVES;2;Wallonie
4260;Fumal;64015;BRAIVES;2;Wallonie
4260;Ville-en-Hesbaye;64015;BRAIVES;2;Wallonie
4261;Latinne;64015;BRAIVES;2;Wallonie
4263;Tourinne (Lg.);64015;BRAIVES;2;Wallonie
4280;Abolens;64034;HANNUT;2;Wallonie
4280;Avernas-le-Bauduin;64034;HANNUT;2;Wallonie
4280;Avin;64034;HANNUT;2;Wallonie
4280;Bertrée;64034;HANNUT;2;Wallonie
4280;Blehen;64034;HANNUT;2;Wallonie
4280;Cras-Avernas;64034;HANNUT;2;Wallonie
4280;Crehen;64034;HANNUT;2;Wallonie
4280;Grand-Hallet;64034;HANNUT;2;Wallonie
4280;Hannut;64034;HANNUT;2;Wallonie
4280;Lens-Saint-Remy;64034;HANNUT;2;Wallonie
4280;Merdorp;64034;HANNUT;2;Wallonie
4280;Moxhe;64034;HANNUT;2;Wallonie
4280;Petit-Hallet;64034;HANNUT;2;Wallonie
4280;Poucet;64034;HANNUT;2;Wallonie
4280;Thisnes;64034;HANNUT;2;Wallonie
4280;Trognée;64034;HANNUT;2;Wallonie
4280;Villers-le-Peuplier;64034;HANNUT;2;Wallonie
4280;Wansin;64034;HANNUT;2;Wallonie
4287;Lincent;64047;LINCENT;2;Wallonie
4287;Pellaines;64047;LINCENT;2;Wallonie
4287;Racour;64047;LINCENT;2;Wallonie
4300;Bettincourt;64074;WAREMME;2;Wallonie
4300;Bleret;64074;WAREMME;2;Wallonie
4300;Bovenistier;64074;WAREMME;2;Wallonie
4300;Grand-Axhe;64074;WAREMME;2;Wallonie
4300;Lantremange;64074;WAREMME;2;Wallonie
4300;Oleye;64074;WAREMME;2;Wallonie
4300;Waremme;64074;WAREMME;2;Wallonie
4317;Aineffe;64076;FAIMES;2;Wallonie
4317;Borlez;64076;FAIMES;2;Wallonie
4317;Celles (Lg.);64076;FAIMES;2;Wallonie
4317;Faimes;64076;FAIMES;2;Wallonie
4317;Les Waleffes;64076;FAIMES;2;Wallonie
4317;Viemme;64076;FAIMES;2;Wallonie
4340;Awans;62006;AWANS;2;Wallonie
4340;Fooz;62006;AWANS;2;Wallonie
4340;Othée;62006;AWANS;2;Wallonie
4340;Villers-l'Evźque;62006;AWANS;2;Wallonie
4342;Hognoul;62006;AWANS;2;Wallonie
4347;Fexhe-le-Haut-Clocher;64025;FEXHE-LE-HAUT-CLOCHER;2;Wallonie
4347;Freloux;64025;FEXHE-LE-HAUT-CLOCHER;2;Wallonie
4347;Noville (Lg.);64025;FEXHE-LE-HAUT-CLOCHER;2;Wallonie
4347;Roloux;64025;FEXHE-LE-HAUT-CLOCHER;2;Wallonie
4347;Voroux-Goreux;64025;FEXHE-LE-HAUT-CLOCHER;2;Wallonie
4350;Lamine;64063;REMICOURT;2;Wallonie
4350;Momalle;64063;REMICOURT;2;Wallonie
4350;Pousset;64063;REMICOURT;2;Wallonie
4350;Remicourt;64063;REMICOURT;2;Wallonie
4351;Hodeige;64063;REMICOURT;2;Wallonie
4357;Donceel;64023;DONCEEL;2;Wallonie
4357;Haneffe;64023;DONCEEL;2;Wallonie
4357;Jeneffe (Lg.);64023;DONCEEL;2;Wallonie
4357;Limont;64023;DONCEEL;2;Wallonie
4360;Bergilers;64056;OREYE;2;Wallonie
4360;Grandville;64056;OREYE;2;Wallonie
4360;Lens-sur-Geer;64056;OREYE;2;Wallonie
4360;Oreye;64056;OREYE;2;Wallonie
4360;Otrange;64056;OREYE;2;Wallonie
4367;Crisnée;64021;CRISNEE;2;Wallonie
4367;Fize-le-Marsal;64021;CRISNEE;2;Wallonie
4367;Kemexhe;64021;CRISNEE;2;Wallonie
4367;Odeur;64021;CRISNEE;2;Wallonie
4367;Thys;64021;CRISNEE;2;Wallonie
4400;Awirs;62120;FLEMALLE;2;Wallonie
4400;Chokier;62120;FLEMALLE;2;Wallonie
4400;Flémalle;62120;FLEMALLE;2;Wallonie
4400;Flémalle-Grande;62120;FLEMALLE;2;Wallonie
4400;Flémalle-Haute;62120;FLEMALLE;2;Wallonie
4400;Gleixhe;62120;FLEMALLE;2;Wallonie
4400;Ivoz-Ramet;62120;FLEMALLE;2;Wallonie
4400;Mons-lez-Ličge;62120;FLEMALLE;2;Wallonie
4420;Montegnée;62093;SAINT-NICOLAS;2;Wallonie
4420;Saint-Nicolas (Lg.);62093;SAINT-NICOLAS;2;Wallonie
4420;Tilleur;62093;SAINT-NICOLAS;2;Wallonie
4430;Ans;62003;ANS;2;Wallonie
4431;Loncin;62003;ANS;2;Wallonie
4432;Alleur;62003;ANS;2;Wallonie
4432;Xhendremael;62003;ANS;2;Wallonie
4450;Juprelle;62060;JUPRELLE;2;Wallonie
4450;Lantin;62060;JUPRELLE;2;Wallonie
4450;Slins;62060;JUPRELLE;2;Wallonie
4451;Voroux-lez-Liers;62060;JUPRELLE;2;Wallonie
4452;Paifve;62060;JUPRELLE;2;Wallonie
4452;Wihogne;62060;JUPRELLE;2;Wallonie
4453;Villers-Saint-Siméon;62060;JUPRELLE;2;Wallonie
4458;Fexhe-Slins;62060;JUPRELLE;2;Wallonie
4460;Bierset;62118;GRACE-HOLLOGNE;2;Wallonie
4460;Grāce-Berleur;62118;GRACE-HOLLOGNE;2;Wallonie
4460;Grāce-Hollogne;62118;GRACE-HOLLOGNE;2;Wallonie
4460;Hollogne-aux-Pierres;62118;GRACE-HOLLOGNE;2;Wallonie
4460;Horion-Hozémont;62118;GRACE-HOLLOGNE;2;Wallonie
4460;Velroux;62118;GRACE-HOLLOGNE;2;Wallonie
4470;Saint-Georges-sur-Meuse;64065;SAINT-GEORGES-SUR-MEUSE;2;Wallonie
4480;Clermont-sous-Huy;61080;ENGIS;2;Wallonie
4480;Engis;61080;ENGIS;2;Wallonie
4480;Hermalle-sous-Huy;61080;ENGIS;2;Wallonie
4500;Ben-Ahin;61031;HUY;2;Wallonie
4500;Huy;61031;HUY;2;Wallonie
4500;Tihange;61031;HUY;2;Wallonie
4520;Antheit;61072;WANZE;2;Wallonie
4520;Bas-Oha;61072;WANZE;2;Wallonie
4520;Huccorgne;61072;WANZE;2;Wallonie
4520;Moha;61072;WANZE;2;Wallonie
4520;Vinalmont;61072;WANZE;2;Wallonie
4520;Wanze;61072;WANZE;2;Wallonie
4530;Fize-Fontaine;61068;VILLERS-LE-BOUILLET;2;Wallonie
4530;Vaux-et-Borset;61068;VILLERS-LE-BOUILLET;2;Wallonie
4530;Vieux-Waleffe;61068;VILLERS-LE-BOUILLET;2;Wallonie
4530;Villers-le-Bouillet;61068;VILLERS-LE-BOUILLET;2;Wallonie
4530;Warnant-Dreye;61068;VILLERS-LE-BOUILLET;2;Wallonie
4537;Chapon-Seraing;61063;VERLAINE;2;Wallonie
4537;Seraing-le-Chāteau;61063;VERLAINE;2;Wallonie
4537;Verlaine;61063;VERLAINE;2;Wallonie
4540;Amay;61003;AMAY;2;Wallonie
4540;Ampsin;61003;AMAY;2;Wallonie
4540;Flōne;61003;AMAY;2;Wallonie
4540;Jehay;61003;AMAY;2;Wallonie
4540;Ombret;61003;AMAY;2;Wallonie
4550;Nandrin;61043;NANDRIN;2;Wallonie
4550;Saint-Séverin;61043;NANDRIN;2;Wallonie
4550;Villers-le-Temple;61043;NANDRIN;2;Wallonie
4550;Yernée-Fraineux;61043;NANDRIN;2;Wallonie
4557;Abée;61081;TINLOT;2;Wallonie
4557;Fraiture;61081;TINLOT;2;Wallonie
4557;Ramelot;61081;TINLOT;2;Wallonie
4557;Seny;61081;TINLOT;2;Wallonie
4557;Soheit-Tinlot;61081;TINLOT;2;Wallonie
4557;Tinlot;61081;TINLOT;2;Wallonie
4560;Bois-et-Borsu;61012;CLAVIER;2;Wallonie
4560;Clavier;61012;CLAVIER;2;Wallonie
4560;Les Avins;61012;CLAVIER;2;Wallonie
4560;Ocquier;61012;CLAVIER;2;Wallonie
4560;Pailhe;61012;CLAVIER;2;Wallonie
4560;Terwagne;61012;CLAVIER;2;Wallonie
4570;Marchin;61039;MARCHIN;2;Wallonie
4570;Vyle-et-Tharoul;61039;MARCHIN;2;Wallonie
4577;Modave;61041;MODAVE;2;Wallonie
4577;Outrelouxhe;61041;MODAVE;2;Wallonie
4577;Strée-lez-Huy;61041;MODAVE;2;Wallonie
4577;Vierset-Barse;61041;MODAVE;2;Wallonie
4590;Ellemelle;61048;OUFFET;2;Wallonie
4590;Ouffet;61048;OUFFET;2;Wallonie
4590;Warzée;61048;OUFFET;2;Wallonie
4600;Lanaye;62108;VISE;2;Wallonie
4600;Lixhe;62108;VISE;2;Wallonie
4600;Richelle;62108;VISE;2;Wallonie
4600;Visé;62108;VISE;2;Wallonie
4601;Argenteau;62108;VISE;2;Wallonie
4602;Cheratte;62108;VISE;2;Wallonie
4606;Saint-André;62027;DALHEM;2;Wallonie
4607;Berneau;62027;DALHEM;2;Wallonie
4607;Bombaye;62027;DALHEM;2;Wallonie
4607;Dalhem;62027;DALHEM;2;Wallonie
4607;Feneur;62027;DALHEM;2;Wallonie
4607;Mortroux;62027;DALHEM;2;Wallonie
4608;Neufchāteau (Lg.);62027;DALHEM;2;Wallonie
4608;Warsage;62027;DALHEM;2;Wallonie
4610;Bellaire;62015;BEYNE-HEUSAY;2;Wallonie
4610;Beyne-Heusay;62015;BEYNE-HEUSAY;2;Wallonie
4610;Queue-du-Bois;62015;BEYNE-HEUSAY;2;Wallonie
4620;Fléron;62038;FLERON;2;Wallonie
4621;Retinne;62038;FLERON;2;Wallonie
4623;Magnée;62038;FLERON;2;Wallonie
4624;Romsée;62038;FLERON;2;Wallonie
4630;Ayeneux;62099;SOUMAGNE;2;Wallonie
4630;Micheroux;62099;SOUMAGNE;2;Wallonie
4630;Soumagne;62099;SOUMAGNE;2;Wallonie
4630;Tignée;62099;SOUMAGNE;2;Wallonie
4631;Evegnée;62099;SOUMAGNE;2;Wallonie
4632;Cérexhe-Heuseux;62099;SOUMAGNE;2;Wallonie
4633;Melen;62099;SOUMAGNE;2;Wallonie
4650;Chaineux;63035;HERVE;2;Wallonie
4650;Grand-Rechain;63035;HERVE;2;Wallonie
4650;Herve;63035;HERVE;2;Wallonie
4650;Julémont;63035;HERVE;2;Wallonie
4651;Battice;63035;HERVE;2;Wallonie
4652;Xhendelesse;63035;HERVE;2;Wallonie
4653;Bolland;63035;HERVE;2;Wallonie
4654;Charneux;63035;HERVE;2;Wallonie
4670;Blégny;62119;BLEGNY;2;Wallonie
4670;Mortier;62119;BLEGNY;2;Wallonie
4670;Trembleur;62119;BLEGNY;2;Wallonie
4671;Barchon;62119;BLEGNY;2;Wallonie
4671;Housse;62119;BLEGNY;2;Wallonie
4671;Saive;62119;BLEGNY;2;Wallonie
4672;Saint-Remy (Lg.);62119;BLEGNY;2;Wallonie
4680;Hermée;62079;OUPEYE;2;Wallonie
4680;Oupeye;62079;OUPEYE;2;Wallonie
4681;Hermalle-sous-Argenteau;62079;OUPEYE;2;Wallonie
4682;Heure-le-Romain;62079;OUPEYE;2;Wallonie
4682;Houtain-Saint-Siméon;62079;OUPEYE;2;Wallonie
4683;Vivegnis;62079;OUPEYE;2;Wallonie
4684;Haccourt;62079;OUPEYE;2;Wallonie
4690;Bassenge;62011;BASSENGE;2;Wallonie
4690;Boirs;62011;BASSENGE;2;Wallonie
4690;Eben-Emael;62011;BASSENGE;2;Wallonie
4690;Glons;62011;BASSENGE;2;Wallonie
4690;Roclenge-sur-Geer;62011;BASSENGE;2;Wallonie
4690;Wonck;62011;BASSENGE;2;Wallonie
4700;Eupen;63023;EUPEN;2;Wallonie
4701;Kettenis;63023;EUPEN;2;Wallonie
4710;Lontzen;63048;LONTZEN;2;Wallonie
4711;Walhorn;63048;LONTZEN;2;Wallonie
4720;Kelmis;63040;LA CALAMINE;2;Wallonie
4720;La Calamine;63040;LA CALAMINE;2;Wallonie
4721;Neu-Moresnet;63040;LA CALAMINE;2;Wallonie
4728;Hergenrath;63040;LA CALAMINE;2;Wallonie
4730;Hauset;63061;RAEREN;2;Wallonie
4730;Raeren;63061;RAEREN;2;Wallonie
4731;Eynatten;63061;RAEREN;2;Wallonie
4750;Bütgenbach;63013;BUTGENBACH;2;Wallonie
4750;Butgenbach;63013;BUTGENBACH;2;Wallonie
4750;Elsenborn;63013;BUTGENBACH;2;Wallonie
4760;Bullange;63012;BULLANGE;2;Wallonie
4760;Büllingen;63012;BULLANGE;2;Wallonie
4760;Manderfeld;63012;BULLANGE;2;Wallonie
4761;Rocherath;63012;BULLANGE;2;Wallonie
4770;Amblčve;63001;AMBLEVE;2;Wallonie
4770;Amel;63001;AMBLEVE;2;Wallonie
4770;Meyerode;63001;AMBLEVE;2;Wallonie
4771;Heppenbach;63001;AMBLEVE;2;Wallonie
4780;Recht;63067;SAINT-VITH;2;Wallonie
4780;Saint-Vith;63067;SAINT-VITH;2;Wallonie
4780;Sankt Vith;63067;SAINT-VITH;2;Wallonie
4782;Schoenberg;63067;SAINT-VITH;2;Wallonie
4782;Schönberg;63067;SAINT-VITH;2;Wallonie
4783;Lommersweiler;63067;SAINT-VITH;2;Wallonie
4784;Crombach;63067;SAINT-VITH;2;Wallonie
4790;Burg-Reuland;63087;BURG-REULAND;2;Wallonie
4790;Reuland;63087;BURG-REULAND;2;Wallonie
4791;Thommen;63087;BURG-REULAND;2;Wallonie
4800;Ensival;63079;VERVIERS;2;Wallonie
4800;Lambermont;63079;VERVIERS;2;Wallonie
4800;Petit-Rechain;63079;VERVIERS;2;Wallonie
4800;Verviers;63079;VERVIERS;2;Wallonie
4801;Stembert;63079;VERVIERS;2;Wallonie
4802;Heusy;63079;VERVIERS;2;Wallonie
4820;Dison;63020;DISON;2;Wallonie
4821;Andrimont;63020;DISON;2;Wallonie
4830;Limbourg;63046;LIMBOURG;2;Wallonie
4831;Bilstain;63046;LIMBOURG;2;Wallonie
4834;Goé;63046;LIMBOURG;2;Wallonie
4837;Baelen (Lg.);63004;BAELEN;2;Wallonie
4837;Membach;63004;BAELEN;2;Wallonie
4840;Welkenraedt;63084;WELKENRAEDT;2;Wallonie
4841;Henri-Chapelle;63084;WELKENRAEDT;2;Wallonie
4845;Jalhay;63038;JALHAY;2;Wallonie
4845;Sart-lez-Spa;63038;JALHAY;2;Wallonie
4850;Montzen;63088;PLOMBIERES;2;Wallonie
4850;Moresnet;63088;PLOMBIERES;2;Wallonie
4850;Plombičres;63088;PLOMBIERES;2;Wallonie
4851;Gemmenich;63088;PLOMBIERES;2;Wallonie
4851;Sippenaeken;63088;PLOMBIERES;2;Wallonie
4852;Hombourg;63088;PLOMBIERES;2;Wallonie
4860;Cornesse;63058;PEPINSTER;2;Wallonie
4860;Pepinster;63058;PEPINSTER;2;Wallonie
4860;Wegnez;63058;PEPINSTER;2;Wallonie
4861;Soiron;63058;PEPINSTER;2;Wallonie
4870;Forźt;62122;TROOZ;2;Wallonie
4870;Fraipont;62122;TROOZ;2;Wallonie
4870;Nessonvaux;62122;TROOZ;2;Wallonie
4870;Trooz;62122;TROOZ;2;Wallonie
4877;Olne;63057;OLNE;2;Wallonie
4880;Aubel;63003;AUBEL;2;Wallonie
4890;Clermont (Lg.);63089;THIMISTER-CLERMONT;2;Wallonie
4890;Thimister;63089;THIMISTER-CLERMONT;2;Wallonie
4890;Thimister-Clermont;63089;THIMISTER-CLERMONT;2;Wallonie
4900;Spa;63072;SPA;2;Wallonie
4910;La Reid;63076;THEUX;2;Wallonie
4910;Polleur;63076;THEUX;2;Wallonie
4910;Theux;63076;THEUX;2;Wallonie
4920;Aywaille;62009;AYWAILLE;2;Wallonie
4920;Ernonheid;62009;AYWAILLE;2;Wallonie
4920;Harzé;62009;AYWAILLE;2;Wallonie
4920;Sougné-Remouchamps;62009;AYWAILLE;2;Wallonie
4950;Faymonville;63080;WAIMES;2;Wallonie
4950;Robertville;63080;WAIMES;2;Wallonie
4950;Sourbrodt;63080;WAIMES;2;Wallonie
4950;Waimes;63080;WAIMES;2;Wallonie
4950;Weismes;63080;WAIMES;2;Wallonie
4960;Bellevaux-Ligneuville;63049;MALMEDY;2;Wallonie
4960;Bevercé;63049;MALMEDY;2;Wallonie
4960;Malmedy;63049;MALMEDY;2;Wallonie
4970;Francorchamps;63073;STAVELOT;2;Wallonie
4970;Stavelot;63073;STAVELOT;2;Wallonie
4980;Fosse (Lg.);63086;TROIS-PONTS;2;Wallonie
4980;Trois-Ponts;63086;TROIS-PONTS;2;Wallonie
4980;Wanne;63086;TROIS-PONTS;2;Wallonie
4983;Basse-Bodeux;63086;TROIS-PONTS;2;Wallonie
4987;Chevron;63075;STOUMONT;2;Wallonie
4987;La Gleize;63075;STOUMONT;2;Wallonie
4987;Lorcé;63075;STOUMONT;2;Wallonie
4987;Rahier;63075;STOUMONT;2;Wallonie
4987;Stoumont;63075;STOUMONT;2;Wallonie
4990;Arbrefontaine;63045;LIERNEUX;2;Wallonie
4990;Bra;63045;LIERNEUX;2;Wallonie
4990;Lierneux;63045;LIERNEUX;2;Wallonie
5000;Beez;92094;NAMUR;2;Wallonie
5000;Namur;92094;NAMUR;2;Wallonie
5001;Belgrade;92094;NAMUR;2;Wallonie
5002;Saint-Servais;92094;NAMUR;2;Wallonie
5003;Saint-Marc;92094;NAMUR;2;Wallonie
5004;Bouge;92094;NAMUR;2;Wallonie
5020;Champion;92094;NAMUR;2;Wallonie
5020;Daussoulx;92094;NAMUR;2;Wallonie
5020;Flawinne;92094;NAMUR;2;Wallonie
5020;Malonne;92094;NAMUR;2;Wallonie
5020;Suarlée;92094;NAMUR;2;Wallonie
5020;Temploux;92094;NAMUR;2;Wallonie
5020;Vedrin;92094;NAMUR;2;Wallonie
5021;Boninne;92094;NAMUR;2;Wallonie
5022;Cognelée;92094;NAMUR;2;Wallonie
5024;Gelbressée;92094;NAMUR;2;Wallonie
5024;Marche-les-Dames;92094;NAMUR;2;Wallonie
5030;Beuzet;92142;GEMBLOUX;2;Wallonie
5030;Ernage;92142;GEMBLOUX;2;Wallonie
5030;Gembloux;92142;GEMBLOUX;2;Wallonie
5030;Grand-Manil;92142;GEMBLOUX;2;Wallonie
5030;Lonzée;92142;GEMBLOUX;2;Wallonie
5030;Sauveničre;92142;GEMBLOUX;2;Wallonie
5031;Grand-Leez;92142;GEMBLOUX;2;Wallonie
5032;Bossičre;92142;GEMBLOUX;2;Wallonie
5032;Bothey;92142;GEMBLOUX;2;Wallonie
5032;Corroy-le-Chāteau;92142;GEMBLOUX;2;Wallonie
5032;Isnes;92142;GEMBLOUX;2;Wallonie
5032;Mazy;92142;GEMBLOUX;2;Wallonie
5060;Arsimont;92137;SAMBREVILLE;2;Wallonie
5060;Auvelais;92137;SAMBREVILLE;2;Wallonie
5060;Falisolle;92137;SAMBREVILLE;2;Wallonie
5060;Keumiée;92137;SAMBREVILLE;2;Wallonie
5060;Moignelée;92137;SAMBREVILLE;2;Wallonie
5060;Sambreville;92137;SAMBREVILLE;2;Wallonie
5060;Tamines;92137;SAMBREVILLE;2;Wallonie
5060;Velaine-sur-Sambre;92137;SAMBREVILLE;2;Wallonie
5070;Aisemont;92048;FOSSES-LA-VILLE;2;Wallonie
5070;Fosses-la-Ville;92048;FOSSES-LA-VILLE;2;Wallonie
5070;Le Roux;92048;FOSSES-LA-VILLE;2;Wallonie
5070;Sart-Eustache;92048;FOSSES-LA-VILLE;2;Wallonie
5070;Sart-Saint-Laurent;92048;FOSSES-LA-VILLE;2;Wallonie
5070;Vitrival;92048;FOSSES-LA-VILLE;2;Wallonie
5080;Emines;92141;LA BRUYERE;2;Wallonie
5080;La Bruyčre;92141;LA BRUYERE;2;Wallonie
5080;Rhisnes;92141;LA BRUYERE;2;Wallonie
5080;Villers-lez-Heest;92141;LA BRUYERE;2;Wallonie
5080;Warisoulx;92141;LA BRUYERE;2;Wallonie
5081;Bovesse;92141;LA BRUYERE;2;Wallonie
5081;Meux;92141;LA BRUYERE;2;Wallonie
5081;Saint-Denis-Bovesse;92141;LA BRUYERE;2;Wallonie
5100;Dave;92094;NAMUR;2;Wallonie
5100;Jambes (Namur);92094;NAMUR;2;Wallonie
5100;Naninne;92094;NAMUR;2;Wallonie
5100;Wépion;92094;NAMUR;2;Wallonie
5100;Wierde;92094;NAMUR;2;Wallonie
5101;Erpent;92094;NAMUR;2;Wallonie
5101;Lives-sur-Meuse;92094;NAMUR;2;Wallonie
5101;Loyers;92094;NAMUR;2;Wallonie
5140;Boignée;92114;SOMBREFFE;2;Wallonie
5140;Ligny;92114;SOMBREFFE;2;Wallonie
5140;Sombreffe;92114;SOMBREFFE;2;Wallonie
5140;Tongrinne;92114;SOMBREFFE;2;Wallonie
5150;Floreffe;92045;FLOREFFE;2;Wallonie
5150;Floriffoux;92045;FLOREFFE;2;Wallonie
5150;Franičre;92045;FLOREFFE;2;Wallonie
5150;Soye (Nam.);92045;FLOREFFE;2;Wallonie
5170;Arbre (Nam.);92101;PROFONDEVILLE;2;Wallonie
5170;Bois-de-Villers;92101;PROFONDEVILLE;2;Wallonie
5170;Lesve;92101;PROFONDEVILLE;2;Wallonie
5170;Lustin;92101;PROFONDEVILLE;2;Wallonie
5170;Profondeville;92101;PROFONDEVILLE;2;Wallonie
5170;Rivičre;92101;PROFONDEVILLE;2;Wallonie
5190;Balātre;92140;JEMEPPE-SUR-SAMBRE;2;Wallonie
5190;Ham-sur-Sambre;92140;JEMEPPE-SUR-SAMBRE;2;Wallonie
5190;Jemeppe-sur-Sambre;92140;JEMEPPE-SUR-SAMBRE;2;Wallonie
5190;Mornimont;92140;JEMEPPE-SUR-SAMBRE;2;Wallonie
5190;Moustier-sur-Sambre;92140;JEMEPPE-SUR-SAMBRE;2;Wallonie
5190;Onoz;92140;JEMEPPE-SUR-SAMBRE;2;Wallonie
5190;Saint-Martin;92140;JEMEPPE-SUR-SAMBRE;2;Wallonie
5190;Spy;92140;JEMEPPE-SUR-SAMBRE;2;Wallonie
5300;Andenne;92003;ANDENNE;2;Wallonie
5300;Bonneville;92003;ANDENNE;2;Wallonie
5300;Coutisse;92003;ANDENNE;2;Wallonie
5300;Landenne;92003;ANDENNE;2;Wallonie
5300;Maizeret;92003;ANDENNE;2;Wallonie
5300;Namźche;92003;ANDENNE;2;Wallonie
5300;Sclayn;92003;ANDENNE;2;Wallonie
5300;Seilles;92003;ANDENNE;2;Wallonie
5300;Thon;92003;ANDENNE;2;Wallonie
5300;Vezin;92003;ANDENNE;2;Wallonie
5310;Aische-en-Refail;92035;EGHEZEE;2;Wallonie
5310;Bolinne;92035;EGHEZEE;2;Wallonie
5310;Boneffe;92035;EGHEZEE;2;Wallonie
5310;Branchon;92035;EGHEZEE;2;Wallonie
5310;Dhuy;92035;EGHEZEE;2;Wallonie
5310;Eghezée;92035;EGHEZEE;2;Wallonie
5310;Hanret;92035;EGHEZEE;2;Wallonie
5310;Leuze (Nam.);92035;EGHEZEE;2;Wallonie
5310;Liernu;92035;EGHEZEE;2;Wallonie
5310;Longchamps (Nam.);92035;EGHEZEE;2;Wallonie
5310;Mehaigne;92035;EGHEZEE;2;Wallonie
5310;Noville-sur-Méhaigne;92035;EGHEZEE;2;Wallonie
5310;Saint-Germain;92035;EGHEZEE;2;Wallonie
5310;Taviers (Nam.);92035;EGHEZEE;2;Wallonie
5310;Upigny;92035;EGHEZEE;2;Wallonie
5310;Waret-la-Chaussée;92035;EGHEZEE;2;Wallonie
5330;Assesse;92006;ASSESSE;2;Wallonie
5330;Maillen;92006;ASSESSE;2;Wallonie
5330;Sart-Bernard;92006;ASSESSE;2;Wallonie
5332;Crupet;92006;ASSESSE;2;Wallonie
5333;Sorinne-la-Longue;92006;ASSESSE;2;Wallonie
5334;Florée;92006;ASSESSE;2;Wallonie
5336;Courričre;92006;ASSESSE;2;Wallonie
5340;Faulx-les-Tombes;92054;GESVES;2;Wallonie
5340;Gesves;92054;GESVES;2;Wallonie
5340;Haltinne;92054;GESVES;2;Wallonie
5340;Mozet;92054;GESVES;2;Wallonie
5340;Sorée;92054;GESVES;2;Wallonie
5350;Evelette;92097;OHEY;2;Wallonie
5350;Ohey;92097;OHEY;2;Wallonie
5351;Haillot;92097;OHEY;2;Wallonie
5352;Perwez-Haillot;92097;OHEY;2;Wallonie
5353;Goesnes;92097;OHEY;2;Wallonie
5354;Jallet;92097;OHEY;2;Wallonie
5360;Hamois;91059;HAMOIS;2;Wallonie
5360;Natoye;91059;HAMOIS;2;Wallonie
5361;Mohiville;91059;HAMOIS;2;Wallonie
5361;Scy;91059;HAMOIS;2;Wallonie
5362;Achet;91059;HAMOIS;2;Wallonie
5363;Emptinne;91059;HAMOIS;2;Wallonie
5364;Schaltin;91059;HAMOIS;2;Wallonie
5370;Barvaux-Condroz;91064;HAVELANGE;2;Wallonie
5370;Flostoy;91064;HAVELANGE;2;Wallonie
5370;Havelange;91064;HAVELANGE;2;Wallonie
5370;Jeneffe (Nam.);91064;HAVELANGE;2;Wallonie
5370;Porcheresse (Nam.);91064;HAVELANGE;2;Wallonie
5370;Verlée;91064;HAVELANGE;2;Wallonie
5372;Méan;91064;HAVELANGE;2;Wallonie
5374;Maffe;91064;HAVELANGE;2;Wallonie
5376;Miécret;91064;HAVELANGE;2;Wallonie
5377;Baillonville;91120;SOMME-LEUZE;2;Wallonie
5377;Bonsin;91120;SOMME-LEUZE;2;Wallonie
5377;Heure (Nam.);91120;SOMME-LEUZE;2;Wallonie
5377;Hogne;91120;SOMME-LEUZE;2;Wallonie
5377;Nettinne;91120;SOMME-LEUZE;2;Wallonie
5377;Noiseux;91120;SOMME-LEUZE;2;Wallonie
5377;Sinsin;91120;SOMME-LEUZE;2;Wallonie
5377;Somme-Leuze;91120;SOMME-LEUZE;2;Wallonie
5377;Waillet;91120;SOMME-LEUZE;2;Wallonie
5380;Bierwart;92138;FERNELMONT;2;Wallonie
5380;Cortil-Wodon;92138;FERNELMONT;2;Wallonie
5380;Fernelmont;92138;FERNELMONT;2;Wallonie
5380;Forville;92138;FERNELMONT;2;Wallonie
5380;Franc-Waret;92138;FERNELMONT;2;Wallonie
5380;Hemptinne (Fernelmont);92138;FERNELMONT;2;Wallonie
5380;Hingeon;92138;FERNELMONT;2;Wallonie
5380;Marchovelette;92138;FERNELMONT;2;Wallonie
5380;Noville-les-Bois;92138;FERNELMONT;2;Wallonie
5380;Pontillas;92138;FERNELMONT;2;Wallonie
5380;Tillier;92138;FERNELMONT;2;Wallonie
5500;Anseremme;91034;DINANT;2;Wallonie
5500;Bouvignes-sur-Meuse;91034;DINANT;2;Wallonie
5500;Dinant;91034;DINANT;2;Wallonie
5500;Dréhance;91034;DINANT;2;Wallonie
5500;Falmagne;91034;DINANT;2;Wallonie
5500;Falmignoul;91034;DINANT;2;Wallonie
5500;Furfooz;91034;DINANT;2;Wallonie
5501;Lisogne;91034;DINANT;2;Wallonie
5502;Thynes;91034;DINANT;2;Wallonie
5503;Sorinnes;91034;DINANT;2;Wallonie
5504;Foy-Notre-Dame;91034;DINANT;2;Wallonie
5520;Anthée;91103;ONHAYE;2;Wallonie
5520;Onhaye;91103;ONHAYE;2;Wallonie
5521;Serville;91103;ONHAYE;2;Wallonie
5522;Falaėn;91103;ONHAYE;2;Wallonie
5523;Sommičre;91103;ONHAYE;2;Wallonie
5523;Weillen;91103;ONHAYE;2;Wallonie
5524;Gerin;91103;ONHAYE;2;Wallonie
5530;Dorinne;91141;YVOIR;2;Wallonie
5530;Durnal;91141;YVOIR;2;Wallonie
5530;Evrehailles;91141;YVOIR;2;Wallonie
5530;Godinne;91141;YVOIR;2;Wallonie
5530;Houx;91141;YVOIR;2;Wallonie
5530;Mont (Nam.);91141;YVOIR;2;Wallonie
5530;Purnode;91141;YVOIR;2;Wallonie
5530;Spontin;91141;YVOIR;2;Wallonie
5530;Yvoir;91141;YVOIR;2;Wallonie
5537;Anhée;91005;ANHEE;2;Wallonie
5537;Annevoie-Rouillon;91005;ANHEE;2;Wallonie
5537;Bioul;91005;ANHEE;2;Wallonie
5537;Denée;91005;ANHEE;2;Wallonie
5537;Haut-le-Wastia;91005;ANHEE;2;Wallonie
5537;Sosoye;91005;ANHEE;2;Wallonie
5537;Warnant;91005;ANHEE;2;Wallonie
5540;Hastičre;91142;HASTIERE;2;Wallonie
5540;Hastičre-Lavaux;91142;HASTIERE;2;Wallonie
5540;Hermeton-sur-Meuse;91142;HASTIERE;2;Wallonie
5540;Waulsort;91142;HASTIERE;2;Wallonie
5541;Hastičre-par-Delą;91142;HASTIERE;2;Wallonie
5542;Blaimont;91142;HASTIERE;2;Wallonie
5543;Heer;91142;HASTIERE;2;Wallonie
5544;Agimont;91142;HASTIERE;2;Wallonie
5550;Alle;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Bagimont;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Bohan;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Chairičre;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Laforźt;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Membre;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Mouzaive;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Nafraiture;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Orchimont;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Pussemange;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Sugny;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5550;Vresse-sur-Semois;91143;VRESSE-SUR-SEMOIS;2;Wallonie
5555;Baillamont;91015;BIEVRE;2;Wallonie
5555;Bellefontaine (Nam.);91015;BIEVRE;2;Wallonie
5555;Bievre;91015;BIEVRE;2;Wallonie
5555;Cornimont;91015;BIEVRE;2;Wallonie
5555;Graide;91015;BIEVRE;2;Wallonie
5555;Gros-Fays;91015;BIEVRE;2;Wallonie
5555;Monceau-en-Ardenne;91015;BIEVRE;2;Wallonie
5555;Naomé;91015;BIEVRE;2;Wallonie
5555;Oizy;91015;BIEVRE;2;Wallonie
5555;Petit-Fays;91015;BIEVRE;2;Wallonie
5560;Ciergnon;91072;HOUYET;2;Wallonie
5560;Finnevaux;91072;HOUYET;2;Wallonie
5560;Houyet;91072;HOUYET;2;Wallonie
5560;Hulsonniaux;91072;HOUYET;2;Wallonie
5560;Mesnil-Eglise;91072;HOUYET;2;Wallonie
5560;Mesnil-Saint-Blaise;91072;HOUYET;2;Wallonie
5561;Celles (Nam.);91072;HOUYET;2;Wallonie
5562;Custinne;91072;HOUYET;2;Wallonie
5563;Hour;91072;HOUYET;2;Wallonie
5564;Wanlin;91072;HOUYET;2;Wallonie
5570;Baronville;91013;BEAURAING;2;Wallonie
5570;Beauraing;91013;BEAURAING;2;Wallonie
5570;Dion;91013;BEAURAING;2;Wallonie
5570;Felenne;91013;BEAURAING;2;Wallonie
5570;Feschaux;91013;BEAURAING;2;Wallonie
5570;Honnay;91013;BEAURAING;2;Wallonie
5570;Javingue;91013;BEAURAING;2;Wallonie
5570;Vonźche;91013;BEAURAING;2;Wallonie
5570;Wancennes;91013;BEAURAING;2;Wallonie
5570;Winenne;91013;BEAURAING;2;Wallonie
5571;Wiesme;91013;BEAURAING;2;Wallonie
5572;Focant;91013;BEAURAING;2;Wallonie
5573;Martouzin-Neuville;91013;BEAURAING;2;Wallonie
5574;Pondrōme;91013;BEAURAING;2;Wallonie
5575;Bourseigne-Neuve;91054;GEDINNE;2;Wallonie
5575;Bourseigne-Vieille;91054;GEDINNE;2;Wallonie
5575;Gedinne;91054;GEDINNE;2;Wallonie
5575;Houdremont;91054;GEDINNE;2;Wallonie
5575;Louette-Saint-Denis;91054;GEDINNE;2;Wallonie
5575;Louette-Saint-Pierre;91054;GEDINNE;2;Wallonie
5575;Malvoisin;91054;GEDINNE;2;Wallonie
5575;Patignies;91054;GEDINNE;2;Wallonie
5575;Rienne;91054;GEDINNE;2;Wallonie
5575;Sart-Custinne;91054;GEDINNE;2;Wallonie
5575;Vencimont;91054;GEDINNE;2;Wallonie
5575;Willerzie;91054;GEDINNE;2;Wallonie
5576;Froidfontaine;91013;BEAURAING;2;Wallonie
5580;Ave-et-Auffe;91114;ROCHEFORT;2;Wallonie
5580;Buissonville;91114;ROCHEFORT;2;Wallonie
5580;Eprave;91114;ROCHEFORT;2;Wallonie
5580;Han-sur-Lesse;91114;ROCHEFORT;2;Wallonie
5580;Jemelle;91114;ROCHEFORT;2;Wallonie
5580;Lavaux-Sainte-Anne;91114;ROCHEFORT;2;Wallonie
5580;Lessive;91114;ROCHEFORT;2;Wallonie
5580;Mont-Gauthier;91114;ROCHEFORT;2;Wallonie
5580;Rochefort;91114;ROCHEFORT;2;Wallonie
5580;Villers-sur-Lesse;91114;ROCHEFORT;2;Wallonie
5580;Wavreille;91114;ROCHEFORT;2;Wallonie
5590;Achźne;91030;CINEY;2;Wallonie
5590;Braibant;91030;CINEY;2;Wallonie
5590;Chevetogne;91030;CINEY;2;Wallonie
5590;Ciney;91030;CINEY;2;Wallonie
5590;Conneux;91030;CINEY;2;Wallonie
5590;Haversin;91030;CINEY;2;Wallonie
5590;Leignon;91030;CINEY;2;Wallonie
5590;Pessoux;91030;CINEY;2;Wallonie
5590;Serinchamps;91030;CINEY;2;Wallonie
5590;Sovet;91030;CINEY;2;Wallonie
5600;Fagnolle;93056;PHILIPPEVILLE;2;Wallonie
5600;Franchimont;93056;PHILIPPEVILLE;2;Wallonie
5600;Jamagne;93056;PHILIPPEVILLE;2;Wallonie
5600;Jamiolle;93056;PHILIPPEVILLE;2;Wallonie
5600;Merlemont;93056;PHILIPPEVILLE;2;Wallonie
5600;Neuville (Philippeville);93056;PHILIPPEVILLE;2;Wallonie
5600;Omezée;93056;PHILIPPEVILLE;2;Wallonie
5600;Philippeville;93056;PHILIPPEVILLE;2;Wallonie
5600;Roly;93056;PHILIPPEVILLE;2;Wallonie
5600;Romedenne;93056;PHILIPPEVILLE;2;Wallonie
5600;Samart;93056;PHILIPPEVILLE;2;Wallonie
5600;Sart-en-Fagne;93056;PHILIPPEVILLE;2;Wallonie
5600;Sautour;93056;PHILIPPEVILLE;2;Wallonie
5600;Surice;93056;PHILIPPEVILLE;2;Wallonie
5600;Villers-en-Fagne;93056;PHILIPPEVILLE;2;Wallonie
5600;Villers-le-Gambon;93056;PHILIPPEVILLE;2;Wallonie
5600;Vodecée;93056;PHILIPPEVILLE;2;Wallonie
5620;Corenne;93022;FLORENNES;2;Wallonie
5620;Flavion;93022;FLORENNES;2;Wallonie
5620;Florennes;93022;FLORENNES;2;Wallonie
5620;Hemptinne-lez-Florennes;93022;FLORENNES;2;Wallonie
5620;Morville;93022;FLORENNES;2;Wallonie
5620;Rosée;93022;FLORENNES;2;Wallonie
5620;Saint-Aubin;93022;FLORENNES;2;Wallonie
5621;Hanzinelle;93022;FLORENNES;2;Wallonie
5621;Hanzinne;93022;FLORENNES;2;Wallonie
5621;Morialmé;93022;FLORENNES;2;Wallonie
5621;Thy-le-Bauduin;93022;FLORENNES;2;Wallonie
5630;Cerfontaine;93010;CERFONTAINE;2;Wallonie
5630;Daussois;93010;CERFONTAINE;2;Wallonie
5630;Senzeille;93010;CERFONTAINE;2;Wallonie
5630;Silenrieux;93010;CERFONTAINE;2;Wallonie
5630;Soumoy;93010;CERFONTAINE;2;Wallonie
5630;Villers-Deux-Eglises;93010;CERFONTAINE;2;Wallonie
5640;Biesme;92087;METTET;2;Wallonie
5640;Biesmerée;92087;METTET;2;Wallonie
5640;Graux;92087;METTET;2;Wallonie
5640;Mettet;92087;METTET;2;Wallonie
5640;Oret;92087;METTET;2;Wallonie
5640;Saint-Gérard;92087;METTET;2;Wallonie
5641;Furnaux;92087;METTET;2;Wallonie
5644;Ermeton-sur-Biert;92087;METTET;2;Wallonie
5646;Stave;92087;METTET;2;Wallonie
5650;Castillon;93088;WALCOURT;2;Wallonie
5650;Chastrčs;93088;WALCOURT;2;Wallonie
5650;Clermont (Nam.);93088;WALCOURT;2;Wallonie
5650;Fontenelle;93088;WALCOURT;2;Wallonie
5650;Fraire;93088;WALCOURT;2;Wallonie
5650;Pry;93088;WALCOURT;2;Wallonie
5650;Vogenée;93088;WALCOURT;2;Wallonie
5650;Walcourt;93088;WALCOURT;2;Wallonie
5650;Yves-Gomezée;93088;WALCOURT;2;Wallonie
5651;Berzée;93088;WALCOURT;2;Wallonie
5651;Gourdinne;93088;WALCOURT;2;Wallonie
5651;Laneffe;93088;WALCOURT;2;Wallonie
5651;Rognée;93088;WALCOURT;2;Wallonie
5651;Somzée;93088;WALCOURT;2;Wallonie
5651;Tarcienne;93088;WALCOURT;2;Wallonie
5651;Thy-le-Chāteau;93088;WALCOURT;2;Wallonie
5660;Aublain;93014;COUVIN;2;Wallonie
5660;Boussu-en-Fagne;93014;COUVIN;2;Wallonie
5660;Brūly;93014;COUVIN;2;Wallonie
5660;Brūly-de-Pesche;93014;COUVIN;2;Wallonie
5660;Couvin;93014;COUVIN;2;Wallonie
5660;Cul-des-Sarts;93014;COUVIN;2;Wallonie
5660;Dailly;93014;COUVIN;2;Wallonie
5660;Frasnes (Nam.);93014;COUVIN;2;Wallonie
5660;Gonrieux;93014;COUVIN;2;Wallonie
5660;Mariembourg;93014;COUVIN;2;Wallonie
5660;Pesche;93014;COUVIN;2;Wallonie
5660;Petigny;93014;COUVIN;2;Wallonie
5660;Petite-Chapelle;93014;COUVIN;2;Wallonie
5660;Presgaux;93014;COUVIN;2;Wallonie
5670;Dourbes;93090;VIROINVAL;2;Wallonie
5670;Le Mesnil;93090;VIROINVAL;2;Wallonie
5670;Mazée;93090;VIROINVAL;2;Wallonie
5670;Nismes;93090;VIROINVAL;2;Wallonie
5670;Oignies-en-Thiérache;93090;VIROINVAL;2;Wallonie
5670;Olloy-sur-Viroin;93090;VIROINVAL;2;Wallonie
5670;Treignes;93090;VIROINVAL;2;Wallonie
5670;Vierves-sur-Viroin;93090;VIROINVAL;2;Wallonie
5670;Viroinval;93090;VIROINVAL;2;Wallonie
5680;Doische;93018;DOISCHE;2;Wallonie
5680;Gimnée;93018;DOISCHE;2;Wallonie
5680;Gochenée;93018;DOISCHE;2;Wallonie
5680;Matagne-la-Grande;93018;DOISCHE;2;Wallonie
5680;Matagne-la-Petite;93018;DOISCHE;2;Wallonie
5680;Niverlée;93018;DOISCHE;2;Wallonie
5680;Romerée;93018;DOISCHE;2;Wallonie
5680;Soulme;93018;DOISCHE;2;Wallonie
5680;Vaucelles;93018;DOISCHE;2;Wallonie
5680;Vodelée;93018;DOISCHE;2;Wallonie
6000;Charleroi;52011;CHARLEROI;2;Wallonie
6001;Marcinelle;52011;CHARLEROI;2;Wallonie
6010;Couillet;52011;CHARLEROI;2;Wallonie
6020;Dampremy;52011;CHARLEROI;2;Wallonie
6030;Goutroux;52011;CHARLEROI;2;Wallonie
6030;Marchienne-au-Pont;52011;CHARLEROI;2;Wallonie
6031;Monceau-sur-Sambre;52011;CHARLEROI;2;Wallonie
6032;Mont-sur-Marchienne;52011;CHARLEROI;2;Wallonie
6040;Jumet (Charleroi);52011;CHARLEROI;2;Wallonie
6041;Gosselies;52011;CHARLEROI;2;Wallonie
6042;Lodelinsart;52011;CHARLEROI;2;Wallonie
6043;Ransart;52011;CHARLEROI;2;Wallonie
6044;Roux;52011;CHARLEROI;2;Wallonie
6060;Gilly (Charleroi);52011;CHARLEROI;2;Wallonie
6061;Montignies-sur-Sambre;52011;CHARLEROI;2;Wallonie
6110;Montigny-le-Tilleul;52048;MONTIGNY-LE-TILLEUL;2;Wallonie
6111;Landelies;52048;MONTIGNY-LE-TILLEUL;2;Wallonie
6120;Cour-sur-Heure;56086;HAM-SUR-HEURE-NALINNES;2;Wallonie
6120;Ham-sur-Heure;56086;HAM-SUR-HEURE-NALINNES;2;Wallonie
6120;Ham-sur-Heure-Nalinnes;56086;HAM-SUR-HEURE-NALINNES;2;Wallonie
6120;Jamioulx;56086;HAM-SUR-HEURE-NALINNES;2;Wallonie
6120;Marbaix (Ht.);56086;HAM-SUR-HEURE-NALINNES;2;Wallonie
6120;Nalinnes;56086;HAM-SUR-HEURE-NALINNES;2;Wallonie
6140;Fontaine-l'Evźque;52022;FONTAINE-L'EVEQUE;2;Wallonie
6141;Forchies-la-Marche;52022;FONTAINE-L'EVEQUE;2;Wallonie
6142;Leernes;52022;FONTAINE-L'EVEQUE;2;Wallonie
6150;Anderlues;56001;ANDERLUES;2;Wallonie
6180;Courcelles;52015;COURCELLES;2;Wallonie
6181;Gouy-lez-Piéton;52015;COURCELLES;2;Wallonie
6182;Souvret;52015;COURCELLES;2;Wallonie
6183;Trazegnies;52015;COURCELLES;2;Wallonie
6200;Bouffioulx;52012;CHATELET;2;Wallonie
6200;Chātelet;52012;CHATELET;2;Wallonie
6200;Chātelineau;52012;CHATELET;2;Wallonie
6210;Frasnes-lez-Gosselies;52075;LES BONS VILLERS;2;Wallonie
6210;Les Bons Villers;52075;LES BONS VILLERS;2;Wallonie
6210;Rčves;52075;LES BONS VILLERS;2;Wallonie
6210;Villers-Perwin;52075;LES BONS VILLERS;2;Wallonie
6210;Wayaux;52075;LES BONS VILLERS;2;Wallonie
6211;Mellet;52075;LES BONS VILLERS;2;Wallonie
6220;Fleurus;52021;FLEURUS;2;Wallonie
6220;Heppignies;52021;FLEURUS;2;Wallonie
6220;Lambusart;52021;FLEURUS;2;Wallonie
6220;Wangenies;52021;FLEURUS;2;Wallonie
6221;Saint-Amand;52021;FLEURUS;2;Wallonie
6222;Brye;52021;FLEURUS;2;Wallonie
6223;Wagnelée;52021;FLEURUS;2;Wallonie
6224;Wanfercée-Baulet;52021;FLEURUS;2;Wallonie
6230;Buzet;52055;PONT-A-CELLES;2;Wallonie
6230;Obaix;52055;PONT-A-CELLES;2;Wallonie
6230;Pont-ą-Celles;52055;PONT-A-CELLES;2;Wallonie
6230;Thiméon;52055;PONT-A-CELLES;2;Wallonie
6230;Viesville;52055;PONT-A-CELLES;2;Wallonie
6238;Liberchies;52055;PONT-A-CELLES;2;Wallonie
6238;Luttre;52055;PONT-A-CELLES;2;Wallonie
6240;Farciennes;52018;FARCIENNES;2;Wallonie
6240;Pironchamps;52018;FARCIENNES;2;Wallonie
6250;Aiseau;52074;AISEAU-PRESLES;2;Wallonie
6250;Aiseau-Presles;52074;AISEAU-PRESLES;2;Wallonie
6250;Pont-de-Loup;52074;AISEAU-PRESLES;2;Wallonie
6250;Presles;52074;AISEAU-PRESLES;2;Wallonie
6250;Roselies;52074;AISEAU-PRESLES;2;Wallonie
6280;Acoz;52025;GERPINNES;2;Wallonie
6280;Gerpinnes;52025;GERPINNES;2;Wallonie
6280;Gougnies;52025;GERPINNES;2;Wallonie
6280;Joncret;52025;GERPINNES;2;Wallonie
6280;Loverval;52025;GERPINNES;2;Wallonie
6280;Villers-Poterie;52025;GERPINNES;2;Wallonie
6440;Boussu-lez-Walcourt;56029;FROID-CHAPELLE;2;Wallonie
6440;Fourbechies;56029;FROID-CHAPELLE;2;Wallonie
6440;Froidchapelle;56029;FROID-CHAPELLE;2;Wallonie
6440;Vergnies;56029;FROID-CHAPELLE;2;Wallonie
6441;Erpion;56029;FROID-CHAPELLE;2;Wallonie
6460;Bailičvre;56016;CHIMAY;2;Wallonie
6460;Chimay;56016;CHIMAY;2;Wallonie
6460;Robechies;56016;CHIMAY;2;Wallonie
6460;Saint-Remy (Ht.);56016;CHIMAY;2;Wallonie
6460;Salles;56016;CHIMAY;2;Wallonie
6460;Villers-la-Tour;56016;CHIMAY;2;Wallonie
6461;Virelles;56016;CHIMAY;2;Wallonie
6462;Vaulx-lez-Chimay;56016;CHIMAY;2;Wallonie
6463;Lompret;56016;CHIMAY;2;Wallonie
6464;Baileux;56016;CHIMAY;2;Wallonie
6464;Bourlers;56016;CHIMAY;2;Wallonie
6464;Forges;56016;CHIMAY;2;Wallonie
6464;l'Escaillčre;56016;CHIMAY;2;Wallonie
6464;Ričzes;56016;CHIMAY;2;Wallonie
6470;Grandrieu;56088;SIVRY-RANCE;2;Wallonie
6470;Montbliart;56088;SIVRY-RANCE;2;Wallonie
6470;Rance;56088;SIVRY-RANCE;2;Wallonie
6470;Sautin;56088;SIVRY-RANCE;2;Wallonie
6470;Sivry;56088;SIVRY-RANCE;2;Wallonie
6470;Sivry-Rance;56088;SIVRY-RANCE;2;Wallonie
6500;Barbenēon;56005;BEAUMONT;2;Wallonie
6500;Beaumont;56005;BEAUMONT;2;Wallonie
6500;Leugnies;56005;BEAUMONT;2;Wallonie
6500;Leval-Chaudeville;56005;BEAUMONT;2;Wallonie
6500;Renlies;56005;BEAUMONT;2;Wallonie
6500;Solre-Saint-Géry;56005;BEAUMONT;2;Wallonie
6500;Thirimont;56005;BEAUMONT;2;Wallonie
6511;Strée (Ht.);56005;BEAUMONT;2;Wallonie
6530;Leers-et-Fosteau;56078;THUIN;2;Wallonie
6530;Thuin;56078;THUIN;2;Wallonie
6531;Biesme-sous-Thuin;56078;THUIN;2;Wallonie
6532;Ragnies;56078;THUIN;2;Wallonie
6533;Biercée;56078;THUIN;2;Wallonie
6534;Gozée;56078;THUIN;2;Wallonie
6536;Donstiennes;56078;THUIN;2;Wallonie
6536;Thuillies;56078;THUIN;2;Wallonie
6540;Lobbes;56044;LOBBES;2;Wallonie
6540;Mont-Sainte-Genevičve;56044;LOBBES;2;Wallonie
6542;Sars-la-Buissičre;56044;LOBBES;2;Wallonie
6543;Bienne-lez-Happart;56044;LOBBES;2;Wallonie
6560;Bersillies-l'Abbaye;56022;ERQUELINNES;2;Wallonie
6560;Erquelinnes;56022;ERQUELINNES;2;Wallonie
6560;Grand-Reng;56022;ERQUELINNES;2;Wallonie
6560;Hantes-Wihéries;56022;ERQUELINNES;2;Wallonie
6560;Montignies-Saint-Christophe;56022;ERQUELINNES;2;Wallonie
6560;Solre-sur-Sambre;56022;ERQUELINNES;2;Wallonie
6567;Fontaine-Valmont;56049;MERBES-LE-CHATEAU;2;Wallonie
6567;Labuissičre;56049;MERBES-LE-CHATEAU;2;Wallonie
6567;Merbes-le-Chāteau;56049;MERBES-LE-CHATEAU;2;Wallonie
6567;Merbes-Sainte-Marie;56049;MERBES-LE-CHATEAU;2;Wallonie
6590;Momignies;56051;MOMIGNIES;2;Wallonie
6591;Macon;56051;MOMIGNIES;2;Wallonie
6592;Monceau-Imbrechies;56051;MOMIGNIES;2;Wallonie
6593;Macquenoise;56051;MOMIGNIES;2;Wallonie
6594;Beauwelz;56051;MOMIGNIES;2;Wallonie
6596;Forge-Philippe;56051;MOMIGNIES;2;Wallonie
6596;Seloignes;56051;MOMIGNIES;2;Wallonie
6600;Bastogne;82003;BASTOGNE;2;Wallonie
6600;Longvilly;82003;BASTOGNE;2;Wallonie
6600;Noville (Lux.);82003;BASTOGNE;2;Wallonie
6600;Villers-la-Bonne-Eau;82003;BASTOGNE;2;Wallonie
6600;Wardin;82003;BASTOGNE;2;Wallonie
6630;Martelange;81013;MARTELANGE;2;Wallonie
6637;Fauvillers;82009;FAUVILLERS;2;Wallonie
6637;Hollange;82009;FAUVILLERS;2;Wallonie
6637;Tintange;82009;FAUVILLERS;2;Wallonie
6640;Hompré;82036;VAUX-SUR-SURE;2;Wallonie
6640;Morhet;82036;VAUX-SUR-SURE;2;Wallonie
6640;Nives;82036;VAUX-SUR-SURE;2;Wallonie
6640;Sibret;82036;VAUX-SUR-SURE;2;Wallonie
6640;Vaux-lez-Rosičres;82036;VAUX-SUR-SURE;2;Wallonie
6640;Vaux-sur-Sure;82036;VAUX-SUR-SURE;2;Wallonie
6642;Juseret;82036;VAUX-SUR-SURE;2;Wallonie
6660;Houffalize;82014;HOUFFALIZE;2;Wallonie
6660;Nadrin;82014;HOUFFALIZE;2;Wallonie
6661;Mont (Lux.);82014;HOUFFALIZE;2;Wallonie
6661;Tailles;82014;HOUFFALIZE;2;Wallonie
6662;Tavigny;82014;HOUFFALIZE;2;Wallonie
6663;Mabompré;82014;HOUFFALIZE;2;Wallonie
6666;Wibrin;82014;HOUFFALIZE;2;Wallonie
6670;Gouvy;82037;GOUVY;2;Wallonie
6670;Limerlé;82037;GOUVY;2;Wallonie
6671;Bovigny;82037;GOUVY;2;Wallonie
6672;Beho;82037;GOUVY;2;Wallonie
6673;Cherain;82037;GOUVY;2;Wallonie
6674;Montleban;82037;GOUVY;2;Wallonie
6680;Amberloup;82038;SAINTE-ODE;2;Wallonie
6680;Sainte-Ode;82038;SAINTE-ODE;2;Wallonie
6680;Tillet;82038;SAINTE-ODE;2;Wallonie
6681;Lavacherie;82038;SAINTE-ODE;2;Wallonie
6686;Flamierge;82005;BERTOGNE;2;Wallonie
6687;Bertogne;82005;BERTOGNE;2;Wallonie
6688;Longchamps (Lux.);82005;BERTOGNE;2;Wallonie
6690;Bihain;82032;VIELSALM;2;Wallonie
6690;Vielsalm;82032;VIELSALM;2;Wallonie
6692;Petit-Thier;82032;VIELSALM;2;Wallonie
6698;Grand-Halleux;82032;VIELSALM;2;Wallonie
6700;Arlon;81001;ARLON;2;Wallonie
6700;Bonnert;81001;ARLON;2;Wallonie
6700;Heinsch;81001;ARLON;2;Wallonie
6700;Toernich;81001;ARLON;2;Wallonie
6704;Guirsch;81001;ARLON;2;Wallonie
6706;Autelbas;81001;ARLON;2;Wallonie
6717;Attert;81003;ATTERT;2;Wallonie
6717;Nobressart;81003;ATTERT;2;Wallonie
6717;Nothomb;81003;ATTERT;2;Wallonie
6717;Thiaumont;81003;ATTERT;2;Wallonie
6717;Tontelange;81003;ATTERT;2;Wallonie
6720;Habay;85046;HABAY;2;Wallonie
6720;Habay-la-Neuve;85046;HABAY;2;Wallonie
6720;Hachy;85046;HABAY;2;Wallonie
6721;Anlier;85046;HABAY;2;Wallonie
6723;Habay-la-Vieille;85046;HABAY;2;Wallonie
6724;Houdemont;85046;HABAY;2;Wallonie
6724;Marbehan;85046;HABAY;2;Wallonie
6724;Rulles;85046;HABAY;2;Wallonie
6730;Bellefontaine (Lux.);85039;TINTIGNY;2;Wallonie
6730;Rossignol;85039;TINTIGNY;2;Wallonie
6730;Saint-Vincent;85039;TINTIGNY;2;Wallonie
6730;Tintigny;85039;TINTIGNY;2;Wallonie
6740;Etalle;85009;ETALLE;2;Wallonie
6740;Sainte-Marie-sur-Semois;85009;ETALLE;2;Wallonie
6740;Villers-sur-Semois;85009;ETALLE;2;Wallonie
6741;Vance;85009;ETALLE;2;Wallonie
6742;Chantemelle;85009;ETALLE;2;Wallonie
6743;Buzenol;85009;ETALLE;2;Wallonie
6747;Chātillon;85034;SAINT-LEGER;2;Wallonie
6747;Meix-le-Tige;85034;SAINT-LEGER;2;Wallonie
6747;Saint-Léger (Lux.);85034;SAINT-LEGER;2;Wallonie
6750;Musson;85026;MUSSON;2;Wallonie
6750;Mussy-la-Ville;85026;MUSSON;2;Wallonie
6750;Signeulx;85026;MUSSON;2;Wallonie
6760;Bleid;85045;VIRTON;2;Wallonie
6760;Ethe;85045;VIRTON;2;Wallonie
6760;Ruette;85045;VIRTON;2;Wallonie
6760;Virton;85045;VIRTON;2;Wallonie
6761;Latour;85045;VIRTON;2;Wallonie
6762;Saint-Mard;85045;VIRTON;2;Wallonie
6767;Dampicourt;85047;ROUVROY;2;Wallonie
6767;Harnoncourt;85047;ROUVROY;2;Wallonie
6767;Lamorteau;85047;ROUVROY;2;Wallonie
6767;Rouvroy;85047;ROUVROY;2;Wallonie
6767;Torgny;85047;ROUVROY;2;Wallonie
6769;Gérouville;85024;MEIX-DEVANT-VIRTON;2;Wallonie
6769;Meix-Devant-Virton;85024;MEIX-DEVANT-VIRTON;2;Wallonie
6769;Robelmont;85024;MEIX-DEVANT-VIRTON;2;Wallonie
6769;Sommethonne;85024;MEIX-DEVANT-VIRTON;2;Wallonie
6769;Villers-la-Loue;85024;MEIX-DEVANT-VIRTON;2;Wallonie
6780;Hondelange;81015;MESSANCY;2;Wallonie
6780;Messancy;81015;MESSANCY;2;Wallonie
6780;Wolkrange;81015;MESSANCY;2;Wallonie
6781;Sélange;81015;MESSANCY;2;Wallonie
6782;Habergy;81015;MESSANCY;2;Wallonie
6790;Aubange;81004;AUBANGE;2;Wallonie
6791;Athus;81004;AUBANGE;2;Wallonie
6792;Halanzy;81004;AUBANGE;2;Wallonie
6792;Rachecourt;81004;AUBANGE;2;Wallonie
6800;Bras;84077;LIBRAMONT-CHEVIGNY;2;Wallonie
6800;Freux;84077;LIBRAMONT-CHEVIGNY;2;Wallonie
6800;Libramont-Chevigny;84077;LIBRAMONT-CHEVIGNY;2;Wallonie
6800;Moircy;84077;LIBRAMONT-CHEVIGNY;2;Wallonie
6800;Recogne;84077;LIBRAMONT-CHEVIGNY;2;Wallonie
6800;Remagne;84077;LIBRAMONT-CHEVIGNY;2;Wallonie
6800;Sainte-Marie-Chevigny;84077;LIBRAMONT-CHEVIGNY;2;Wallonie
6800;Saint-Pierre;84077;LIBRAMONT-CHEVIGNY;2;Wallonie
6810;Chiny;85007;CHINY;2;Wallonie
6810;Izel;85007;CHINY;2;Wallonie
6810;Jamoigne;85007;CHINY;2;Wallonie
6811;Les Bulles;85007;CHINY;2;Wallonie
6812;Suxy;85007;CHINY;2;Wallonie
6813;Termes;85007;CHINY;2;Wallonie
6820;Florenville;85011;FLORENVILLE;2;Wallonie
6820;Fontenoille;85011;FLORENVILLE;2;Wallonie
6820;Muno;85011;FLORENVILLE;2;Wallonie
6820;Sainte-Cécile;85011;FLORENVILLE;2;Wallonie
6821;Lacuisine;85011;FLORENVILLE;2;Wallonie
6823;Villers-Devant-Orval;85011;FLORENVILLE;2;Wallonie
6824;Chassepierre;85011;FLORENVILLE;2;Wallonie
6830;Bouillon;84010;BOUILLON;2;Wallonie
6830;Les Hayons;84010;BOUILLON;2;Wallonie
6830;Poupehan;84010;BOUILLON;2;Wallonie
6830;Rochehaut;84010;BOUILLON;2;Wallonie
6831;Noirefontaine;84010;BOUILLON;2;Wallonie
6832;Sensenruth;84010;BOUILLON;2;Wallonie
6833;Ucimont;84010;BOUILLON;2;Wallonie
6833;Vivy;84010;BOUILLON;2;Wallonie
6834;Bellevaux;84010;BOUILLON;2;Wallonie
6836;Dohan;84010;BOUILLON;2;Wallonie
6838;Corbion;84010;BOUILLON;2;Wallonie
6840;Grandvoir;84043;NEUFCHATEAU;2;Wallonie
6840;Grapfontaine;84043;NEUFCHATEAU;2;Wallonie
6840;Hamipré;84043;NEUFCHATEAU;2;Wallonie
6840;Longlier;84043;NEUFCHATEAU;2;Wallonie
6840;Neufchāteau;84043;NEUFCHATEAU;2;Wallonie
6840;Tournay;84043;NEUFCHATEAU;2;Wallonie
6850;Carlsbourg;84050;PALISEUL;2;Wallonie
6850;Offagne;84050;PALISEUL;2;Wallonie
6850;Paliseul;84050;PALISEUL;2;Wallonie
6851;Nollevaux;84050;PALISEUL;2;Wallonie
6852;Maissin;84050;PALISEUL;2;Wallonie
6852;Opont;84050;PALISEUL;2;Wallonie
6853;Framont;84050;PALISEUL;2;Wallonie
6856;Fays-les-Veneurs;84050;PALISEUL;2;Wallonie
6860;Assenois;84033;LEGLISE;2;Wallonie
6860;Ebly;84033;LEGLISE;2;Wallonie
6860;Léglise;84033;LEGLISE;2;Wallonie
6860;Mellier;84033;LEGLISE;2;Wallonie
6860;Witry;84033;LEGLISE;2;Wallonie
6870;Arville;84059;SAINT-HUBERT;2;Wallonie
6870;Awenne;84059;SAINT-HUBERT;2;Wallonie
6870;Hatrival;84059;SAINT-HUBERT;2;Wallonie
6870;Mirwart;84059;SAINT-HUBERT;2;Wallonie
6870;Saint-Hubert;84059;SAINT-HUBERT;2;Wallonie
6870;Vesqueville;84059;SAINT-HUBERT;2;Wallonie
6880;Auby-sur-Semois;84009;BERTRIX;2;Wallonie
6880;Bertrix;84009;BERTRIX;2;Wallonie
6880;Cugnon;84009;BERTRIX;2;Wallonie
6880;Jehonville;84009;BERTRIX;2;Wallonie
6880;Orgeo;84009;BERTRIX;2;Wallonie
6887;Herbeumont;84029;HERBEUMONT;2;Wallonie
6887;Saint-Médard;84029;HERBEUMONT;2;Wallonie
6887;Straimont;84029;HERBEUMONT;2;Wallonie
6890;Anloy;84035;LIBIN;2;Wallonie
6890;Libin;84035;LIBIN;2;Wallonie
6890;Ochamps;84035;LIBIN;2;Wallonie
6890;Redu;84035;LIBIN;2;Wallonie
6890;Smuid;84035;LIBIN;2;Wallonie
6890;Transinne;84035;LIBIN;2;Wallonie
6890;Villance;84035;LIBIN;2;Wallonie
6900;Aye;83034;MARCHE-EN-FAMENNE;2;Wallonie
6900;Hargimont;83034;MARCHE-EN-FAMENNE;2;Wallonie
6900;Humain;83034;MARCHE-EN-FAMENNE;2;Wallonie
6900;Marche-en-Famenne;83034;MARCHE-EN-FAMENNE;2;Wallonie
6900;On;83034;MARCHE-EN-FAMENNE;2;Wallonie
6900;Roy;83034;MARCHE-EN-FAMENNE;2;Wallonie
6900;Waha;83034;MARCHE-EN-FAMENNE;2;Wallonie
6920;Sohier;84075;WELLIN;2;Wallonie
6920;Wellin;84075;WELLIN;2;Wallonie
6921;Chanly;84075;WELLIN;2;Wallonie
6922;Halma;84075;WELLIN;2;Wallonie
6924;Lomprez;84075;WELLIN;2;Wallonie
6927;Bure;84068;TELLIN;2;Wallonie
6927;Grupont;84068;TELLIN;2;Wallonie
6927;Resteigne;84068;TELLIN;2;Wallonie
6927;Tellin;84068;TELLIN;2;Wallonie
6929;Daverdisse;84016;DAVERDISSE;2;Wallonie
6929;Gembes;84016;DAVERDISSE;2;Wallonie
6929;Haut-Fays;84016;DAVERDISSE;2;Wallonie
6929;Porcheresse (Lux.);84016;DAVERDISSE;2;Wallonie
6940;Barvaux-sur-Ourthe;83012;DURBUY;2;Wallonie
6940;Durbuy;83012;DURBUY;2;Wallonie
6940;Grandhan;83012;DURBUY;2;Wallonie
6940;Septon;83012;DURBUY;2;Wallonie
6940;Wéris;83012;DURBUY;2;Wallonie
6941;Bende;83012;DURBUY;2;Wallonie
6941;Bomal-sur-Ourthe;83012;DURBUY;2;Wallonie
6941;Borlon;83012;DURBUY;2;Wallonie
6941;Heyd;83012;DURBUY;2;Wallonie
6941;Izier;83012;DURBUY;2;Wallonie
6941;Tohogne;83012;DURBUY;2;Wallonie
6941;Villers-Sainte-Gertrude;83012;DURBUY;2;Wallonie
6950;Harsin;83040;NASSOGNE;2;Wallonie
6950;Nassogne;83040;NASSOGNE;2;Wallonie
6951;Bande;83040;NASSOGNE;2;Wallonie
6952;Grune;83040;NASSOGNE;2;Wallonie
6953;Ambly;83040;NASSOGNE;2;Wallonie
6953;Forričres;83040;NASSOGNE;2;Wallonie
6953;Lesterny;83040;NASSOGNE;2;Wallonie
6953;Masbourg;83040;NASSOGNE;2;Wallonie
6960;Dochamps;83055;MANHAY;2;Wallonie
6960;Grandmenil;83055;MANHAY;2;Wallonie
6960;Harre;83055;MANHAY;2;Wallonie
6960;Malempré;83055;MANHAY;2;Wallonie
6960;Manhay;83055;MANHAY;2;Wallonie
6960;Odeigne;83055;MANHAY;2;Wallonie
6960;Vaux-Chavanne;83055;MANHAY;2;Wallonie
6970;Tenneville;83049;TENNEVILLE;2;Wallonie
6971;Champlon;83049;TENNEVILLE;2;Wallonie
6972;Erneuville;83049;TENNEVILLE;2;Wallonie
6980;Beausaint;83031;LA-ROCHE-EN-ARDENNE;2;Wallonie
6980;La Roche-en-Ardenne;83031;LA-ROCHE-EN-ARDENNE;2;Wallonie
6982;Samrée;83031;LA-ROCHE-EN-ARDENNE;2;Wallonie
6983;Ortho;83031;LA-ROCHE-EN-ARDENNE;2;Wallonie
6984;Hives;83031;LA-ROCHE-EN-ARDENNE;2;Wallonie
6986;Halleux;83031;LA-ROCHE-EN-ARDENNE;2;Wallonie
6987;Beffe;83044;RENDEUX;2;Wallonie
6987;Hodister;83044;RENDEUX;2;Wallonie
6987;Marcourt;83044;RENDEUX;2;Wallonie
6987;Rendeux;83044;RENDEUX;2;Wallonie
6990;Fronville;83028;HOTTON;2;Wallonie
6990;Hampteau;83028;HOTTON;2;Wallonie
6990;Hotton;83028;HOTTON;2;Wallonie
6990;Marenne;83028;HOTTON;2;Wallonie
6997;Amonines;83013;EREZEE;2;Wallonie
6997;Erezée;83013;EREZEE;2;Wallonie
6997;Mormont;83013;EREZEE;2;Wallonie
6997;Soy;83013;EREZEE;2;Wallonie
7000;Mons;53053;MONS;2;Wallonie
7010;S.H.A.P.E. Belgiė;53053;MONS;2;Wallonie
7010;S.H.A.P.E. Belgique;53053;MONS;2;Wallonie
7011;Ghlin;53053;MONS;2;Wallonie
7012;Flénu;53053;MONS;2;Wallonie
7012;Jemappes;53053;MONS;2;Wallonie
7020;Maisičres;53053;MONS;2;Wallonie
7020;Nimy;53053;MONS;2;Wallonie
7021;Havré;53053;MONS;2;Wallonie
7022;Harmignies;53053;MONS;2;Wallonie
7022;Harveng;53053;MONS;2;Wallonie
7022;Hyon;53053;MONS;2;Wallonie
7022;Mesvin;53053;MONS;2;Wallonie
7022;Nouvelles;53053;MONS;2;Wallonie
7024;Ciply;53053;MONS;2;Wallonie
7030;Saint-Symphorien;53053;MONS;2;Wallonie
7031;Villers-Saint-Ghislain;53053;MONS;2;Wallonie
7032;Spiennes;53053;MONS;2;Wallonie
7033;Cuesmes;53053;MONS;2;Wallonie
7034;Obourg;53053;MONS;2;Wallonie
7034;Saint-Denis (Ht.);53053;MONS;2;Wallonie
7040;Asquillies;53084;QUEVY;2;Wallonie
7040;Aulnois;53084;QUEVY;2;Wallonie
7040;Blaregnies;53084;QUEVY;2;Wallonie
7040;Bougnies;53084;QUEVY;2;Wallonie
7040;Genly;53084;QUEVY;2;Wallonie
7040;Goegnies-Chaussée;53084;QUEVY;2;Wallonie
7040;Quévy;53084;QUEVY;2;Wallonie
7040;Quévy-le-Grand;53084;QUEVY;2;Wallonie
7040;Quévy-le-Petit;53084;QUEVY;2;Wallonie
7041;Givry;53084;QUEVY;2;Wallonie
7041;Havay;53084;QUEVY;2;Wallonie
7050;Erbaut;53044;JURBISE;2;Wallonie
7050;Erbisoeul;53044;JURBISE;2;Wallonie
7050;Herchies;53044;JURBISE;2;Wallonie
7050;Jurbise;53044;JURBISE;2;Wallonie
7050;Masnuy-Saint-Jean (Jurbise);53044;JURBISE;2;Wallonie
7050;Masnuy-Saint-Pierre;53044;JURBISE;2;Wallonie
7060;Horrues;55040;SOIGNIES;2;Wallonie
7060;Soignies;55040;SOIGNIES;2;Wallonie
7061;Casteau (Soignies);55040;SOIGNIES;2;Wallonie
7061;Thieusies;55040;SOIGNIES;2;Wallonie
7062;Naast;55040;SOIGNIES;2;Wallonie
7063;Chaussée-Notre-Dame-Louvignies;55040;SOIGNIES;2;Wallonie
7063;Neufvilles;55040;SOIGNIES;2;Wallonie
7070;Gottignies;55035;LE ROEULX;2;Wallonie
7070;Le Roeulx;55035;LE ROEULX;2;Wallonie
7070;Mignault;55035;LE ROEULX;2;Wallonie
7070;Thieu;55035;LE ROEULX;2;Wallonie
7070;Ville-sur-Haine (Le Roeulx);55035;LE ROEULX;2;Wallonie
7080;Eugies (Frameries);53028;FRAMERIES;2;Wallonie
7080;Frameries;53028;FRAMERIES;2;Wallonie
7080;La Bouverie;53028;FRAMERIES;2;Wallonie
7080;Noirchain;53028;FRAMERIES;2;Wallonie
7080;Sars-la-Bruyčre;53028;FRAMERIES;2;Wallonie
7090;Braine-le-Comte;55004;BRAINE-LE-COMTE;2;Wallonie
7090;Hennuyčres;55004;BRAINE-LE-COMTE;2;Wallonie
7090;Henripont;55004;BRAINE-LE-COMTE;2;Wallonie
7090;Petit-Roeulx-lez-Braine;55004;BRAINE-LE-COMTE;2;Wallonie
7090;Ronquičres;55004;BRAINE-LE-COMTE;2;Wallonie
7090;Steenkerque (Ht.);55004;BRAINE-LE-COMTE;2;Wallonie
7100;Haine-Saint-Paul;55022;LA LOUVIERE;2;Wallonie
7100;Haine-Saint-Pierre;55022;LA LOUVIERE;2;Wallonie
7100;La Louvičre;55022;LA LOUVIERE;2;Wallonie
7100;Saint-Vaast;55022;LA LOUVIERE;2;Wallonie
7100;Trivičres;55022;LA LOUVIERE;2;Wallonie
7110;Boussoit;55022;LA LOUVIERE;2;Wallonie
7110;Houdeng-Aimeries;55022;LA LOUVIERE;2;Wallonie
7110;Houdeng-Goegnies (La Louvičre);55022;LA LOUVIERE;2;Wallonie
7110;Maurage;55022;LA LOUVIERE;2;Wallonie
7110;Strépy-Bracquegnies;55022;LA LOUVIERE;2;Wallonie
7120;Croix-lez-Rouveroy;56085;ESTINNES;2;Wallonie
7120;Estinnes;56085;ESTINNES;2;Wallonie
7120;Estinnes-au-Mont;56085;ESTINNES;2;Wallonie
7120;Estinnes-au-Val;56085;ESTINNES;2;Wallonie
7120;Fauroeulx;56085;ESTINNES;2;Wallonie
7120;Haulchin;56085;ESTINNES;2;Wallonie
7120;Peissant;56085;ESTINNES;2;Wallonie
7120;Rouveroy (Ht.);56085;ESTINNES;2;Wallonie
7120;Vellereille-les-Brayeux;56085;ESTINNES;2;Wallonie
7120;Vellereille-le-Sec;56085;ESTINNES;2;Wallonie
7130;Battignies;56011;BINCHE;2;Wallonie
7130;Binche;56011;BINCHE;2;Wallonie
7130;Bray;56011;BINCHE;2;Wallonie
7131;Waudrez;56011;BINCHE;2;Wallonie
7133;Buvrinnes;56011;BINCHE;2;Wallonie
7134;Epinois;56011;BINCHE;2;Wallonie
7134;Leval-Trahegnies;56011;BINCHE;2;Wallonie
7134;Péronnes-lez-Binche;56011;BINCHE;2;Wallonie
7134;Ressaix;56011;BINCHE;2;Wallonie
7140;Morlanwelz;56087;MORLANWELZ;2;Wallonie
7140;Morlanwelz-Mariemont;56087;MORLANWELZ;2;Wallonie
7141;Carničres;56087;MORLANWELZ;2;Wallonie
7141;Mont-Sainte-Aldegonde;56087;MORLANWELZ;2;Wallonie
7160;Chapelle-lez-Herlaimont;52010;CHAPELLE-LEZ-HERLAIMONT;2;Wallonie
7160;Godarville;52010;CHAPELLE-LEZ-HERLAIMONT;2;Wallonie
7160;Piéton;52010;CHAPELLE-LEZ-HERLAIMONT;2;Wallonie
7170;Bellecourt;52043;MANAGE;2;Wallonie
7170;Bois-d'Haine;52043;MANAGE;2;Wallonie
7170;Fayt-lez-Manage;52043;MANAGE;2;Wallonie
7170;La Hestre;52043;MANAGE;2;Wallonie
7170;Manage;52043;MANAGE;2;Wallonie
7180;Seneffe;52063;SENEFFE;2;Wallonie
7181;Arquennes;52063;SENEFFE;2;Wallonie
7181;Familleureux;52063;SENEFFE;2;Wallonie
7181;Feluy;52063;SENEFFE;2;Wallonie
7181;Petit-Roeulx-lez-Nivelles;52063;SENEFFE;2;Wallonie
7190;Ecaussinnes;55050;ECAUSSINES;2;Wallonie
7190;Ecaussinnes-d'Enghien;55050;ECAUSSINES;2;Wallonie
7190;Marche-lez-Ecaussinnes;55050;ECAUSSINES;2;Wallonie
7191;Ecaussinnes-Lalaing;55050;ECAUSSINES;2;Wallonie
7300;Boussu;53014;BOUSSU;2;Wallonie
7301;Hornu;53014;BOUSSU;2;Wallonie
7320;Bernissart;51009;BERNISSART;2;Wallonie
7321;Blaton;51009;BERNISSART;2;Wallonie
7321;Harchies;51009;BERNISSART;2;Wallonie
7322;Pommeroeul;51009;BERNISSART;2;Wallonie
7322;Ville-Pommeroeul;51009;BERNISSART;2;Wallonie
7330;Saint-Ghislain;53070;SAINT-GHISLAIN;2;Wallonie
7331;Baudour;53070;SAINT-GHISLAIN;2;Wallonie
7332;Neufmaison;53070;SAINT-GHISLAIN;2;Wallonie
7332;Sirault;53070;SAINT-GHISLAIN;2;Wallonie
7333;Tertre;53070;SAINT-GHISLAIN;2;Wallonie
7334;Hautrage;53070;SAINT-GHISLAIN;2;Wallonie
7334;Villerot;53070;SAINT-GHISLAIN;2;Wallonie
7340;Colfontaine;53082;COLFONTAINE;2;Wallonie
7340;Paturages;53082;COLFONTAINE;2;Wallonie
7340;Warquignies;53082;COLFONTAINE;2;Wallonie
7340;Wasmes;53082;COLFONTAINE;2;Wallonie
7350;Hainin;53039;HENSIES;2;Wallonie
7350;Hensies;53039;HENSIES;2;Wallonie
7350;Montroeul-sur-Haine;53039;HENSIES;2;Wallonie
7350;Thulin;53039;HENSIES;2;Wallonie
7370;Blaugies;53020;DOUR;2;Wallonie
7370;Dour;53020;DOUR;2;Wallonie
7370;Elouges;53020;DOUR;2;Wallonie
7370;Wihéries;53020;DOUR;2;Wallonie
7380;Baisieux;53068;QUIEVRAIN;2;Wallonie
7380;Quiévrain;53068;QUIEVRAIN;2;Wallonie
7382;Audregnies;53068;QUIEVRAIN;2;Wallonie
7387;Angre;53083;HONNELLES;2;Wallonie
7387;Angreau;53083;HONNELLES;2;Wallonie
7387;Athis;53083;HONNELLES;2;Wallonie
7387;Autreppe;53083;HONNELLES;2;Wallonie
7387;Erquennes;53083;HONNELLES;2;Wallonie
7387;Fayt-le-Franc;53083;HONNELLES;2;Wallonie
7387;Honnelles;53083;HONNELLES;2;Wallonie
7387;Marchipont;53083;HONNELLES;2;Wallonie
7387;Montignies-sur-Roc;53083;HONNELLES;2;Wallonie
7387;Onnezies;53083;HONNELLES;2;Wallonie
7387;Roisin;53083;HONNELLES;2;Wallonie
7390;Quaregnon;53065;QUAREGNON;2;Wallonie
7390;Wasmuel;53065;QUAREGNON;2;Wallonie
7500;Ere;57081;TOURNAI;2;Wallonie
7500;Saint-Maur;57081;TOURNAI;2;Wallonie
7500;Tournai;57081;TOURNAI;2;Wallonie
7501;Orcq;57081;TOURNAI;2;Wallonie
7502;Esplechin;57081;TOURNAI;2;Wallonie
7503;Froyennes;57081;TOURNAI;2;Wallonie
7504;Froidmont;57081;TOURNAI;2;Wallonie
7506;Willemeau;57081;TOURNAI;2;Wallonie
7520;Ramegnies-Chin;57081;TOURNAI;2;Wallonie
7520;Templeuve;57081;TOURNAI;2;Wallonie
7521;Chercq;57081;TOURNAI;2;Wallonie
7522;Blandain;57081;TOURNAI;2;Wallonie
7522;Hertain;57081;TOURNAI;2;Wallonie
7522;Lamain;57081;TOURNAI;2;Wallonie
7522;Marquain;57081;TOURNAI;2;Wallonie
7530;Gaurain-Ramecroix (Tournai);57081;TOURNAI;2;Wallonie
7531;Havinnes;57081;TOURNAI;2;Wallonie
7532;Beclers;57081;TOURNAI;2;Wallonie
7533;Thimougies;57081;TOURNAI;2;Wallonie
7534;Barry;57081;TOURNAI;2;Wallonie
7534;Maulde;57081;TOURNAI;2;Wallonie
7536;Vaulx (Tournai);57081;TOURNAI;2;Wallonie
7538;Vezon;57081;TOURNAI;2;Wallonie
7540;Kain;57081;TOURNAI;2;Wallonie
7540;Melles;57081;TOURNAI;2;Wallonie
7540;Quartes;57081;TOURNAI;2;Wallonie
7540;Rumillies;57081;TOURNAI;2;Wallonie
7542;Mont-Saint-Aubert;57081;TOURNAI;2;Wallonie
7543;Mourcourt;57081;TOURNAI;2;Wallonie
7548;Warchin;57081;TOURNAI;2;Wallonie
7600;Péruwelz;57064;PERUWELZ;2;Wallonie
7601;Roucourt;57064;PERUWELZ;2;Wallonie
7602;Bury;57064;PERUWELZ;2;Wallonie
7603;Bon-Secours;57064;PERUWELZ;2;Wallonie
7604;Baugnies;57064;PERUWELZ;2;Wallonie
7604;Braffe;57064;PERUWELZ;2;Wallonie
7604;Brasmenil;57064;PERUWELZ;2;Wallonie
7604;Callenelle;57064;PERUWELZ;2;Wallonie
7604;Wasmes-Audemez-Briffoeil;57064;PERUWELZ;2;Wallonie
7608;Wiers;57064;PERUWELZ;2;Wallonie
7610;Rumes;57072;RUMES;2;Wallonie
7611;La Glanerie;57072;RUMES;2;Wallonie
7618;Taintignies;57072;RUMES;2;Wallonie
7620;Bléharies;57093;BRUNEHAUT;2;Wallonie
7620;Brunehaut;57093;BRUNEHAUT;2;Wallonie
7620;Guignies;57093;BRUNEHAUT;2;Wallonie
7620;Hollain;57093;BRUNEHAUT;2;Wallonie
7620;Jollain-Merlin;57093;BRUNEHAUT;2;Wallonie
7620;Wez-Velvain;57093;BRUNEHAUT;2;Wallonie
7621;Lesdain;57093;BRUNEHAUT;2;Wallonie
7622;Laplaigne;57093;BRUNEHAUT;2;Wallonie
7623;Rongy;57093;BRUNEHAUT;2;Wallonie
7624;Howardries;57093;BRUNEHAUT;2;Wallonie
7640;Antoing;57003;ANTOING;2;Wallonie
7640;Maubray;57003;ANTOING;2;Wallonie
7640;Péronnes-lez-Antoing;57003;ANTOING;2;Wallonie
7641;Bruyelle;57003;ANTOING;2;Wallonie
7642;Calonne;57003;ANTOING;2;Wallonie
7643;Fontenoy;57003;ANTOING;2;Wallonie
7700;Luingne;54007;MOUSCRON;2;Wallonie
7700;Moeskroen;54007;MOUSCRON;2;Wallonie
7700;Mouscron;54007;MOUSCRON;2;Wallonie
7711;Dottenijs;54007;MOUSCRON;2;Wallonie
7711;Dottignies;54007;MOUSCRON;2;Wallonie
7712;Herseaux;54007;MOUSCRON;2;Wallonie
7730;Bailleul;57027;ESTAIMPUIS;2;Wallonie
7730;Estaimbourg;57027;ESTAIMPUIS;2;Wallonie
7730;Estaimpuis;57027;ESTAIMPUIS;2;Wallonie
7730;Evregnies;57027;ESTAIMPUIS;2;Wallonie
7730;Leers-Nord;57027;ESTAIMPUIS;2;Wallonie
7730;Néchin;57027;ESTAIMPUIS;2;Wallonie
7730;Saint-Léger (Ht.);57027;ESTAIMPUIS;2;Wallonie
7740;Pecq;57062;PECQ;2;Wallonie
7740;Warcoing;57062;PECQ;2;Wallonie
7742;Hérinnes-lez-Pecq;57062;PECQ;2;Wallonie
7743;Esquelmes;57062;PECQ;2;Wallonie
7743;Obigies;57062;PECQ;2;Wallonie
7750;Amougies;57095;MONT-DE-L ENCLUS;2;Wallonie
7750;Anseroeul;57095;MONT-DE-L ENCLUS;2;Wallonie
7750;Mont-de-l'Enclus;57095;MONT-DE-L ENCLUS;2;Wallonie
7750;Orroir;57095;MONT-DE-L ENCLUS;2;Wallonie
7750;Russeignies;57095;MONT-DE-L ENCLUS;2;Wallonie
7760;Celles (Ht.);57018;CELLES;2;Wallonie
7760;Escanaffles;57018;CELLES;2;Wallonie
7760;Molenbaix;57018;CELLES;2;Wallonie
7760;Popuelles;57018;CELLES;2;Wallonie
7760;Pottes;57018;CELLES;2;Wallonie
7760;Velaines;57018;CELLES;2;Wallonie
7780;Comines;54010;COMINES-WARNETON;2;Wallonie
7780;Comines-Warneton;54010;COMINES-WARNETON;2;Wallonie
7780;Komen;54010;COMINES-WARNETON;2;Wallonie
7780;Komen-Waasten;54010;COMINES-WARNETON;2;Wallonie
7781;Houthem (Comines);54010;COMINES-WARNETON;2;Wallonie
7782;Ploegsteert;54010;COMINES-WARNETON;2;Wallonie
7783;Bizet;54010;COMINES-WARNETON;2;Wallonie
7784;Bas-Warneton;54010;COMINES-WARNETON;2;Wallonie
7784;Neerwaasten;54010;COMINES-WARNETON;2;Wallonie
7784;Waasten;54010;COMINES-WARNETON;2;Wallonie
7784;Warneton;54010;COMINES-WARNETON;2;Wallonie
7800;Ath;51004;ATH;2;Wallonie
7800;Lanquesaint;51004;ATH;2;Wallonie
7801;Irchonwelz;51004;ATH;2;Wallonie
7802;Ormeignies;51004;ATH;2;Wallonie
7803;Bouvignies;51004;ATH;2;Wallonie
7804;Ostiches;51004;ATH;2;Wallonie
7804;Rebaix;51004;ATH;2;Wallonie
7810;Maffle;51004;ATH;2;Wallonie
7811;Arbre (Ht.);51004;ATH;2;Wallonie
7812;Houtaing;51004;ATH;2;Wallonie
7812;Ligne;51004;ATH;2;Wallonie
7812;Mainvault;51004;ATH;2;Wallonie
7812;Moulbaix;51004;ATH;2;Wallonie
7812;Villers-Notre-Dame;51004;ATH;2;Wallonie
7812;Villers-Saint-Amand;51004;ATH;2;Wallonie
7822;Ghislenghien;51004;ATH;2;Wallonie
7822;Isičres;51004;ATH;2;Wallonie
7822;Meslin-l'Evźque;51004;ATH;2;Wallonie
7823;Gibecq;51004;ATH;2;Wallonie
7830;Bassilly;55039;SILLY;2;Wallonie
7830;Fouleng;55039;SILLY;2;Wallonie
7830;Gondregnies;55039;SILLY;2;Wallonie
7830;Graty;55039;SILLY;2;Wallonie
7830;Hellebecq;55039;SILLY;2;Wallonie
7830;Hoves (Ht.);55039;SILLY;2;Wallonie
7830;Silly;55039;SILLY;2;Wallonie
7830;Thoricourt;55039;SILLY;2;Wallonie
7850;Edingen;55010;ENGHIEN;2;Wallonie
7850;Enghien;55010;ENGHIEN;2;Wallonie
7850;Lettelingen;55010;ENGHIEN;2;Wallonie
7850;Marcq;55010;ENGHIEN;2;Wallonie
7850;Mark;55010;ENGHIEN;2;Wallonie
7850;Petit-Enghien;55010;ENGHIEN;2;Wallonie
7860;Lessines;55023;LESSINES;2;Wallonie
7861;Papignies;55023;LESSINES;2;Wallonie
7861;Wannebecq;55023;LESSINES;2;Wallonie
7862;Ogy;55023;LESSINES;2;Wallonie
7863;Ghoy;55023;LESSINES;2;Wallonie
7864;Deux-Acren;55023;LESSINES;2;Wallonie
7866;Bois-de-Lessines;55023;LESSINES;2;Wallonie
7866;Ollignies;55023;LESSINES;2;Wallonie
7870;Bauffe;53046;LENS;2;Wallonie
7870;Cambron-Saint-Vincent;53046;LENS;2;Wallonie
7870;Lens;53046;LENS;2;Wallonie
7870;Lombise;53046;LENS;2;Wallonie
7870;Montignies-lez-Lens;53046;LENS;2;Wallonie
7880;Flobecq;51019;FLOBECQ;2;Wallonie
7880;Vloesberg;51019;FLOBECQ;2;Wallonie
7890;Ellezelles;51017;ELLEZELLES;2;Wallonie
7890;Lahamaide;51017;ELLEZELLES;2;Wallonie
7890;Wodecq;51017;ELLEZELLES;2;Wallonie
7900;Grandmetz;57094;LEUZE-EN-HAINAUT;2;Wallonie
7900;Leuze-en-Hainaut;57094;LEUZE-EN-HAINAUT;2;Wallonie
7901;Thieulain;57094;LEUZE-EN-HAINAUT;2;Wallonie
7903;Blicquy;57094;LEUZE-EN-HAINAUT;2;Wallonie
7903;Chapelle-ą-Oie;57094;LEUZE-EN-HAINAUT;2;Wallonie
7903;Chapelle-ą-Wattines;57094;LEUZE-EN-HAINAUT;2;Wallonie
7904;Pipaix;57094;LEUZE-EN-HAINAUT;2;Wallonie
7904;Tourpes;57094;LEUZE-EN-HAINAUT;2;Wallonie
7904;Willaupuis;57094;LEUZE-EN-HAINAUT;2;Wallonie
7906;Gallaix;57094;LEUZE-EN-HAINAUT;2;Wallonie
7910;Anvaing;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7910;Arc-Ainičres;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7910;Arc-Wattripont;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7910;Cordes;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7910;Ellignies-lez-Frasnes;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7910;Forest (Ht.);51065;FRASNES-LEZ-ANVAING;2;Wallonie
7910;Frasnes-lez-Anvaing;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7910;Wattripont;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7911;Buissenal;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7911;Frasnes-lez-Buissenal;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7911;Hacquegnies;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7911;Herquegies;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7911;Montroeul-au-Bois;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7911;Moustier (Ht.);51065;FRASNES-LEZ-ANVAING;2;Wallonie
7911;Oeudeghien;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7912;Dergneau;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7912;Saint-Sauveur;51065;FRASNES-LEZ-ANVAING;2;Wallonie
7940;Brugelette;51012;BRUGELETTE;2;Wallonie
7940;Cambron-Casteau;51012;BRUGELETTE;2;Wallonie
7941;Attre;51012;BRUGELETTE;2;Wallonie
7942;Mévergnies-lez-Lens;51012;BRUGELETTE;2;Wallonie
7943;Gages;51012;BRUGELETTE;2;Wallonie
7950;Chičvres;51014;CHIEVRES;2;Wallonie
7950;Grosage;51014;CHIEVRES;2;Wallonie
7950;Huissignies;51014;CHIEVRES;2;Wallonie
7950;Ladeuze;51014;CHIEVRES;2;Wallonie
7950;Tongre-Saint-Martin;51014;CHIEVRES;2;Wallonie
7951;Tongre-Notre-Dame;51014;CHIEVRES;2;Wallonie
7970;Beloeil;51008;BELOEIL;2;Wallonie
7971;Basčcles;51008;BELOEIL;2;Wallonie
7971;Ramegnies;51008;BELOEIL;2;Wallonie
7971;Thumaide;51008;BELOEIL;2;Wallonie
7971;Wadelincourt;51008;BELOEIL;2;Wallonie
7972;Aubechies;51008;BELOEIL;2;Wallonie
7972;Ellignies-Sainte-Anne;51008;BELOEIL;2;Wallonie
7972;Quevaucamps;51008;BELOEIL;2;Wallonie
7973;Grandglise;51008;BELOEIL;2;Wallonie
7973;Stambruges;51008;BELOEIL;2;Wallonie
8000;Brugge;31005;BRUGES;1;Flandre
8000;Koolkerke;31005;BRUGES;1;Flandre
8020;Hertsberge;31022;OOSTKAMP;1;Flandre
8020;Oostkamp;31022;OOSTKAMP;1;Flandre
8020;Ruddervoorde;31022;OOSTKAMP;1;Flandre
8020;Waardamme;31022;OOSTKAMP;1;Flandre
8200;Sint-Andries;31005;BRUGES;1;Flandre
8200;Sint-Michiels;31005;BRUGES;1;Flandre
8210;Loppem;31040;ZEDELGEM;1;Flandre
8210;Veldegem;31040;ZEDELGEM;1;Flandre
8210;Zedelgem;31040;ZEDELGEM;1;Flandre
8211;Aartrijke;31040;ZEDELGEM;1;Flandre
8300;Knokke;31043;KNOKKE-HEIST;1;Flandre
8300;Knokke-Heist;31043;KNOKKE-HEIST;1;Flandre
8300;Westkapelle;31043;KNOKKE-HEIST;1;Flandre
8301;Heist-aan-Zee;31043;KNOKKE-HEIST;1;Flandre
8301;Ramskapelle (Knokke-Heist);31043;KNOKKE-HEIST;1;Flandre
8310;Assebroek;31005;BRUGES;1;Flandre
8310;Sint-Kruis (Brugge);31005;BRUGES;1;Flandre
8340;Damme;31006;DAMME;1;Flandre
8340;Hoeke;31006;DAMME;1;Flandre
8340;Lapscheure;31006;DAMME;1;Flandre
8340;Moerkerke;31006;DAMME;1;Flandre
8340;Oostkerke (Damme);31006;DAMME;1;Flandre
8340;Sijsele;31006;DAMME;1;Flandre
8370;Blankenberge;31004;BLANKENBERGE;1;Flandre
8370;Uitkerke;31004;BLANKENBERGE;1;Flandre
8377;Houtave;31042;ZUIENKERKE;1;Flandre
8377;Meetkerke;31042;ZUIENKERKE;1;Flandre
8377;Nieuwmunster;31042;ZUIENKERKE;1;Flandre
8377;Zuienkerke;31042;ZUIENKERKE;1;Flandre
8380;Dudzele;31005;BRUGES;1;Flandre
8380;Lissewege;31005;BRUGES;1;Flandre
8380;Zeebrugge (Brugge);31005;BRUGES;1;Flandre
8400;Oostende;35013;OSTENDE;1;Flandre
8400;Stene;35013;OSTENDE;1;Flandre
8400;Zandvoorde (Oostende);35013;OSTENDE;1;Flandre
8420;De Haan;35029;DE HAAN;1;Flandre
8420;Klemskerke;35029;DE HAAN;1;Flandre
8420;Wenduine;35029;DE HAAN;1;Flandre
8421;Vlissegem;35029;DE HAAN;1;Flandre
8430;Middelkerke;35011;MIDDELKERKE;1;Flandre
8431;Wilskerke;35011;MIDDELKERKE;1;Flandre
8432;Leffinge;35011;MIDDELKERKE;1;Flandre
8433;Mannekensvere;35011;MIDDELKERKE;1;Flandre
8433;Schore;35011;MIDDELKERKE;1;Flandre
8433;Sint-Pieters-Kapelle (W.-Vl.);35011;MIDDELKERKE;1;Flandre
8433;Slijpe;35011;MIDDELKERKE;1;Flandre
8433;Spermalie;35011;MIDDELKERKE;1;Flandre
8434;Lombardsijde;35011;MIDDELKERKE;1;Flandre
8434;Westende;35011;MIDDELKERKE;1;Flandre
8450;Bredene;35002;BREDENE;1;Flandre
8460;Ettelgem;35014;OUDENBURG;1;Flandre
8460;Oudenburg;35014;OUDENBURG;1;Flandre
8460;Roksem;35014;OUDENBURG;1;Flandre
8460;Westkerke;35014;OUDENBURG;1;Flandre
8470;Gistel;35005;GISTEL;1;Flandre
8470;Moere;35005;GISTEL;1;Flandre
8470;Snaaskerke;35005;GISTEL;1;Flandre
8470;Zevekote;35005;GISTEL;1;Flandre
8480;Bekegem;35006;ICHTEGEM;1;Flandre
8480;Eernegem;35006;ICHTEGEM;1;Flandre
8480;Ichtegem;35006;ICHTEGEM;1;Flandre
8490;Jabbeke;31012;JABBEKE;1;Flandre
8490;Snellegem;31012;JABBEKE;1;Flandre
8490;Stalhille;31012;JABBEKE;1;Flandre
8490;Varsenare;31012;JABBEKE;1;Flandre
8490;Zerkegem;31012;JABBEKE;1;Flandre
8500;Kortrijk;34022;COURTRAI;1;Flandre
8501;Bissegem;34022;COURTRAI;1;Flandre
8501;Heule;34022;COURTRAI;1;Flandre
8510;Bellegem;34022;COURTRAI;1;Flandre
8510;Kooigem;34022;COURTRAI;1;Flandre
8510;Marke (Kortrijk);34022;COURTRAI;1;Flandre
8510;Rollegem;34022;COURTRAI;1;Flandre
8511;Aalbeke;34022;COURTRAI;1;Flandre
8520;Kuurne;34023;KUURNE;1;Flandre
8530;Harelbeke;34013;HARELBEKE;1;Flandre
8531;Bavikhove;34013;HARELBEKE;1;Flandre
8531;Hulste;34013;HARELBEKE;1;Flandre
8540;Deerlijk;34009;DEERLIJK;1;Flandre
8550;Zwevegem;34042;ZWEVEGEM;1;Flandre
8551;Heestert;34042;ZWEVEGEM;1;Flandre
8552;Moen;34042;ZWEVEGEM;1;Flandre
8553;Otegem;34042;ZWEVEGEM;1;Flandre
8554;Sint-Denijs;34042;ZWEVEGEM;1;Flandre
8560;Gullegem;34041;WEVELGEM;1;Flandre
8560;Moorsele;34041;WEVELGEM;1;Flandre
8560;Wevelgem;34041;WEVELGEM;1;Flandre
8570;Anzegem;34002;ANZEGEM;1;Flandre
8570;Gijzelbrechtegem;34002;ANZEGEM;1;Flandre
8570;Ingooigem;34002;ANZEGEM;1;Flandre
8570;Vichte;34002;ANZEGEM;1;Flandre
8572;Kaster;34002;ANZEGEM;1;Flandre
8573;Tiegem;34002;ANZEGEM;1;Flandre
8580;Avelgem;34003;AVELGEM;1;Flandre
8581;Kerkhove;34003;AVELGEM;1;Flandre
8581;Waarmaarde;34003;AVELGEM;1;Flandre
8582;Outrijve;34003;AVELGEM;1;Flandre
8583;Bossuit;34003;AVELGEM;1;Flandre
8587;Espierres;34043;ESPIERRES-HELCHIN;1;Flandre
8587;Espierres-Helchin;34043;ESPIERRES-HELCHIN;1;Flandre
8587;Helchin;34043;ESPIERRES-HELCHIN;1;Flandre
8587;Helkijn;34043;ESPIERRES-HELCHIN;1;Flandre
8587;Spiere;34043;ESPIERRES-HELCHIN;1;Flandre
8587;Spiere-Helkijn;34043;ESPIERRES-HELCHIN;1;Flandre
8600;Beerst;32003;DIXMUDE;1;Flandre
8600;Diksmuide;32003;DIXMUDE;1;Flandre
8600;Driekapellen;32003;DIXMUDE;1;Flandre
8600;Esen;32003;DIXMUDE;1;Flandre
8600;Kaaskerke;32003;DIXMUDE;1;Flandre
8600;Keiem;32003;DIXMUDE;1;Flandre
8600;Lampernisse;32003;DIXMUDE;1;Flandre
8600;Leke;32003;DIXMUDE;1;Flandre
8600;Nieuwkapelle;32003;DIXMUDE;1;Flandre
8600;Oostkerke (Diksmuide);32003;DIXMUDE;1;Flandre
8600;Oudekapelle;32003;DIXMUDE;1;Flandre
8600;Pervijze;32003;DIXMUDE;1;Flandre
8600;Sint-Jacobs-Kapelle;32003;DIXMUDE;1;Flandre
8600;Stuivekenskerke;32003;DIXMUDE;1;Flandre
8600;Vladslo;32003;DIXMUDE;1;Flandre
8600;Woumen;32003;DIXMUDE;1;Flandre
8610;Handzame;32011;KORTEMARK;1;Flandre
8610;Kortemark;32011;KORTEMARK;1;Flandre
8610;Werken;32011;KORTEMARK;1;Flandre
8610;Zarren;32011;KORTEMARK;1;Flandre
8620;Nieuwpoort;38016;NIEUPORT;1;Flandre
8620;Ramskapelle (Nieuwpoort);38016;NIEUPORT;1;Flandre
8620;Sint-Joris (Nieuwpoort);38016;NIEUPORT;1;Flandre
8630;Avekapelle;38025;FURNES;1;Flandre
8630;Beauvoorde;38025;FURNES;1;Flandre
8630;Booitshoeke;38025;FURNES;1;Flandre
8630;Bulskamp;38025;FURNES;1;Flandre
8630;De Moeren;38025;FURNES;1;Flandre
8630;Eggewaartskapelle;38025;FURNES;1;Flandre
8630;Houtem (W.-Vl.);38025;FURNES;1;Flandre
8630;Steenkerke (W.-Vl.);38025;FURNES;1;Flandre
8630;Veurne;38025;FURNES;1;Flandre
8630;Vinkem;38025;FURNES;1;Flandre
8630;Wulveringem;38025;FURNES;1;Flandre
8630;Zoutenaaie;38025;FURNES;1;Flandre
8640;Oostvleteren;33041;VLETEREN;1;Flandre
8640;Vleteren;33041;VLETEREN;1;Flandre
8640;Westvleteren;33041;VLETEREN;1;Flandre
8640;Woesten;33041;VLETEREN;1;Flandre
8647;Lo;32030;LO-RENINGE;1;Flandre
8647;Lo-Reninge;32030;LO-RENINGE;1;Flandre
8647;Noordschote;32030;LO-RENINGE;1;Flandre
8647;Pollinkhove;32030;LO-RENINGE;1;Flandre
8647;Reninge;32030;LO-RENINGE;1;Flandre
8650;Houthulst;32006;HOUTHULST;1;Flandre
8650;Klerken;32006;HOUTHULST;1;Flandre
8650;Merkem;32006;HOUTHULST;1;Flandre
8660;Adinkerke;38008;LA PANNE;1;Flandre
8660;De Panne;38008;LA PANNE;1;Flandre
8670;Koksijde;38014;KOKSIJDE;1;Flandre
8670;Oostduinkerke;38014;KOKSIJDE;1;Flandre
8670;Wulpen;38014;KOKSIJDE;1;Flandre
8680;Bovekerke;32010;KOEKELARE;1;Flandre
8680;Koekelare;32010;KOEKELARE;1;Flandre
8680;Zande;32010;KOEKELARE;1;Flandre
8690;Alveringem;38002;ALVERINGEM;1;Flandre
8690;Hoogstade;38002;ALVERINGEM;1;Flandre
8690;Oeren;38002;ALVERINGEM;1;Flandre
8690;Sint-Rijkers;38002;ALVERINGEM;1;Flandre
8691;Beveren-aan-den-Ijzer;38002;ALVERINGEM;1;Flandre
8691;Gijverinkhove;38002;ALVERINGEM;1;Flandre
8691;Izenberge;38002;ALVERINGEM;1;Flandre
8691;Leisele;38002;ALVERINGEM;1;Flandre
8691;Stavele;38002;ALVERINGEM;1;Flandre
8700;Aarsele;37015;TIELT;1;Flandre
8700;Kanegem;37015;TIELT;1;Flandre
8700;Schuiferskapelle;37015;TIELT;1;Flandre
8700;Tielt;37015;TIELT;1;Flandre
8710;Ooigem;37017;WIELSBEKE;1;Flandre
8710;Sint-Baafs-Vijve;37017;WIELSBEKE;1;Flandre
8710;Wielsbeke;37017;WIELSBEKE;1;Flandre
8720;Dentergem;37002;DENTERGEM;1;Flandre
8720;Markegem;37002;DENTERGEM;1;Flandre
8720;Oeselgem;37002;DENTERGEM;1;Flandre
8720;Wakken;37002;DENTERGEM;1;Flandre
8730;Beernem;31003;BEERNEM;1;Flandre
8730;Oedelem;31003;BEERNEM;1;Flandre
8730;Sint-Joris (Beernem);31003;BEERNEM;1;Flandre
8740;Egem;37011;PITTEM;1;Flandre
8740;Pittem;37011;PITTEM;1;Flandre
8750;Wingene;37018;WINGENE;1;Flandre
8750;Zwevezele;37018;WINGENE;1;Flandre
8755;Ruiselede;37012;RUISELEDE;1;Flandre
8760;Meulebeke;37007;MEULEBEKE;1;Flandre
8770;Ingelmunster;36007;INGELMUNSTER;1;Flandre
8780;Oostrozebeke;37010;OOSTROZEBEKE;1;Flandre
8790;Waregem;34040;WAREGEM;1;Flandre
8791;Beveren (Leie);34040;WAREGEM;1;Flandre
8792;Desselgem;34040;WAREGEM;1;Flandre
8793;Sint-Eloois-Vijve;34040;WAREGEM;1;Flandre
8800;Beveren (Roeselare);36015;ROULERS;1;Flandre
8800;Oekene;36015;ROULERS;1;Flandre
8800;Roeselare;36015;ROULERS;1;Flandre
8800;Rumbeke;36015;ROULERS;1;Flandre
8810;Lichtervelde;36011;LICHTERVELDE;1;Flandre
8820;Torhout;31033;TORHOUT;1;Flandre
8830;Gits;36006;HOOGLEDE;1;Flandre
8830;Hooglede;36006;HOOGLEDE;1;Flandre
8840;Oostnieuwkerke;36019;STADEN;1;Flandre
8840;Staden;36019;STADEN;1;Flandre
8840;Westrozebeke;36019;STADEN;1;Flandre
8850;Ardooie;37020;ARDOOIE;1;Flandre
8851;Koolskamp;37020;ARDOOIE;1;Flandre
8860;Lendelede;34025;LENDELEDE;1;Flandre
8870;Emelgem;36008;IZEGEM;1;Flandre
8870;Izegem;36008;IZEGEM;1;Flandre
8870;Kachtem;36008;IZEGEM;1;Flandre
8880;Ledegem;36010;LEDEGEM;1;Flandre
8880;Rollegem-Kapelle;36010;LEDEGEM;1;Flandre
8880;Sint-Eloois-Winkel;36010;LEDEGEM;1;Flandre
8890;Dadizele;36012;MOORSLEDE;1;Flandre
8890;Moorslede;36012;MOORSLEDE;1;Flandre
8900;Brielen;33011;YPRES;1;Flandre
8900;Dikkebus;33011;YPRES;1;Flandre
8900;Ieper;33011;YPRES;1;Flandre
8900;Sint-Jan;33011;YPRES;1;Flandre
8902;Hollebeke;33011;YPRES;1;Flandre
8902;Voormezele;33011;YPRES;1;Flandre
8902;Zillebeke;33011;YPRES;1;Flandre
8904;Boezinge;33011;YPRES;1;Flandre
8904;Zuidschote;33011;YPRES;1;Flandre
8906;Elverdinge;33011;YPRES;1;Flandre
8908;Vlamertinge;33011;YPRES;1;Flandre
8920;Bikschote;33040;LANGEMARK-POELKAPELLE;1;Flandre
8920;Langemark;33040;LANGEMARK-POELKAPELLE;1;Flandre
8920;Langemark-Poelkapelle;33040;LANGEMARK-POELKAPELLE;1;Flandre
8920;Poelkapelle;33040;LANGEMARK-POELKAPELLE;1;Flandre
8930;Lauwe;34027;MENIN;1;Flandre
8930;Menen;34027;MENIN;1;Flandre
8930;Rekkem;34027;MENIN;1;Flandre
8940;Geluwe;33029;WERVIK;1;Flandre
8940;Wervik;33029;WERVIK;1;Flandre
8950;Heuvelland;33039;HEUVELLAND;1;Flandre
8950;Nieuwkerke;33039;HEUVELLAND;1;Flandre
8951;Dranouter;33039;HEUVELLAND;1;Flandre
8952;Wulvergem;33039;HEUVELLAND;1;Flandre
8953;Wijtschate;33039;HEUVELLAND;1;Flandre
8954;Westouter;33039;HEUVELLAND;1;Flandre
8956;Kemmel;33039;HEUVELLAND;1;Flandre
8957;Mesen;33016;MESSINES;1;Flandre
8957;Messines;33016;MESSINES;1;Flandre
8958;Loker;33039;HEUVELLAND;1;Flandre
8970;Poperinge;33021;POPERINGE;1;Flandre
8970;Reningelst;33021;POPERINGE;1;Flandre
8972;Krombeke;33021;POPERINGE;1;Flandre
8972;Proven;33021;POPERINGE;1;Flandre
8972;Roesbrugge-Haringe;33021;POPERINGE;1;Flandre
8978;Watou;33021;POPERINGE;1;Flandre
8980;Beselare;33037;ZONNEBEKE;1;Flandre
8980;Geluveld;33037;ZONNEBEKE;1;Flandre
8980;Passendale;33037;ZONNEBEKE;1;Flandre
8980;Zandvoorde (Zonnebeke);33037;ZONNEBEKE;1;Flandre
8980;Zonnebeke;33037;ZONNEBEKE;1;Flandre
9000;Gent;44021;GAND;1;Flandre
9030;Mariakerke (Gent);44021;GAND;1;Flandre
9031;Drongen;44021;GAND;1;Flandre
9032;Wondelgem;44021;GAND;1;Flandre
9040;Sint-Amandsberg (Gent);44021;GAND;1;Flandre
9041;Oostakker;44021;GAND;1;Flandre
9042;Desteldonk;44021;GAND;1;Flandre
9042;Mendonk;44021;GAND;1;Flandre
9042;Sint-Kruis-Winkel;44021;GAND;1;Flandre
9050;Gentbrugge;44021;GAND;1;Flandre
9050;Ledeberg (Gent);44021;GAND;1;Flandre
9051;Afsnee;44021;GAND;1;Flandre
9051;Sint-Denijs-Westrem;44021;GAND;1;Flandre
9052;Zwijnaarde;44021;GAND;1;Flandre
9060;Zelzate;43018;ZELZATE;1;Flandre
9070;Destelbergen;44013;DESTELBERGEN;1;Flandre
9070;Heusden (O.-Vl.);44013;DESTELBERGEN;1;Flandre
9080;Beervelde;44034;LOCHRISTI;1;Flandre
9080;Lochristi;44034;LOCHRISTI;1;Flandre
9080;Zaffelare;44034;LOCHRISTI;1;Flandre
9080;Zeveneken;44034;LOCHRISTI;1;Flandre
9090;Gontrode;44040;MELLE;1;Flandre
9090;Melle;44040;MELLE;1;Flandre
9100;Nieuwkerken-Waas;46021;SAINT-NICOLAS;1;Flandre
9100;Sint-Niklaas;46021;SAINT-NICOLAS;1;Flandre
9111;Belsele (Sint-Niklaas);46021;SAINT-NICOLAS;1;Flandre
9112;Sinaai-Waas;46021;SAINT-NICOLAS;1;Flandre
9120;Beveren-Waas;46003;BEVEREN;1;Flandre
9120;Haasdonk;46003;BEVEREN;1;Flandre
9120;Kallo (Beveren-Waas);46003;BEVEREN;1;Flandre
9120;Melsele;46003;BEVEREN;1;Flandre
9120;Vrasene;46003;BEVEREN;1;Flandre
9130;Doel;46003;BEVEREN;1;Flandre
9130;Kallo (Kieldrecht);46003;BEVEREN;1;Flandre
9130;Kieldrecht (Beveren);46003;BEVEREN;1;Flandre
9130;Verrebroek;46003;BEVEREN;1;Flandre
9140;Elversele;46025;TAMISE;1;Flandre
9140;Steendorp;46025;TAMISE;1;Flandre
9140;Temse;46025;TAMISE;1;Flandre
9140;Tielrode;46025;TAMISE;1;Flandre
9150;Bazel;46013;KRUIBEKE;1;Flandre
9150;Kruibeke;46013;KRUIBEKE;1;Flandre
9150;Rupelmonde;46013;KRUIBEKE;1;Flandre
9160;Daknam;46014;LOKEREN;1;Flandre
9160;Eksaarde;46014;LOKEREN;1;Flandre
9160;Lokeren;46014;LOKEREN;1;Flandre
9170;De Klinge;46020;SINT-GILLIS-WAAS;1;Flandre
9170;Meerdonk;46020;SINT-GILLIS-WAAS;1;Flandre
9170;Sint-Gillis-Waas;46020;SINT-GILLIS-WAAS;1;Flandre
9170;Sint-Pauwels;46020;SINT-GILLIS-WAAS;1;Flandre
9180;Moerbeke-Waas;44045;MOERBEKE;1;Flandre
9185;Wachtebeke;44073;WACHTEBEKE;1;Flandre
9190;Kemzeke;46024;STEKENE;1;Flandre
9190;Stekene;46024;STEKENE;1;Flandre
9200;Appels;42006;TERMONDE;1;Flandre
9200;Baasrode;42006;TERMONDE;1;Flandre
9200;Dendermonde;42006;TERMONDE;1;Flandre
9200;Grembergen;42006;TERMONDE;1;Flandre
9200;Mespelare;42006;TERMONDE;1;Flandre
9200;Oudegem;42006;TERMONDE;1;Flandre
9200;Schoonaarde;42006;TERMONDE;1;Flandre
9200;Sint-Gillis-bij-Dendermonde;42006;TERMONDE;1;Flandre
9220;Hamme (O.-Vl.);42008;HAMME;1;Flandre
9220;Moerzeke;42008;HAMME;1;Flandre
9230;Massemen;42025;WETTEREN;1;Flandre
9230;Westrem;42025;WETTEREN;1;Flandre
9230;Wetteren;42025;WETTEREN;1;Flandre
9240;Zele;42028;ZELE;1;Flandre
9250;Waasmunster;42023;WAASMUNSTER;1;Flandre
9255;Buggenhout;42004;BUGGENHOUT;1;Flandre
9255;Opdorp;42004;BUGGENHOUT;1;Flandre
9260;Schellebelle;42026;WICHELEN;1;Flandre
9260;Serskamp;42026;WICHELEN;1;Flandre
9260;Wichelen;42026;WICHELEN;1;Flandre
9270;Kalken;42010;LAARNE;1;Flandre
9270;Laarne;42010;LAARNE;1;Flandre
9280;Denderbelle;42011;LEBBEKE;1;Flandre
9280;Lebbeke;42011;LEBBEKE;1;Flandre
9280;Wieze;42011;LEBBEKE;1;Flandre
9290;Berlare;42003;BERLARE;1;Flandre
9290;Overmere;42003;BERLARE;1;Flandre
9290;Uitbergen;42003;BERLARE;1;Flandre
9300;Aalst;41002;ALOST;1;Flandre
9308;Gijzegem;41002;ALOST;1;Flandre
9308;Hofstade (O.-Vl.);41002;ALOST;1;Flandre
9310;Baardegem;41002;ALOST;1;Flandre
9310;Herdersem;41002;ALOST;1;Flandre
9310;Meldert (O.-Vl.);41002;ALOST;1;Flandre
9310;Moorsel;41002;ALOST;1;Flandre
9320;Erembodegem (Aalst);41002;ALOST;1;Flandre
9320;Nieuwerkerken (Aalst);41002;ALOST;1;Flandre
9340;Impe;41034;LEDE;1;Flandre
9340;Lede;41034;LEDE;1;Flandre
9340;Oordegem;41034;LEDE;1;Flandre
9340;Smetlede;41034;LEDE;1;Flandre
9340;Wanzele;41034;LEDE;1;Flandre
9400;Appelterre-Eichem;41048;NINOVE;1;Flandre
9400;Denderwindeke;41048;NINOVE;1;Flandre
9400;Lieferinge;41048;NINOVE;1;Flandre
9400;Nederhasselt;41048;NINOVE;1;Flandre
9400;Ninove;41048;NINOVE;1;Flandre
9400;Okegem;41048;NINOVE;1;Flandre
9400;Voorde;41048;NINOVE;1;Flandre
9401;Pollare;41048;NINOVE;1;Flandre
9402;Meerbeke;41048;NINOVE;1;Flandre
9403;Neigem;41048;NINOVE;1;Flandre
9404;Aspelare;41048;NINOVE;1;Flandre
9406;Outer;41048;NINOVE;1;Flandre
9420;Aaigem;41082;ERPE-MERE;1;Flandre
9420;Bambrugge;41082;ERPE-MERE;1;Flandre
9420;Burst;41082;ERPE-MERE;1;Flandre
9420;Erondegem;41082;ERPE-MERE;1;Flandre
9420;Erpe;41082;ERPE-MERE;1;Flandre
9420;Erpe-Mere;41082;ERPE-MERE;1;Flandre
9420;Mere;41082;ERPE-MERE;1;Flandre
9420;Ottergem;41082;ERPE-MERE;1;Flandre
9420;Vlekkem;41082;ERPE-MERE;1;Flandre
9450;Denderhoutem;41024;HAALTERT;1;Flandre
9450;Haaltert;41024;HAALTERT;1;Flandre
9450;Heldergem;41024;HAALTERT;1;Flandre
9451;Kerksken;41024;HAALTERT;1;Flandre
9470;Denderleeuw;41011;DENDERLEEUW;1;Flandre
9472;Iddergem;41011;DENDERLEEUW;1;Flandre
9473;Welle;41011;DENDERLEEUW;1;Flandre
9500;Geraardsbergen;41018;GRAMMONT;1;Flandre
9500;Goeferdinge;41018;GRAMMONT;1;Flandre
9500;Moerbeke;41018;GRAMMONT;1;Flandre
9500;Nederboelare;41018;GRAMMONT;1;Flandre
9500;Onkerzele;41018;GRAMMONT;1;Flandre
9500;Ophasselt;41018;GRAMMONT;1;Flandre
9500;Overboelare;41018;GRAMMONT;1;Flandre
9500;Viane;41018;GRAMMONT;1;Flandre
9500;Zarlardinge;41018;GRAMMONT;1;Flandre
9506;Grimminge;41018;GRAMMONT;1;Flandre
9506;Idegem;41018;GRAMMONT;1;Flandre
9506;Nieuwenhove;41018;GRAMMONT;1;Flandre
9506;Schendelbeke;41018;GRAMMONT;1;Flandre
9506;Smeerebbe-Vloerzegem;41018;GRAMMONT;1;Flandre
9506;Waarbeke;41018;GRAMMONT;1;Flandre
9506;Zandbergen;41018;GRAMMONT;1;Flandre
9520;Bavegem;41063;SINT-LIEVENS-HOUTEM;1;Flandre
9520;Sint-Lievens-Houtem;41063;SINT-LIEVENS-HOUTEM;1;Flandre
9520;Vlierzele;41063;SINT-LIEVENS-HOUTEM;1;Flandre
9520;Zonnegem;41063;SINT-LIEVENS-HOUTEM;1;Flandre
9521;Letterhoutem;41063;SINT-LIEVENS-HOUTEM;1;Flandre
9550;Herzele;41027;HERZELE;1;Flandre
9550;Hillegem;41027;HERZELE;1;Flandre
9550;Sint-Antelinks;41027;HERZELE;1;Flandre
9550;Sint-Lievens-Esse;41027;HERZELE;1;Flandre
9550;Steenhuize-Wijnhuize;41027;HERZELE;1;Flandre
9550;Woubrechtegem;41027;HERZELE;1;Flandre
9551;Ressegem;41027;HERZELE;1;Flandre
9552;Borsbeke;41027;HERZELE;1;Flandre
9570;Deftinge;45063;LIERDE;1;Flandre
9570;Lierde;45063;LIERDE;1;Flandre
9570;Sint-Maria-Lierde;45063;LIERDE;1;Flandre
9571;Hemelveerdegem;45063;LIERDE;1;Flandre
9572;Sint-Martens-Lierde;45063;LIERDE;1;Flandre
9600;Renaix;45041;RENAIX;1;Flandre
9600;Ronse;45041;RENAIX;1;Flandre
9620;Elene;41081;ZOTTEGEM;1;Flandre
9620;Erwetegem;41081;ZOTTEGEM;1;Flandre
9620;Godveerdegem;41081;ZOTTEGEM;1;Flandre
9620;Grotenberge;41081;ZOTTEGEM;1;Flandre
9620;Leeuwergem;41081;ZOTTEGEM;1;Flandre
9620;Oombergen (Zottegem);41081;ZOTTEGEM;1;Flandre
9620;Sint-Goriks-Oudenhove;41081;ZOTTEGEM;1;Flandre
9620;Sint-Maria-Oudenhove (Zottegem);41081;ZOTTEGEM;1;Flandre
9620;Strijpen;41081;ZOTTEGEM;1;Flandre
9620;Velzeke-Ruddershove;41081;ZOTTEGEM;1;Flandre
9620;Zottegem;41081;ZOTTEGEM;1;Flandre
9630;Beerlegem;45065;ZWALM;1;Flandre
9630;Dikkele;45065;ZWALM;1;Flandre
9630;Hundelgem;45065;ZWALM;1;Flandre
9630;Meilegem;45065;ZWALM;1;Flandre
9630;Munkzwalm;45065;ZWALM;1;Flandre
9630;Paulatem;45065;ZWALM;1;Flandre
9630;Roborst;45065;ZWALM;1;Flandre
9630;Rozebeke;45065;ZWALM;1;Flandre
9630;Sint-Blasius-Boekel;45065;ZWALM;1;Flandre
9630;Sint-Denijs-Boekel;45065;ZWALM;1;Flandre
9630;Sint-Maria-Latem;45065;ZWALM;1;Flandre
9630;Zwalm;45065;ZWALM;1;Flandre
9636;Nederzwalm-Hermelgem;45065;ZWALM;1;Flandre
9660;Brakel;45059;BRAKEL;1;Flandre
9660;Elst;45059;BRAKEL;1;Flandre
9660;Everbeek;45059;BRAKEL;1;Flandre
9660;Michelbeke;45059;BRAKEL;1;Flandre
9660;Nederbrakel;45059;BRAKEL;1;Flandre
9660;Opbrakel;45059;BRAKEL;1;Flandre
9660;Zegelsem;45059;BRAKEL;1;Flandre
9661;Parike;45059;BRAKEL;1;Flandre
9667;Horebeke;45062;HOREBEKE;1;Flandre
9667;Sint-Kornelis-Horebeke;45062;HOREBEKE;1;Flandre
9667;Sint-Maria-Horebeke;45062;HOREBEKE;1;Flandre
9680;Etikhove;45064;MAARKEDAL;1;Flandre
9680;Maarkedal;45064;MAARKEDAL;1;Flandre
9680;Maarke-Kerkem;45064;MAARKEDAL;1;Flandre
9681;Nukerke;45064;MAARKEDAL;1;Flandre
9688;Schorisse;45064;MAARKEDAL;1;Flandre
9690;Berchem (O.-Vl.);45060;KLUISBERGEN;1;Flandre
9690;Kluisbergen;45060;KLUISBERGEN;1;Flandre
9690;Kwaremont;45060;KLUISBERGEN;1;Flandre
9690;Ruien;45060;KLUISBERGEN;1;Flandre
9690;Zulzeke;45060;KLUISBERGEN;1;Flandre
9700;Bevere;45035;AUDENARDE;1;Flandre
9700;Edelare;45035;AUDENARDE;1;Flandre
9700;Eine;45035;AUDENARDE;1;Flandre
9700;Ename;45035;AUDENARDE;1;Flandre
9700;Heurne;45035;AUDENARDE;1;Flandre
9700;Leupegem;45035;AUDENARDE;1;Flandre
9700;Mater;45035;AUDENARDE;1;Flandre
9700;Melden;45035;AUDENARDE;1;Flandre
9700;Mullem;45035;AUDENARDE;1;Flandre
9700;Nederename;45035;AUDENARDE;1;Flandre
9700;Oudenaarde;45035;AUDENARDE;1;Flandre
9700;Volkegem;45035;AUDENARDE;1;Flandre
9700;Welden;45035;AUDENARDE;1;Flandre
9750;Huise;45057;ZINGEM;1;Flandre
9750;Ouwegem;45057;ZINGEM;1;Flandre
9750;Zingem;45057;ZINGEM;1;Flandre
9770;Kruishoutem;45017;KRUISHOUTEM;1;Flandre
9771;Nokere;45017;KRUISHOUTEM;1;Flandre
9772;Wannegem-Lede;45017;KRUISHOUTEM;1;Flandre
9790;Elsegem;45061;WORTEGEM-PETEGEM;1;Flandre
9790;Moregem;45061;WORTEGEM-PETEGEM;1;Flandre
9790;Ooike (Wortegem-Petegem);45061;WORTEGEM-PETEGEM;1;Flandre
9790;Petegem-aan-de-Schelde;45061;WORTEGEM-PETEGEM;1;Flandre
9790;Wortegem;45061;WORTEGEM-PETEGEM;1;Flandre
9790;Wortegem-Petegem;45061;WORTEGEM-PETEGEM;1;Flandre
9800;Astene;44011;DEINZE;1;Flandre
9800;Bachte-Maria-Leerne;44011;DEINZE;1;Flandre
9800;Deinze;44011;DEINZE;1;Flandre
9800;Gottem;44011;DEINZE;1;Flandre
9800;Grammene;44011;DEINZE;1;Flandre
9800;Meigem;44011;DEINZE;1;Flandre
9800;Petegem-aan-de-Leie;44011;DEINZE;1;Flandre
9800;Sint-Martens-Leerne;44011;DEINZE;1;Flandre
9800;Vinkt;44011;DEINZE;1;Flandre
9800;Wontergem;44011;DEINZE;1;Flandre
9800;Zeveren;44011;DEINZE;1;Flandre
9810;Eke;44048;NAZARETH;1;Flandre
9810;Nazareth;44048;NAZARETH;1;Flandre
9820;Bottelare;44043;MERELBEKE;1;Flandre
9820;Lemberge;44043;MERELBEKE;1;Flandre
9820;Melsen;44043;MERELBEKE;1;Flandre
9820;Merelbeke;44043;MERELBEKE;1;Flandre
9820;Munte;44043;MERELBEKE;1;Flandre
9820;Schelderode;44043;MERELBEKE;1;Flandre
9830;Sint-Martens-Latem;44064;SINT-MARTENS-LATEM;1;Flandre
9831;Deurle;44064;SINT-MARTENS-LATEM;1;Flandre
9840;De Pinte;44012;DE PINTE;1;Flandre
9840;Zevergem;44012;DE PINTE;1;Flandre
9850;Hansbeke;44049;NEVELE;1;Flandre
9850;Landegem;44049;NEVELE;1;Flandre
9850;Merendree;44049;NEVELE;1;Flandre
9850;Nevele;44049;NEVELE;1;Flandre
9850;Poesele;44049;NEVELE;1;Flandre
9850;Vosselare;44049;NEVELE;1;Flandre
9860;Balegem;44052;OOSTERZELE;1;Flandre
9860;Gijzenzele;44052;OOSTERZELE;1;Flandre
9860;Landskouter;44052;OOSTERZELE;1;Flandre
9860;Moortsele;44052;OOSTERZELE;1;Flandre
9860;Oosterzele;44052;OOSTERZELE;1;Flandre
9860;Scheldewindeke;44052;OOSTERZELE;1;Flandre
9870;Machelen (O.-Vl.);44081;ZULTE;1;Flandre
9870;Olsene;44081;ZULTE;1;Flandre
9870;Zulte;44081;ZULTE;1;Flandre
9880;Aalter;44001;AALTER;1;Flandre
9880;Lotenhulle;44001;AALTER;1;Flandre
9880;Poeke;44001;AALTER;1;Flandre
9881;Bellem;44001;AALTER;1;Flandre
9890;Asper;44020;GAVERE;1;Flandre
9890;Baaigem;44020;GAVERE;1;Flandre
9890;Dikkelvenne;44020;GAVERE;1;Flandre
9890;Gavere;44020;GAVERE;1;Flandre
9890;Semmerzake;44020;GAVERE;1;Flandre
9890;Vurste;44020;GAVERE;1;Flandre
9900;Eeklo;43005;EEKLO;1;Flandre
9910;Knesselare;44029;KNESSELARE;1;Flandre
9910;Ursel;44029;KNESSELARE;1;Flandre
9920;Lovendegem;44036;LOVENDEGEM;1;Flandre
9921;Vinderhoute;44036;LOVENDEGEM;1;Flandre
9930;Zomergem;44080;ZOMERGEM;1;Flandre
9931;Oostwinkel;44080;ZOMERGEM;1;Flandre
9932;Ronsele;44080;ZOMERGEM;1;Flandre
9940;Ertvelde;44019;EVERGEM;1;Flandre
9940;Evergem;44019;EVERGEM;1;Flandre
9940;Kluizen;44019;EVERGEM;1;Flandre
9940;Sleidinge;44019;EVERGEM;1;Flandre
9950;Waarschoot;44072;WAARSCHOOT;1;Flandre
9960;Assenede;43002;ASSENEDE;1;Flandre
9961;Boekhoute;43002;ASSENEDE;1;Flandre
9968;Bassevelde;43002;ASSENEDE;1;Flandre
9968;Oosteeklo;43002;ASSENEDE;1;Flandre
9970;Kaprijke;43007;KAPRIJKE;1;Flandre
9971;Lembeke;43007;KAPRIJKE;1;Flandre
9980;Sint-Laureins;43014;SINT-LAUREINS;1;Flandre
9981;Sint-Margriete;43014;SINT-LAUREINS;1;Flandre
9982;Sint-Jan-in-Eremo;43014;SINT-LAUREINS;1;Flandre
9988;Waterland-Oudeman;43014;SINT-LAUREINS;1;Flandre
9988;Watervliet;43014;SINT-LAUREINS;1;Flandre
9990;Maldegem;43010;MALDEGEM;1;Flandre
9991;Adegem;43010;MALDEGEM;1;Flandre
9992;Middelburg;43010;MALDEGEM;1;Flandre
"""

def objects():
    Country = resolve_model('countries.Country')
    City = resolve_model('countries.City')
    
    BE = Country.objects.get(pk='BE')
    
    #~ yield City(name="Dummy",country=BE)
    
    if 'fr' in settings.LINO.languages:
        logger.info("Loading country INS codes")
        for ln in COUNTRIES.splitlines():
            if not ln: continue
            a = ln.split("',",1)
            code,name = a[0].split(None,1)
            assert name.startswith("'")
            name = name[1:]
            try:
                country = Country.objects.get(name_fr=name)
                country.ins_code = code
                logger.debug("ins_code %s --> country %s ",code,country)
                #~ country.save()
                yield country
            except Country.DoesNotExist:
                logger.warning("Failed to set ins_code %s because there's no country %r",code,name)
                pass
                
    logger.info("Loading city INS codes")
    for ln in CITIES.splitlines():
        if not ln.strip(): continue
        a = [s.strip() for s in ln.split(';')]
        zip_code, name, ins_code, x, y, z = a
        if not zip_code: continue
        try:
            city = City.objects.get(country=BE,zip_code=zip_code,name=name)
            city.ins_code = ins_code
            logger.debug("ins_code %s --> city %s",ins_code,city)
            yield city
        except City.DoesNotExist:
            logger.warning("Failed to set ins_code %s because there's no city %s %s",ins_code,zip_code,name)
            
        #~ for city in City.objects.filter(country=BE,zip_code=zip_code):
            #~ if city.ins_code and city.ins_code != ins_code:
                #~ logger.warning("Duplicate ins_code %s for %s %s",ins_code,zip_code, name)
            #~ city.ins_code = ins_code
            #~ logger.debug("ins_code %s --> city %s",ins_code,city)
            #~ city.save()
            #~ yield city
        