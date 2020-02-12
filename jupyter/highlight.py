import json

from pygments import formatters, lexers, highlight, styles
from pygson.json_lexer import JSONLexer
from IPython.core.display import HTML, display

def pprint(code, lexer=None, style='solarized-dark'):
    " Pretty print some code using a given Pyments lexer."    
    # Load stylesheet for pygments
    allowed = set(styles.get_all_styles())
    if not style in allowed:
        raise ValueError(f'Style {style} not in list of known styles ({allowed})')
    
    # Load language lexer
    try:
        lexer = getattr(lexers, lexer or 'JavascriptLexer')
    except AttributeError:
        if lexer == 'JSONLexer':
            lexer = JSONLexer
        else:
            raise ValueError(f'Unknonwn lexer {lexer} - is this in `pygments.lexers`?')
    
    # Generate and return HTML for display
    formatter = formatters.HtmlFormatter(style=style)
    css = formatter.get_style_defs('.highlight')
    html = f"<style>{css}</style>" + highlight(code, lexer(), formatter)
    display(HTML(html))
    
def pjson(obj, **kwargs):
    "Print an object as a JSON string."
    pprint(json.dumps(obj, indent=4), lexer='JSONLexer', **kwargs)
