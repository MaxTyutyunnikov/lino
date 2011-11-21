#coding: utf-8

"""

This is originally based on 
http://www.davros.org/misc/iso3166.html

See also http://www.iso.org/iso/country_codes.htm

"""

import os
from xml.dom import minidom
#~ import logging
#~ logger = logging.getLogger('lino')

from lino.utils import ucsv
from lino.utils import dblogger as logger
from lino.utils.babel import babel_values, DEFAULT_LANGUAGE
from lino.modlib.countries.models import Country


#~ TABLE1 = """
#~ AF 	AFG 	004 		Afghanistan
#~ AL 	ALB 	008 		Albania, People's Socialist Republic of
#~ DZ 	DZA 	012 		Algeria, People's Democratic Republic of
#~ AS 	ASM 	016 		American Samoa
#~ AD 	AND 	020 		Andorra, Principality of
#~ AO 	AGO 	024 		Angola, Republic of
#~ AI 	AIA 	660 	 	Anguilla
#~ AQ 	ATA 	010 		Antarctica (the territory South of 60 deg S)
#~ AG 	ATG 	028 		Antigua and Barbuda
#~ AR 	ARG 	032 		Argentina, Argentine Republic
#~ AM 	ARM 	051 	 	Armenia
#~ AW 	ABW 	533 	 	Aruba
#~ AU 	AUS 	036 		Australia, Commonwealth of
#~ AT 	AUT 	040 		Austria, Republic of
#~ AZ 	AZE 	031 	 	Azerbaijan, Republic of
#~ BS 	BHS 	044 		Bahamas, Commonwealth of the
#~ BH 	BHR 	048 		Bahrain, Kingdom of
#~ BD 	BGD 	050 		Bangladesh, People's Republic of
#~ BB 	BRB 	052 		Barbados
#~ BY 	BLR 	112 	 	Belarus
#~ BE 	BEL 	056 		Belgium
#~ BZ 	BLZ 	084 		Belize
#~ BJ 	BEN 	204 	 	Benin (was Dahomey), People's Republic of
#~ BM 	BMU 	060 		Bermuda
#~ BT 	BTN 	064 		Bhutan, Kingdom of
#~ BO 	BOL 	068 		Bolivia, Republic of
#~ BA 	BIH 	070 	 	Bosnia and Herzegovina
#~ BW 	BWA 	072 		Botswana, Republic of
#~ BV 	BVT 	074 		Bouvet Island (Bouvetoya)
#~ BR 	BRA 	076 		Brazil, Federative Republic of
#~ IO 	IOT 	086 		British Indian Ocean Territory (Chagos Archipelago)
#~ VG 	VGB 	092 		British Virgin Islands
#~ BN 	BRN 	096 		Brunei Darussalam
#~ BG 	BGR 	100 		Bulgaria, People's Republic of
#~ BF 	BFA 	854 	 	Burkina Faso (was Upper Volta)
#~ BI 	BDI 	108 		Burundi, Republic of
#~ KH 	KHM 	116 		Cambodia, Kingdom of (was Khmer Republic/Kampuchea, Democratic)
#~ CM 	CMR 	120 		Cameroon, United Republic of
#~ CA 	CAN 	124 		Canada
#~ CV 	CPV 	132 		Cape Verde, Republic of
#~ KY 	CYM 	136 		Cayman Islands
#~ CF 	CAF 	140 		Central African Republic
#~ TD 	TCD 	148 		Chad, Republic of
#~ CL 	CHL 	152 		Chile, Republic of
#~ CN 	CHN 	156 		China, People's Republic of
#~ CX 	CXR 	162 		Christmas Island
#~ CC 	CCK 	166 		Cocos (Keeling) Islands
#~ CO 	COL 	170 		Colombia, Republic of
#~ KM 	COM 	174 		Comoros, Union of the
#~ CD 	COD 	180 	 	Congo, Democratic Republic of (was Zaire)
#~ CG 	COG 	178 		Congo, People's Republic of
#~ CK 	COK 	184 		Cook Islands
#~ CR 	CRI 	188 		Costa Rica, Republic of
#~ CI 	CIV 	384 		Cote D'Ivoire, Ivory Coast, Republic of the
#~ CU 	CUB 	192 		Cuba, Republic of
#~ CY 	CYP 	196 		Cyprus, Republic of
#~ CZ 	CZE 	203 	 	Czech Republic
#~ DK 	DNK 	208 		Denmark, Kingdom of
#~ DJ 	DJI 	262 	 	Djibouti, Republic of (was French Afars and Issas)
#~ DM 	DMA 	212 		Dominica, Commonwealth of
#~ DO 	DOM 	214 		Dominican Republic
#~ EC 	ECU 	218 		Ecuador, Republic of
#~ EG 	EGY 	818 		Egypt, Arab Republic of
#~ SV 	SLV 	222 		El Salvador, Republic of
#~ GQ 	GNQ 	226 		Equatorial Guinea, Republic of
#~ ER 	ERI 	232 	 	Eritrea
#~ EE 	EST 	233 	 	Estonia
#~ ET 	ETH 	231 	 	Ethiopia
#~ FO 	FRO 	234 		Faeroe Islands
#~ FK 	FLK 	238 		Falkland Islands (Malvinas)
#~ FJ 	FJI 	242 		Fiji, Republic of the Fiji Islands
#~ FI 	FIN 	246 		Finland, Republic of
#~ FR 	FRA 	250 		France, French Republic
#~ GF 	GUF 	254 		French Guiana
#~ PF 	PYF 	258 		French Polynesia
#~ TF 	ATF 	260 	 	French Southern Territories
#~ GA 	GAB 	266 		Gabon, Gabonese Republic
#~ GM 	GMB 	270 		Gambia, Republic of the
#~ GE 	GEO 	268 	 	Georgia
#~ DE 	DEU 	276 	 	Germany
#~ GH 	GHA 	288 		Ghana, Republic of
#~ GI 	GIB 	292 		Gibraltar
#~ GR 	GRC 	300 		Greece, Hellenic Republic
#~ GL 	GRL 	304 		Greenland
#~ GD 	GRD 	308 		Grenada
#~ GP 	GLP 	312 		Guadaloupe
#~ GU 	GUM 	316 		Guam
#~ GT 	GTM 	320 		Guatemala, Republic of
#~ GN 	GIN 	324 		Guinea, Revolutionary People's Rep'c of
#~ GW 	GNB 	624 		Guinea-Bissau, Republic of (was Portuguese Guinea)
#~ GY 	GUY 	328 		Guyana, Republic of
#~ HT 	HTI 	332 		Haiti, Republic of
#~ HM 	HMD 	334 		Heard and McDonald Islands
#~ VA 	VAT 	336 	 	Holy See (Vatican City State)
#~ HN 	HND 	340 		Honduras, Republic of
#~ HK 	HKG 	344 		Hong Kong, Special Administrative Region of China
#~ HR 	HRV 	191 	 	Hrvatska (Croatia)
#~ HU 	HUN 	348 		Hungary, Hungarian People's Republic
#~ IS 	ISL 	352 		Iceland, Republic of
#~ IN 	IND 	356 		India, Republic of
#~ ID 	IDN 	360 		Indonesia, Republic of
#~ IR 	IRN 	364 		Iran, Islamic Republic of
#~ IQ 	IRQ 	368 		Iraq, Republic of
#~ IE 	IRL 	372 		Ireland
#~ IL 	ISR 	376 		Israel, State of
#~ IT 	ITA 	380 		Italy, Italian Republic
#~ JM 	JAM 	388 		Jamaica
#~ JP 	JPN 	392 		Japan
#~ JO 	JOR 	400 		Jordan, Hashemite Kingdom of
#~ KZ 	KAZ 	398 	 	Kazakhstan, Republic of
#~ KE 	KEN 	404 		Kenya, Republic of
#~ KI 	KIR 	296 	 	Kiribati, Republic of (was Gilbert Islands)
#~ KP 	PRK 	408 		Korea, Democratic People's Republic of
#~ KR 	KOR 	410 		Korea, Republic of
#~ KW 	KWT 	414 		Kuwait, State of
#~ KG 	KGZ 	417 		Kyrgyz Republic
#~ LA 	LAO 	418 		Lao People's Democratic Republic
#~ LV 	LVA 	428 	 	Latvia
#~ LB 	LBN 	422 		Lebanon, Lebanese Republic
#~ LS 	LSO 	426 		Lesotho, Kingdom of
#~ LR 	LBR 	430 		Liberia, Republic of
#~ LY 	LBY 	434 		Libyan Arab Jamahiriya
#~ LI 	LIE 	438 		Liechtenstein, Principality of
#~ LT 	LTU 	440 	 	Lithuania
#~ LU 	LUX 	442 		Luxembourg, Grand Duchy of
#~ MO 	MAC 	446 		Macao, Special Administrative Region of China
#~ MK 	MKD 	807 	 	Macedonia, the former Yugoslav Republic of
#~ MG 	MDG 	450 		Madagascar, Republic of
#~ MW 	MWI 	454 		Malawi, Republic of
#~ MY 	MYS 	458 		Malaysia
#~ MV 	MDV 	462 		Maldives, Republic of
#~ ML 	MLI 	466 		Mali, Republic of
#~ MT 	MLT 	470 		Malta, Republic of
#~ MH 	MHL 	584 	 	Marshall Islands
#~ MQ 	MTQ 	474 		Martinique
#~ MR 	MRT 	478 		Mauritania, Islamic Republic of
#~ MU 	MUS 	480 		Mauritius
#~ YT 	MYT 	175 	 	Mayotte
#~ MX 	MEX 	484 		Mexico, United Mexican States
#~ FM 	FSM 	583 	 	Micronesia, Federated States of
#~ MD 	MDA 	498 	 	Moldova, Republic of
#~ MC 	MCO 	492 		Monaco, Principality of
#~ MN 	MNG 	496 		Mongolia, Mongolian People's Republic
#~ MS 	MSR 	500 		Montserrat
#~ MA 	MAR 	504 		Morocco, Kingdom of
#~ MZ 	MOZ 	508 		Mozambique, People's Republic of
#~ MM 	MMR 	104 	 	Myanmar (was Burma)
#~ NA 	NAM 	516 		Namibia
#~ NR 	NRU 	520 		Nauru, Republic of
#~ NP 	NPL 	524 		Nepal, Kingdom of
#~ AN 	ANT 	530 	 	Netherlands Antilles
#~ NL 	NLD 	528 		Netherlands, Kingdom of the
#~ NC 	NCL 	540 		New Caledonia
#~ NZ 	NZL 	554 		New Zealand
#~ NI 	NIC 	558 		Nicaragua, Republic of
#~ NE 	NER 	562 		Niger, Republic of the
#~ NG 	NGA 	566 		Nigeria, Federal Republic of
#~ NU 	NIU 	570 		Niue, Republic of
#~ NF 	NFK 	574 		Norfolk Island
#~ MP 	MNP 	580 	 	Northern Mariana Islands
#~ NO 	NOR 	578 		Norway, Kingdom of
#~ OM 	OMN 	512 		Oman, Sultanate of (was Muscat and Oman)
#~ PK 	PAK 	586 		Pakistan, Islamic Republic of
#~ PW 	PLW 	585 	 	Palau
#~ PS 	PSE 	275 	 	Palestinian Territory, Occupied
#~ PA 	PAN 	591 	 	Panama, Republic of
#~ PG 	PNG 	598 		Papua New Guinea
#~ PY 	PRY 	600 		Paraguay, Republic of
#~ PE 	PER 	604 		Peru, Republic of
#~ PH 	PHL 	608 		Philippines, Republic of the
#~ PN 	PCN 	612 		Pitcairn Island
#~ PL 	POL 	616 		Poland, Polish People's Republic
#~ PT 	PRT 	620 		Portugal, Portuguese Republic
#~ PR 	PRI 	630 		Puerto Rico
#~ QA 	QAT 	634 		Qatar, State of
#~ RE 	REU 	638 		Reunion
#~ RO 	ROU 	642 	 	Romania, Socialist Republic of
#~ RU 	RUS 	643 	 	Russian Federation
#~ RW 	RWA 	646 		Rwanda, Rwandese Republic
#~ SH 	SHN 	654 		St. Helena
#~ KN 	KNA 	659 	 	St. Kitts and Nevis
#~ LC 	LCA 	662 		St. Lucia
#~ PM 	SPM 	666 		St. Pierre and Miquelon
#~ VC 	VCT 	670 		St. Vincent and the Grenadines
#~ WS 	WSM 	882 		Samoa, Independent State of (was Western Samoa)
#~ SM 	SMR 	674 		San Marino, Republic of
#~ ST 	STP 	678 		Sao Tome and Principe, Democratic Republic of
#~ SA 	SAU 	682 		Saudi Arabia, Kingdom of
#~ SN 	SEN 	686 		Senegal, Republic of
#~ CS 	SCG 	891 	 	Serbia and Montenegro
#~ SC 	SYC 	690 		Seychelles, Republic of
#~ SL 	SLE 	694 		Sierra Leone, Republic of
#~ SG 	SGP 	702 		Singapore, Republic of
#~ SK 	SVK 	703 	 	Slovakia (Slovak Republic)
#~ SI 	SVN 	705 	 	Slovenia
#~ SB 	SLB 	090 		Solomon Islands (was British Solomon Islands)
#~ SO 	SOM 	706 		Somalia, Somali Republic
#~ ZA 	ZAF 	710 		South Africa, Republic of
#~ GS 	SGS 	239 	 	South Georgia and the South Sandwich Islands
#~ ES 	ESP 	724 		Spain, Spanish State
#~ LK 	LKA 	144 		Sri Lanka, Democratic Socialist Republic of (was Ceylon)
#~ SD 	SDN 	736 		Sudan, Democratic Republic of the
#~ SR 	SUR 	740 		Suriname, Republic of
#~ SJ 	SJM 	744 		Svalbard & Jan Mayen Islands
#~ SZ 	SWZ 	748 		Swaziland, Kingdom of
#~ SE 	SWE 	752 		Sweden, Kingdom of
#~ CH 	CHE 	756 		Switzerland, Swiss Confederation
#~ SY 	SYR 	760 		Syrian Arab Republic
#~ TW 	TWN 	158 		Taiwan, Province of China
#~ TJ 	TJK 	762 	 	Tajikistan
#~ TZ 	TZA 	834 		Tanzania, United Republic of
#~ TH 	THA 	764 		Thailand, Kingdom of
#~ TL 	TLS 	626 	 	Timor-Leste, Democratic Republic of
#~ TG 	TGO 	768 		Togo, Togolese Republic
#~ TK 	TKL 	772 		Tokelau (Tokelau Islands)
#~ TO 	TON 	776 		Tonga, Kingdom of
#~ TT 	TTO 	780 		Trinidad and Tobago, Republic of
#~ TN 	TUN 	788 		Tunisia, Republic of
#~ TR 	TUR 	792 		Turkey, Republic of
#~ TM 	TKM 	795 	 	Turkmenistan
#~ TC 	TCA 	796 		Turks and Caicos Islands
#~ TV 	TUV 	798 		Tuvalu (was part of Gilbert & Ellice Islands)
#~ VI 	VIR 	850 		US Virgin Islands
#~ UG 	UGA 	800 		Uganda, Republic of
#~ UA 	UKR 	804 		Ukraine
#~ AE 	ARE 	784 		United Arab Emirates (was Trucial States)
#~ GB 	GBR 	826 		United Kingdom of Great Britain & N. Ireland
#~ UM 	UMI 	581 	 	United States Minor Outlying Islands
#~ US 	USA 	840 		United States of America
#~ UY 	URY 	858 		Uruguay, Eastern Republic of
#~ UZ 	UZB 	860 	 	Uzbekistan
#~ VU 	VUT 	548 	 	Vanuatu (was New Hebrides)
#~ VE 	VEN 	862 		Venezuela, Bolivarian Republic of
#~ VN 	VNM 	704 	 	Viet Nam, Socialist Republic of (was Democratic Republic of & Republic of)
#~ WF 	WLF 	876 		Wallis and Futuna Islands
#~ EH 	ESH 	732 	 	Western Sahara (was Spanish Sahara)
#~ YE 	YEM 	887 	 	Yemen
#~ ZM 	ZMB 	894 		Zambia, Republic of
#~ ZW 	ZWE 	716 	 	Zimbabwe (was Southern Rhodesia) 
#~ """

TABLE2 = """
BQAQ 	ATB 	000 British Antarctic Territory
BUMM 	BUR 	104 Burma, Socialist Republic of the Union of
BYAA 	BYS 	112 Byelorussian SSR Soviet Socialist Republic
CTKI 	CTE 	128 Canton & Enderbury Islands
CSHH 	CSK 	200 Czechoslovakia, Czechoslovak Socialist Republic
DYBJ 	DHY 	204 Dahomey
NQAQ 	ATN 	216 Dronning Maud Land
TPTL 	TMP 	626 East Timor (was Portuguese Timor)
AIDJ 	AFI 	262 French Afars and Issas
FQHH 	ATF 	000 French Southern and Antarctic Territories (now split between AQ and TF)
DDDE 	DDR 	278 German Democratic Republic
GEHH 	GEL 	296 Gilbert & Ellice Islands (now split into Kiribati and Tuvalu)
JTUM 	JTN 	396 Johnston Island
MIUM 	MID 	488 Midway Islands
NTHH 	NTZ 	536 Neutral Zone (formerly between Saudi Arabia & Iraq)
NHVU 	NHB 	548 New Hebrides
PCHH 	PCI 	582 Pacific Islands (trust territory) (divided into FM, MH, MP, and PW)
PZPA 	PCZ 	000 Panama Canal Zone
SKIN 	SKM 	000 Sikkim
RHZW 	RHO 	716 Southern Rhodesia
PUUM 	PUS 	849 US Miscellaneous Pacific Islands
SUHH 	SUN 	810 USSR, Union of Soviet Socialist Republics
HVBF 	HVO 	854 Upper Volta, Republic of
VDVN 	VDR 	000 Viet-Nam, Democratic Republic of
WKUM 	WAK 	872 Wake Island
YDYE 	YMD 	720 Yemen, Democratic, People's Democratic Republic of
YUCS 	YUG 	891 Yugoslavia, Federal Republic of
ZRCD 	ZAR 	180 Zaire, Republic of
"""

#~ unused = """
#~ FX 	  FXX 	249 France, Metropolitan
#~ EH  	ESH 	732 Spanish Sahara (now Western Sahara)
#~ YU  	YUG 	890 Yugoslavia, Socialist Federal Republic of
#~ """

#~ from lino.utils.instantiator import Instantiator, i2d
#~ country = Instantiator('countries.Country','isocode name').build

COUNTRIES = {}

if False:
    for ln in TABLE1.splitlines() + TABLE2.splitlines():
        ln = ln.strip()
        if ln:
            COUNTRIES[code1] = dict(en=name)
            code1, code2, code3, name = ln.split(None,3)
            #~ yield country(code1,name)
            #~ yield Country()
        

"""
http://countrylist.net/        
"""
if False:

    fn = os.path.join(os.path.dirname(__file__),'CountrysNF.csv')
    r = ucsv.UnicodeReader(open(fn),delimiter=';')
    n = 0
    for rec in r:
        n += 1
        if len(rec) != 11:
            logger.warning("Ignored line %d (len(%r) is %d)",n,rec,len(rec))
        else:
            iso2 = rec[5]
            iso3 = rec[6]
            de = rec[2]
            en = rec[3]
            if iso2:
                if COUNTRIES.has_key(iso2):
                    logger.debug("Ignored duplicate country %r",iso2)
                else:
                    COUNTRIES[iso2]=dict(en=en,de=de,iso3=iso3,fr=en,nl=en)

    for ln in TABLE2.splitlines():
        ln = ln.strip()
        if ln:
            code1, code2, code3, name = ln.split(None,3)
            if COUNTRIES.has_key(code1):
                logger.debug("Ignored duplicate country %r",code1)
            else:
                COUNTRIES[code1] = dict(en=name,de=name,fr=name,nl=name)


    def old_objects():
                
        n = 0
        for code,kw in COUNTRIES.items():
            iso3 = kw.get('iso3','')
            kw = babel_values('name',**kw)
            if kw['name']:
                kw.update(iso3=iso3)
                n += 1
                yield Country(isocode=code,**kw)
            else:
                logger.debug("%r : no name for default babel language %s",code,DEFAULT_LANGUAGE)
        logger.info("Installed %d countries",n)
                
            
def objects():
            
    n = 0
    """
    http://users.pandora.be/bosteels/countries.xml
    """
    fn = os.path.join(os.path.dirname(__file__),'countries.xml')
    dom = minidom.parse(fn)
    #~ print dom.documentElement.__class__
    #~ print dom.documentElement
    for coun in dom.documentElement.getElementsByTagName('coun:country'):
        #~ print coun.toxml()
        #~ print c.attributes['coun:alpha2']
        names = {}
        for name in coun.getElementsByTagName('coun:name'):
            assert len(name.childNodes) == 1
            #~ print [n.data for n in ]
            #~ print name.firstChild.data
            names[str(name.attributes['lang'].value)] = name.firstChild.data
            
        kw = babel_values('name',**names)
        kw.update(
          isocode = coun.getElementsByTagName('coun:alpha2')[0].childNodes[0].data,
          iso3 = coun.getElementsByTagName('coun:alpha3')[0].childNodes[0].data,
          )
        
        if kw['name']:
            #~ kw.update(iso3=iso3)
            n += 1
            yield Country(**kw)
        else:
            logger.debug("%r : no name for default babel language %s",code,DEFAULT_LANGUAGE)
            
    for ln in TABLE2.splitlines():
        ln = ln.strip()
        if ln:
            code1, code2, code3, name = ln.split(None,3)
            n += 1
            yield Country(isocode=code1,name=name)
            
            
    logger.info("Installed %d countries",n)
