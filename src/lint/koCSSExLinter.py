#!python
# Copyright (c) 2000-2011 ActiveState Software Inc.
# See the file LICENSE.txt for licensing information.

# Use the silvercity tokenizer and parse text here
# Support for SCSS (CSS-like Sass) and Less as well.

from koLintResult import createAddResult, SEV_ERROR, SEV_WARNING, SEV_INFO, KoLintResult
from koLintResults import koLintResults
import logging
from xpcom import components, nsError, COMException
from codeintel2.css_linter import CSSLinter

log = logging.getLogger("koCSSLinter")
#log.setLevel(logging.DEBUG)

class KoCSSLinter(object):
    _com_interfaces_ = [components.interfaces.koILinter,
                        components.interfaces.nsIConsoleListener]
    _reg_desc_ = "Komodo CSS Linter"
    _reg_clsid_ = "{ded22115-148a-4a2f-aef1-2ae7e12395b0}"
    _reg_contractid_ = "@activestate.com/koLinter?language=CSS;1"
    _reg_categories_ = [
         ("category-komodo-linter", 'CSS'),
         ("category-komodo-linter", 'SCSS'),
         ("category-komodo-linter", 'Less'),
         ]

    """
    This class is mostly a parser.
    """
    
    def lint(self, request):
        """Lint the given CSS content.
        
        Raise an exception  if there is a problem.
        """
        text = request.content.encode(request.encoding.python_encoding_name)
        return self.lint_with_text(request, text)

    def lint_with_text(self, request, text):
        textlines = text.splitlines()
        results = CSSLinter().lint(text)
        lintResults = koLintResults()
        for r in results:
            if r.line_start is None:
                lastLine = textlines
                createAddResult(lintResults, textlines, r.status + 1,
                                len(textlines) - 1,
                                r.message);
            else:
                result = KoLintResult(description=r.message,
                                      severity=r.status + 1,
                                      lineStart=r.line_start,
                                      lineEnd=r.line_end,
                                      columnStart=r.col_start,
                                      columnEnd=r.col_end)
                lintResults.addResult(result)
        return lintResults
                
            
        

