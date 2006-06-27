#coding: latin1

## Copyright 2006 Luc Saffre.
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

import sys
import os
import locale

from lino.console.application import Application, UsageError
from lino.reports.reports import DictReport
#from lino.gendoc.html import StaticHtmlDocument
from lino.gendoc.html import Document
from HyperText import HTML as html
#from HyperText.Documents import Document

def diag_encoding(ct):

    ct.header(2,"System Encodings")
    
    s="    locale.getdefaultlocale(): "\
       + repr(locale.getdefaultlocale())

    s+="\n    sys.getdefaultencoding() : "+ sys.getdefaultencoding()
    s+="\n    sys.getfilesystemencoding() : " + sys.getfilesystemencoding()
    s+="\n    sys.stdout.encoding : "
    try:
        s+=str(sys.stdout.encoding)
    except AttributeError:
        s+=("(undefined)")
    s+="\n    sys.stdin.encoding : "
    try:
        s+=str(sys.stdin.encoding)
    except AttributeError:
        s+="(undefined)"
    s+="\n    sys.getcheckinterval() : %r " % sys.getcheckinterval()
    s+="\n    sys.getwindowsversion() : %r " % (sys.getwindowsversion(),)
    
    
    s+="\n"
    ct.pre(s)

def diag_printer(story):
    try:
        import win32print
    except ImportError,e:
        story.par("No module win32print (%s)" % e)
        return

    printerName=win32print.GetDefaultPrinter()
    story.header(2,"Windows Default Printer (%s)" % printerName)
    h=win32print.OpenPrinter(printerName)
    d=win32print.GetPrinter(h,2)
    devmode=d['pDevMode']
    l=[ "%r\t%r\n" % (n,getattr(devmode,n))
        for n in dir(devmode)
        if n != 'DriverData' and n[0]!='_']
    ul=story.ul(*l)
    win32print.ClosePrinter(h)

class SysInfo(Application):
    name="Lino/SysInfo"
    copyright="""\
Copyright (c) 2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://lino.saffre-rumma.ee/sysinfo.html"
    
    usage="usage: lino sysinfo [options] [FILE]"
    
    description="""
    
Writes some diagnostics about your computer to FILE and starts your
browser to view the result.  'sysinfo.html' is default value for FILE.
The generated content is always in HTML, independantly of the
filename. If you specify the special filename "-", no file is created
and output is sent to stdout.

""" 
    
    def run(self):
        if len(self.args) == 0:
            filename="sysinfo.html" # self.toolkit.stdout
        elif len(self.args) == 1:
            filename=self.args[0]
        else:
            raise UsageError("Got more than 1 argument")

        self.notice("Generating %s ...",filename)
        doc=Document()
        #doc=StaticHtmlDocument()
        
        doc.body.header(1,"System Information")
        doc.body.par("This report has been generated by:")
        doc.body.pre(self.aboutString())
        diag_encoding(doc.body)
        
        diag_printer(doc.body)

        if False:
            doc.body.header(2,"sys.modules")
            doc.body.report(DictReport(sys.modules))
        if filename == "-":
            doc.__xml__(self.toolkit.console.stdout.write)
        else:
            doc.saveas(filename)
            os.system(filename)
        



SysInfo().main()

        

