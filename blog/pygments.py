# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = False

import re

from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer


class CodeBlockPreprocessor(Preprocessor):

    pattern = re.compile(r'\[sourcecode:(.+?)\](.+?)\[/sourcecode\]', re.S)

    formatter = HtmlFormatter(noclasses=INLINESTYLES)

    def run(self, lines):
        def repl(m):
            try:
                lexer = get_lexer_by_name(m.group(1))
            except ValueError:
                lexer = TextLexer()
            code = highlight(m.group(2), lexer, self.formatter)
            code = code.replace('\n\n', '\n&nbsp;\n').replace('\n', '<br />')
            return '\n\n<div class="code">%s</div>\n\n' % code
        joined_lines = "\n".join(lines)
        joined_lines = self.pattern.sub(repl, joined_lines)
        return joined_lines.split("\n")

class CodeBlockExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('CodeBlockPreprocessor', CodeBlockPreprocessor(), '_begin')


