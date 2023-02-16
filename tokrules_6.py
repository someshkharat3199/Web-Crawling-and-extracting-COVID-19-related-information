tokens = [
    'START',
    'END',
    'SEP1',
    'SEP2',
    'DIV',
    'STYLE',
    'SPAN',
    'LUL',
    'RUL',
    'DATA',
    'DATE',
    'H3'
]

def t_START(t):
    r'''<!DOCTYPE\shtml>[\S\s]+?class="mw-headline"\sid="[0-9]{,4}[_]?(January|February|March|April|May|June|July|August|September|October|November|December)[^"]*?">
    |<!DOCTYPE\shtml>[\S\s]+?class="mw-headline"\sid="[0-9]{4}">
    '''
    
def t_END(t):
    r'<h2><span\sclass="mw-headline"\sid="(Alert_levels_timeline|See_also|Notes|References)">(Alert\slevels\stimeline|See\salso|Notes|References)[\S\s]+?</html>'
    

def t_SEP1(t):
    r'</span>[\S\s]*?</h[234]>'
    

def t_SEP2(t):
    r'''<h[234]><span\sclass="mw-headline"\sid="[0-9]{4}">|
    <h[234]><span\sclass="mw-headline"\sid="[0-9]{,4}[_]?(January|February|March|April|May|June|July|August|September|October|November|December)[^"]*?">
    |<h[234]><span[^>]*?></span><span\sclass="mw-headline"\sid="(January|February|March|April|May|June|July|August|September|October|November|December)_[0-9]{1,2}–[0-9]{1,2}">
    '''
    

def t_DIV(t):
    r'<div[^>]*?><div[^>]*?>[\S\s]*?<div[^>]*?>[\S\s]*?</div></div></div>|<div[\S\s]+?</div>|<table[\S\s]+?</table>|<link[\S\s]+?/>|<i>[\S\s]*?</i>'

    
def t_STYLE(t):
    r'<style[\S\s]+?</style>'
    
    
def t_SPAN(t):
    r'<span[\S\s]+?</span>'
    
    
def t_H3(t):
    r'<h2[\S\s]+?</h2>|<h3[\S\s]+?</h3>|<h4[\S\s]+?</h4>'
    

def t_LUL(t):
    r'<ul>'
    

def t_RUL(t):
    r'</ul>'

def t_DATE(t):
    r'''(January|February|March|April|May|June|July|August|September|October|November|December)\s[0-9]{1,2}–[0-9]{1,2}[,]?[\s]?[0-9]{,4}
    |(January|February|March|April|May|June|July|August|September|October|November|December)–(January|February|March|April|May|June|July|August|September|October|November|December)\s[0-9]{4}
    |(January|February|March|April|May|June|July|August|September|October|November|December)\s[0-9]{,3}\sto\s[0-9]{,3}
    |(<p><b>)?[0-9]{,4}\s?(January|February|March|April|May|June|July|August|September|October|November|December)\s?[0-9]{,4}(</b></p>)?
    |[0-9]{4}
    '''
    t.value = t.value.lstrip('<p><b>').rstrip('</p></b>')
    return t

def t_DATA(t):
    r'<p>[\S\s]+?</p>|<li[\S\s]+?</li>'
    return t

t_ignore = ' \t'

def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
     
def t_error(t):
    t.lexer.skip(1)
    
#grammar rules

def p_start(t):
    '''start : entries
             | subentries
             | subentries entries
             | entries subentries
             '''
    if(len(t) == 3):
        t[0] = {**t[1],**t[2]}
    else:
        t[0] = t[1]
    
def p_entries(t):
    '''entries : DATE subentries
               | DATE subentries entries
               '''
    if(len(t) == 3):
        t[0] = {t[1] : t[2]}
    else:
        if(t[3] != None):
            t[0] = {**{t[1]:t[2]},**t[3]}
        else:
            t[0] = {t[1]:t[2]}

def p_subentries(t):
    '''subentries : subentries DATE data
                  | DATE data
                  '''
    if(len(t) == 3):
        t[0] = {t[1] : t[2]}
    if(len(t) == 4):
        if(t[1] != None):
            t[0] = {**t[1],**{t[2]:t[3]}}
        else:
            t[0] = {t[2]:t[3]}

def p_data(t):
    '''data : DATA data
            |
            '''
    if(len(t) == 3):
        if(t[2] != None):
            t[0] = t[1] + '\n' + t[2]
        else:
            t[0] = t[1]
    
def p_error(t):
    # print(t,t.lineno)
    pass  