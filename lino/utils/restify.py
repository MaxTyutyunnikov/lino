#coding: utf-8
"""
Just a copy & paste of the :mod:`docutils.examples` module (as instructed there).

:func:`restify` is an alias for :func:`html_body`.

:func:`latex_body` deduced from :func:`html_body`

"""

#~ import traceback
from docutils import core, io

def html_parts(input_string, source_path=None, destination_path=None,
               input_encoding='unicode', doctitle=1, initial_header_level=1):
    """
    Given an input string, returns a dictionary of HTML document parts.

    Dictionary keys are the names of parts, and values are Unicode strings;
    encoding is up to the client.

    Parameters:

    - `input_string`: A multi-line text string; required.
    - `source_path`: Path to the source file or object.  Optional, but useful
      for diagnostic output (system messages).
    - `destination_path`: Path to the file or object which will receive the
      output; optional.  Used for determining relative paths (stylesheets,
      source links, etc.).
    - `input_encoding`: The encoding of `input_string`.  If it is an encoded
      8-bit string, provide the correct encoding.  If it is a Unicode string,
      use "unicode", the default.
    - `doctitle`: Disable the promotion of a lone top-level section title to
      document title (and subsequent section title to document subtitle
      promotion); enabled by default.
    - `initial_header_level`: The initial level for header elements (e.g. 1
      for "<h1>").
    """
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}
    parts = core.publish_parts(
        source=input_string, source_path=source_path,
        destination_path=destination_path,
        writer_name='html', settings_overrides=overrides)
    return parts

def html_body(input_string, source_path=None, destination_path=None,
              input_encoding='unicode', output_encoding='unicode',
              doctitle=1, initial_header_level=1):
    """
    Given an input string, returns an HTML fragment as a string.

    The return value is the contents of the <body> element.

    Parameters (see `html_parts()` for the remainder):

    - `output_encoding`: The desired encoding of the output.  If a Unicode
      string is desired, use the default value of "unicode" .
    """
    parts = html_parts(
        input_string=input_string, source_path=source_path,
        destination_path=destination_path,
        input_encoding=input_encoding, doctitle=doctitle,
        initial_header_level=initial_header_level)
    fragment = parts['html_body']
    if output_encoding != 'unicode':
        fragment = fragment.encode(output_encoding)
    #~ print __file__, repr(fragment)
    return fragment


restify = html_body

def install_restify(renderer):
    """
    Install the `restify` function into the specified appy.pod renderer.
    This may break with later versions of appy.pod since 
    it hacks on undocumented regions... but we wanted to be 
    able to insert rst formatted plain text using a simple comment 
    like this::
    
      do text
        from restify(self.body)
        
    Without this hack, users would have to write each time something 
    like::
    
      do text
        from xhtml(restify(self.body).encode('utf-8'))
        
      do text
        from xhtml(restify(self.body,output_encoding='utf-8'))
    

    """
    def func(unicode_string,**kw):
        if not unicode_string:
            return ''
        html = restify(unicode_string,output_encoding='utf-8')
        #~ try:
            #~ html = restify(unicode_string,output_encoding='utf-8')
        #~ except Exception,e:
            #~ print unicode_string
            #~ traceback.print_exc(e)
        #~ print repr(html)
        assert html.startswith('<div class="document">\n')
        assert html.endswith('</div>\n')
        html = html[23:-7]
        #~ print repr(html)
        return renderer.renderXhtml(html,**kw)
        #~ return renderer.renderXhtml(html.encode('utf-8'),**kw)
    renderer.contentParser.env.context.update(restify=func)


def latex_parts(input_string, source_path=None, destination_path=None,
               input_encoding='unicode', doctitle=1, initial_header_level=1):
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}
    parts = core.publish_parts(
        source=input_string, source_path=source_path,
        destination_path=destination_path,
        #~ writer_name='latex2e', 
        writer_name='newlatex2e', 
        settings_overrides=overrides)
    return parts

def latex_body(input_string, source_path=None, destination_path=None,
              input_encoding='unicode', output_encoding='unicode',
              doctitle=1, initial_header_level=1):
    parts = latex_parts(
        input_string=input_string, source_path=source_path,
        destination_path=destination_path,
        input_encoding=input_encoding, doctitle=doctitle,
        initial_header_level=initial_header_level)
    #~ print parts.keys()
    fragment = parts['body']
    if output_encoding != 'unicode':
        fragment = fragment.encode(output_encoding)
    return fragment
    
def rst2latex(input_string, 
              source_path=None, 
              input_encoding='unicode',
              doctitle=1, 
              initial_header_level=1):
    """
    returns a dict containing the following keys::
    
      'body', 
      'latex_preamble', 
      'head_prefix', 
      'requirements', 
      'encoding', 
      'abstract', 
      'title', 
      'fallbacks', 
      'stylesheet', 
      'version', 
      'body_pre_docinfo', 
      'dedication', 
      'subtitle', 
      'whole', 
      'docinfo', 
      'pdfsetup'

    """
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}
    #~ doc = core.publish_doctree(source=input_string, 
                #~ source_path=source_path,
                #~ 'input_encoding': input_encoding)
    
    parts = core.publish_parts(source=input_string, 
        source_path=source_path,
        #~ writer_name='latex2e', 
        writer_name='latex2e', 
        settings_overrides=overrides)
    return parts
    #~ print parts.keys()
    #~ f = file('tmp.txt','w')
    #~ f.write(repr(parts.keys())+'\n\n')
    #~ f.write(repr(parts))
    #~ f.close()
    #~ return parts['body']
    
    
  


if __name__ == '__main__':
    test = u"""
Test example of reST__ document
containg non-ascii latin-1 chars::

  Ä Ë Ï Ö Ü 
  ä ë ï ö ü ÿ
  à è ì ò ù 
  á é í ó ú
  ã õ ñ 
  ç ß 

__ http://docutils.sf.net/rst.html

A list:

  - item 1
  - item 2
  - item 3


"""
    print restify(test)
    #~ print latex_body(test)



