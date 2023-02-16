tokens = [
    'DATE',
    'DATA'
]

def t_DATE(t):
    r'''[0-9]{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)
    |(On\s|By\s)?(January|February|March|April|May|June|July|August|September|October|November|December)\s[0-9]{1,2}[,]?
    |(On|As\sof|By)\s[0-9]{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)[,]?
    '''
    return t

def t_DATA(t):
    r'.+'
    t.value = t.value.strip(': ').strip('- ').strip('– ')
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
             '''
    t[0] = t[1]

def p_entries(t):
    '''entries : entries date data
               | date data
               '''
    if(len(t) == 3):
        t[0] = {t[1] : t[2]}
    else:
        if t[1] != None:
            if(t[1].get(t[2]) != None):
                prev_data = t[1][t[2]]
                t[1][t[2]] = prev_data + '\n' + t[3]
                t[0] = t[1]
            else:
                t[0] = {**t[1], **{t[2] : t[3]}}
        else:
            t[0] = {t[2]:t[3]}
            
def p_date(t):
    '''date : DATE
            | DATE DATE
            | 
            '''
    if(len(t) == 2):
        t[0] = t[1]
    elif(len(t) == 3):
        t[0] = t[1]
    else:
        t[0] = "nodata"

def p_data(t):
    '''data : DATA
            | DATA data
            '''
    if(len(t) == 2):
        t[0] = t[1]
    else:
        t[0] = t[1] + '\n' + t[2]
        
def p_error(t):
    # print(t,t.lineno)
    pass  