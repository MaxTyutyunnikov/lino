## Copyright 2005-2006 Luc Saffre 

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

"""

Belgian price indexing

Example:

    Price January 2003 (200301) was 200,-
    How much is the indexed price in June 2004 (200406)?
    Anwer:
    - oldIndex = index in 200301 = 110,94
    - newIndex = index in 200406 = 111.85
    - newPrice = oldPrice * newIndex / oldIndex

>>> print indexed_price(200301,200405,200)
204.92

Sources:

-
http://mineco.fgov.be/informations/indexes/indint1xls_2003_2005_22_fr.htm

- L'indexation du loyer:
  http://www.notaire.be/info/location/304_indexation_du_loyer.htm

- Tableau des indices
  http://www.snp-aes.be/indextabelFR.htm


File lino/tests/51.py contains more test cases.

"""

from lino.tools.months import Month
from lino.tools.fixedpoint import FixedPoint



class Index:
    def __init__(self,start,values):
        assert isinstance(start,Month)
        self.start = start
        self.values=values

    def coeff(self,baseMonth,newMonth):
        assert baseMonth >= self.start
        baseIndex=self.values[baseMonth-self.start]
        try:
            newIndex=self.values[newMonth-self.start]
        except IndexError,e:
            print newMonth, "-", self.start, "=", newMonth-self.start
            raise
        #print self.start,baseIndex, newIndex
        return newIndex / baseIndex
        

sante1988 = Index(Month.parse('198212'), (
# 1982:    
82.53, 
# 1983:
83.54, 84.00, 84.31, 84.57, 85.02, 85.57,
86.39, 87.21, 87.82, 87.83, 88.28, 88.44, 
# 1984:
89.27, 89.94, 90.32, 90.91, 91.11, 91.37,
91.86, 92.22, 92.50, 92.92, 92.96, 93.17,

# 1985:
93.77, 94.74, 95.50, 95.87, 95.97, 95.99,
96.51, 96.51, 96.71, 96.66, 96.89, 96.92,

# 1986:
97.03, 97.11, 96.96, 97.26, 97.04, 97.17,
97.16, 97.25, 97.59, 97.48, 97.40, 97.49,

# 1987:
97.89, 98.08, 98.19, 98.64, 98.68, 98.79,
99.14, 99.45, 99.27, 99.17, 98.87, 98.90,

# 1988
 98.82,  99.10,  99.13,  99.58,  99.67,  99.84,
100.15, 100.36, 100.47, 100.50, 100.44, 100.80,

# 1989
101.18, 101.63, 101.87, 102.56, 102.65, 102.84,
103.18, 103.52, 104.04, 104.16, 104.03, 104.43,

# 1990
104.82, 105.07, 105.33, 105.81, 105.84, 105.91,
106.28, 106.90, 107.87, 108.60, 108.21, 108.08,

# 1991
108.89, 109.25, 108.80, 108.86, 109.25, 109.74,
110.34, 110.68, 110.60, 111.01, 111.29, 111.09,

# 1992
111.37, 111.72, 111.75, 111.87, 112.28, 112.64,
113.16, 112.97, 113.17, 113.41, 113.77, 113.76,

# 1993
114.53, 114.82, 115.02, 115.12, 115.30, 115.32,
116.08, 116.57, 116.36, 116.50, 116.65, 116.83,

# 1994
115.65, 116.00, 115.92, 116.10, 116.44, 116.65,
117.45, 117.58, 117.43, 117.24, 117.25, 117.29,

# 1995
117.83, 118.22, 118.11, 118.23, 118.15, 118.23,
119.03, 119.38, 118.97, 118.78, 118.97, 118.94,

# 1996
119.86, 120.09, 120.13, 120.15, 119.90, 120.00,
120.84, 121.17, 120.81, 121.00, 121.12, 121.29,

# 1997
122.09, 121.88, 121.31, 121.33, 121.45, 121.67,
122.78, 122.84, 122.34, 122.37, 122.72, 122.68,

# 1998
122.78, 123.08, 122.92, 123.51, 124.18, 124.05,
124.36, 123.87, 123.84, 123.85, 123.83, 123.84,

# 1999
124.27, 124.56, 124.57, 124.87, 125.08, 124.86,
124.89, 124.58, 124.83, 124.97, 125.19, 125.42,

# 2000
125.74, 126.07, 126.35, 126.69, 126.85, 127.12,
127.43, 127.49, 128.05, 127.85, 128.35, 128.29,

# 2001
128.38, 128.80, 129.18, 130.14, 130.77, 131.19,
131.32, 131.41, 131.61, 131.69, 131.94, 131.70,

# 2002
132.54, 132.74, 133.02, 132.76, 133.05, 132.74,
133.16, 133.10, 133.37, 133.15, 133.18, 133.29,

# 2003
133.76, 134.51, 134.82, 134.71, 134.52, 134.86,
135.11, 135.28, 135.61, 135.22, 135.47, 135.42,

# 2004
135.85, 136.27, 136.30, 136.85, 137.05, 137.03,
137.45, 137.49, 137.55, 138.04, 138.03, 137.75,

# 2005
138.27, 138.99, 139.74, 139.70, 139.97, 140.21,
140.78, 140.80, 140.64, 140.42, 140.85, 140.96,

# 2006
	
141.04, 141.71, 141.60, 142.11, 142.59, 142.56

))






sante1996 = Index( Month.parse('199401'), (
	
# 1994:
    
95.92, 96.21, 96.14, 96.29, 96.58, 96.75,
97.41, 97.52, 97.40, 97.24, 97.25, 97.28,

#1995:
	
97.73, 98.05, 97.96, 98.06, 97.99, 98.06,
98.72, 99.01, 98.67, 98.52, 98.67, 98.65,

#1996:
	
 99.41,  99.60,  99.64,  99.65,  99.45,  99.53,
100.22, 100.50, 100.20, 100.36, 100.46, 100.60,

# 1997:
	
101.26, 101.09, 100.61, 100.63, 100.73, 100.91,
101.83, 101.88, 101.47, 101.49, 101.78, 101.75,

# 1998:
	
101.83, 102.08, 101.95, 102.44, 102.99, 102.89,
103.14, 102.74, 102.71, 102.72, 102.70, 102.71,

# 1999:
	
103.07, 103.31, 103.32, 103.57, 103.74, 103.56,
103.58, 103.33, 103.53, 103.65, 103.83, 104.02,

# 2000:
	
104.29, 104.56, 104.79, 105.08, 105.21, 105.43,
105.69, 105.74, 106.20, 106.04, 106.45, 106.40,

# 2001
	
106.48, 106.83, 107.14, 107.94, 108.46, 108.81,
108.92, 108.99, 109.16, 109.22, 109.43, 109.23,

# 2002
	
109.93, 110.09, 110.33, 110.11, 110.35, 110.09,
110.44, 110.39, 110.62, 110.43, 110.46, 110.55,

# 2003:
	
110.94, 111.56, 111.82, 111.73, 111.57, 111.85,
112.06, 112.20, 112.47, 112.15, 112.36, 112.32,

# 2004:
	
112.67, 113.02, 113.05, 113.50, 113.67, 113.65,
114.00, 114.03, 114.08, 114.49, 114.48, 114.25,

# 2005:
	
114.68, 115.28, 115.90, 115.87, 116.09, 116.29,
116.76, 116.78, 116.65, 116.46, 116.82, 116.91,
	
# 2006:

116.98, 117.54, 117.44, 117.87, 118.26, 118.24

))


sante2004 = Index( Month.parse('200601'), (
    
# 2006:
    
102.82, 103.31, 103.23, 103.60, 103.95, 103.93

))


SANTE = (sante1996, sante1988, sante2004)

	
def indexed_price(base,target,basePrice,**kw):
    baseMonth=Month.parse(str(base))
    targetMonth=Month.parse(str(target))
    for i in SANTE:
        if i.start <= baseMonth:
            return FixedPoint(
                basePrice * i.coeff(baseMonth,targetMonth),**kw)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
