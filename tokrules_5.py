tokens = [
    'START',
    'END',
    'SEP1',
    'SEP2',
    'DIV',
    'STYLE',
    'SPAN',
    'DATA',
    'LUL',
    'RUL',
    'DATE',
    'H3'
]

def t_START(t):
    r'<!DOCTYPE\shtml>[\S\s]+?class="mw-headline"\sid="[0-9]{,2}[_]?(January|February|March|April|May|June|July|August|September|October|November|December)[_]?[0-9]{,2}">'
    
def t_END(t):
    r'<h2><span\sclass="mw-headline"\sid="Summary">Summary[\S\s]+?</html>|<h2><span\sclass="mw-headline"\sid="See_also">See\salso[\S\s]+?</html>'


def t_SEP1(t):
    r'</span>[\S\s]*?</h[23]>'

def t_SEP2(t):
    r'<h[23]><span\sclass="mw-headline"[^>]+>'

def t_DIV(t):
    r'<div[^>]*?><div[^>]*?>[\S\s]*?<div[^>]*?>[\S\s]*?</div></div></div>|<div[\S\s]+?</div>|<link[\S\s]+?/>'
    
def t_STYLE(t):
    r'<style[\S\s]+?</style>'
    
def t_SPAN(t):
    r'<span[\S\s]+?</span>'
    
def t_H3(t):
    r'<h2[\S\s]+?</h2>|<h3[\S\s]+?</h3>|<h4[\S\s]+?</h4>'

def t_LUL(t):
    r'<ul>|<dl>'

def t_RUL(t):
    r'</ul>|</dl>'
    
def t_DATA(t):
    r'<p>[\S\s]+?</p>|<li[\S\s]+?</li>|<dd>[\S\s]+?</dd>'
    return t

def t_DATE(t):
    r'[0-9]{,2}\s?(January|February|March|April|May|June|July|August|September|October|November|December)\s?[0-9]{,2}'
    return t

t_ignore = ' \t'

def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
     
def t_error(t):
    t.lexer.skip(1)
    
#grammar rules

def p_start(t):
    'start : entries'
    t[0] = t[1]

def p_entries(t):
    '''entries : DATE data
               | DATE data entries
               '''
    if(len(t) == 3):
        t[0] = {t[1] : t[2]}
    else:
        if(t[3] != None):
            prev = t[3].get(t[1],'')
            if(prev != ''):
                val = prev  + t[2]
                t[3][t[1]] = val
                t[0] = t[3]
            else:
                t[0] = {**{t[1]:t[2]},**t[3]}
        else:
            t[0] = {t[1]:t[2]}

def p_data(t):
    '''data : DATA
            | DATA data'''
    if(len(t) == 2):
        t[0] = t[1]
    else:
        t[0] = t[1] + '\n' + t[2]
    
def p_error(t):
    # print(t,t.lineno)
    pass  