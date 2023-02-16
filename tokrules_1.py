
tokens = [
    'LTABLE',
    'RTABLE',
    'THEAD',
    'LTBODY',
    'RTBODY',
    'LTROW',
    'RTROW',
    'LTDATA',
    'RTDATA',
    'CONTRYLINK',
    'POPULNLINK',
    'LINKEND',
    'LNOBR',
    'RNOBR',
    'LSPAN',
    'RSPAN',
    'CONTENT'
]

def t_LTABLE(t):
    r'<!DOCTYPE\shtml>[\S\s]+<table\sid="main_table_countries_yesterday"\s[^>]*>'
    return t

def t_RTABLE(t):
    r'<tbody\sclass="body_continents">[\S\s]+</html>'
    return t

def t_THEAD(t):
    r'<thead>[\S\s]+?</thead>'
    return t

def t_LTBODY(t):
    r'<tbody>'
    return t

def t_RTBODY(t):
    r'</tbody>'
    return t

def t_LTROW(t):
    r'<tr\s[^>]*>'
    return t

def t_RTROW(t):
    r'</tr>'
    return t

def t_LTDATA(t):
    r'<td[^>]*>'
    return t

def t_RTDATA(t):
    r'</td>'
    return t

def t_CONTRYLINK(t):
    r'<a\sclass="mt_a"\shref="country/[^>]*>'
    return t

def t_POPULNLINK(t):
    r'<a\shref="/world-population/[^>]*>'
    return t
    
def t_LINKEND(t):
    r'</a>'
    return t
    
def t_LNOBR(t):
    r'<nobr>'
    return t
    
def t_RNOBR(t):
    r'</nobr>'
    return t

def t_LSPAN(t):
    r'<span\s[^>]*>'
    return t

def t_RSPAN(t):
    r'</span>'
    return t
    
def t_CONTENT(t):
    r'[A-Za-z0-9/,.+]+'
    return t

t_ignore = ' \t'

def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
     
def t_error(t):
    t.lexer.skip(1)
    

#Grammar rules

def p_start(t):
    'start : table'
    t[0] = t[1]

def p_table(t):
    'table : LTABLE THEAD ptbody RTABLE'
    t[0] = t[3]
    
def p_ptbody(t):
    'ptbody : LTBODY prow RTBODY'
    t[0] = t[2]
    
def p_prow(t):
    '''prow : LTROW ptdata RTROW
            | LTROW ptdata RTROW prow
            '''
    if(len(t)==4):
        t[0] = t[2]
        
    if(len(t) == 5):
        t[0] = t[2]  + '\n' + t[4]

def p_ptdata(t):
    '''ptdata : LTDATA pcontent RTDATA
              | LTDATA pcontent RTDATA ptdata
              | LTDATA LNOBR pcontent RNOBR RTDATA
              | LTDATA LNOBR pcontent RNOBR RTDATA ptdata
              '''
    if(len(t) == 4):
        t[0] = t[2]
    if(len(t) == 5):
        t[0] = t[2] + '|' + t[4]
    if(len(t) == 6):
        t[0] = t[3]
    if(len(t) == 7):
        t[0] = t[3] + '|' + t[6]
        

def p_population_ptdata(t):
    '''ptdata : LTDATA POPULNLINK pcontent LINKEND RTDATA
              | LTDATA POPULNLINK pcontent LINKEND RTDATA ptdata
              '''
    if(len(t) == 6):
        t[0] = t[3]
    if(len(t) == 7):
        t[0] = t[3] + '|' + t[6]

def p_countrylink_ptdata(t):
    '''ptdata : LTDATA CONTRYLINK pcontent LINKEND RTDATA
              | LTDATA CONTRYLINK pcontent LINKEND RTDATA ptdata
              '''
    if(len(t) == 6):
        t[0] = t[3] + '|' + t[2][29:-3] 
    if(len(t) == 7):
        t[0] = t[3] + '|' + t[2][29:-3] + '|' + t[6]
        
def p_span_ptdata(t):
    '''ptdata : LTDATA LSPAN pcontent RSPAN RTDATA
              | LTDATA LSPAN pcontent RSPAN RTDATA ptdata
              '''
    if(len(t) == 6):
        t[0] = t[3]
    if(len(t) == 7):
        t[0] = t[3] + '|' + t[6]
    
def p_nodata_ptdata(t):
    '''ptdata : LTDATA RTDATA ptdata
              | LTDATA RTDATA
              | LTDATA LNOBR RNOBR RTDATA
              | LTDATA LNOBR RNOBR RTDATA ptdata
              '''
    if(len(t) == 4):
        t[0] = '-1' + '|' + t[3]
    if(len(t) == 3):
        t[0] = '-1'
    if(len(t) == 5):
        t[0] = '-1'
    if(len(t) == 6):
        t[0] = '-1' + '|' + t[5]

def p_pcontent(t):
    '''pcontent : CONTENT
                | CONTENT pcontent
                '''
    if(len(t) == 2):
        t[0] = t[1]
    if(len(t) == 3):
        t[0] = t[1] + ' ' + t[2]

def p_error(t):
    # print(t)
    pass        
