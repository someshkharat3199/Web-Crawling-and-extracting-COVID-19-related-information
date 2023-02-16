#reads the url and saves the html file
def get_webpage(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode('UTF-8')
    return webpage

#save data to file f_name
def save_to_file(data,f_name):
    fd = open(f_name,'w')
    fd.write(data)
    fd.close

def get_percent_details(data):
    if(data == None):
        return None
    world_data = get_summary_details('World')
    percent_details = {}
    percent_details['name'] = data['name']
    if(data['total cases'] == -1 or world_data['total cases'] == -1):
        percent_details['total cases'] = 'N/A'
    else:
        percent_details['total cases'] = '{:.4f}%'.format((data['total cases']/world_data['total cases'])*100)
    if(data['active cases'] == -1 or world_data['active cases'] == -1):
        percent_details['active cases'] = 'N/A'
    else:
        percent_details['active cases'] = '{:.4f}%'.format((data['active cases']/world_data['active cases'])*100)
    if(data['total deaths'] == -1 or world_data['total deaths'] == -1):
        percent_details['total deaths'] = 'N/A'
    else:
        percent_details['total deaths'] = '{:.4f}%'.format((data['total deaths']/world_data['total deaths'])*100)
    if(data['total recovered'] == -1 or world_data['total recovered'] == -1):
        percent_details['total recovered'] = 'N/A'
    else:
        percent_details['total recovered'] = '{:.4f}%'.format((data['total recovered']/world_data['total recovered'])*100)
    if(data['total tests'] == -1 or world_data['total tests'] == -1):
        percent_details['total tests'] = 'N/A'
    else:
        percent_details['total tests'] = '{:.4f}%'.format((data['total tests']/world_data['total tests'])*100)
    if(data['tests/million'] == -1 or world_data['tests/million'] == -1):
        percent_details['tests/million'] = 'N/A'
    else:
        percent_details['tests/million'] = '{:.4f}%'.format((data['tests/million']/world_data['tests/million'])*100)
    if(data['new cases'] == -1 or world_data['new cases'] == -1):
        percent_details['new cases'] = 'N/A'
    else:
        percent_details['new cases'] = '{:.4f}%'.format((data['new cases']/world_data['new cases'])*100)
    if(data['new death'] == -1 or world_data['new death'] == -1):
        percent_details['new death'] = 'N/A'
    else:
        percent_details['new death'] = '{:.4f}%'.format((data['new death']/world_data['new death'])*100)
    if(data['new recovered'] == -1 or world_data['new recovered'] == -1):
        percent_details['new recovered'] = 'N/A'
    else:
        percent_details['new recovered'] = '{:.4f}%'.format((data['new recovered']/world_data['new recovered'])*100)    
      
    if(data['death/million'] == -1 or world_data['death/million'] == -1):
        percent_details['death/million'] = 'N/A'
    else:
        percent_details['death/million']= '{:.4f}%'.format((data['death/million']/world_data['death/million'])*100)
    return percent_details

def get_summary_details(name):
    if(name not in [*country_list,*continent_list,'World']):
        return None
    data = summary_data_dict[name]
    is_country = 0        
    if(data[1] in country_list):
        is_country = 1 
    details = {
        'name':              data[1], 
        'total cases':       int(data[2+is_country].replace(',','')),
        'active cases':      int(data[8+is_country].replace(',','')),
        'total deaths':      int(data[4+is_country].replace(',','')),
        'total recovered':   int(data[6+is_country].replace(',','')),
        'total tests':       int(data[12+is_country].replace(',','')),
        'death/million':     float(data[11+is_country].replace(',','')),
        'tests/million':     float(data[13+is_country].replace(',','')),
        'new cases':         int(data[3+is_country].replace(',','')),
        'new death':         int(data[5+is_country].replace(',','')),
        'new recovered':     int(data[7+is_country].replace(',',''))
    }    
    return details
    

#get dictionary of continents from file f_name    
def get_country_continent_list(f_name):
    fd = open(f_name,'r')
    country_list = {}
    prev_key = ''
    for line in fd:
        x = re.search("^[a-zA-Z].*:$", line)
        if(x):
            country_list[line.rstrip(':\n')] = list()
            prev_key = line.rstrip(':\n')
        x = re.search("^[a-zA-Z].*[a-zA-Z]$",line)
        if(x):
            country_list[prev_key].append(line.rstrip('\n'))
    return country_list

def is_valid_date(ip_date):
    list_date = ip_date.split('-')
    if(len(list_date) != 3):
        return False
    try:
        date_obj = date(int(list_date[2]),int(list_date[1]),int(list_date[0]))
    except Exception:
        return False
    
    today = date.today()
    min_date = date(1800,1,1)
    
    if(date_obj > today or date_obj < min_date):
        return False
    
    return True

def convert_format(ip_date):   
    #input date format 3 Jan 1999 
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    list_date = ip_date.split('-')
    parsed_date = months[int(list_date[1])-1] + ' ' + list_date[0].zfill(2).strip(' ') + ',' + ' ' + list_date[2].strip(' ')
    return parsed_date
    
def is_valid_date_range(start_date, end_date):
    start_list = start_date.split('-')
    end_list = end_date.split('-')
    start_obj = date(int(start_list[2]),int(start_list[1]),int(start_list[0]))
    end_obj = date(int(end_list[2]),int(end_list[1]),int(end_list[0]))
    if(start_obj > end_obj):
        return False
    return True

def add_log_entry(entry):
    fd = open(LOG_FILE,"a")
    fd.write(entry)

def perform_query(country, start_date, end_date, query_type):
    #perform necessary checks
    if(country not in country_list):
        print("Error: country not available in list")
        return -1
    if(not is_valid_date(start_date) or not is_valid_date(end_date)):
        print("Error: start date or end date is not valid")
        return -1
    if(not is_valid_date_range(start_date, end_date)):
        print("Error: dates are not specified in valid range")
        return -1
    start = convert_format(start_date)
    end = convert_format(end_date)

    daily_data = countries_data[country][query_type]
    if(len(daily_data['dates']) == 0 or len(daily_data['data']) == 0):
        return -2
    try:
        start_idx = daily_data['dates'].index(start)
        end_idx = daily_data['dates'].index(end)
    except Exception:
        return -3
    start_value = daily_data['data'][start_idx]
    end_value = daily_data['data'][end_idx]
    if(start_value == 'null' or end_value == 'null'):
        return -4  
    start_value = int(start_value)
    end_value = int(end_value)
    if(start_value == 0):
        #apply smoothing
        percentage_change =  ((end_value - start_value + SMOOTING_FACTOR)/(start_value + SMOOTING_FACTOR))
        return percentage_change
    
    percentage_change = ((end_value - start_value)/start_value)*100
    return percentage_change
    
def closest_country(country, start_date, end_date, query_type):
    country_pchange = perform_query(country,start_date,end_date,query_type)
    if(country_pchange in [-1,-2,-3,-4]):
        return []
    closest_countries = []
    for c in country_list:
        if(c != country):
            pchange = perform_query(c,start_date,end_date,query_type)
            if(pchange >= (country_pchange - LMARGIN) and pchange <= (country_pchange + RMARGIN)):
                closest_countries.append([c,pchange])
    return closest_countries


import os
import re
import sys
import ply.lex as lex   
from datetime import date
from urllib.request import Request, urlopen
import os 

#constants
LMARGIN = 5
RMARGIN = 5
SMOOTING_FACTOR = 0.0001
COUNTRY_LIST_FILE = 'worldometers_countrylist.txt'
LOG_FILE = 'query_logs.txt'

#get clontinent_list and country list
country_continent_dict = get_country_continent_list(COUNTRY_LIST_FILE)
continent_list = list(country_continent_dict.keys())
country_list = [j for i in list(country_continent_dict.values()) for j in i]

print("Loading data")

#fetch web page from below url
url = 'https://www.worldometers.info/coronavirus/'
webpage = get_webpage(url)

#define lexer
import tokrules_1
lexer = lex.lex(module=tokrules_1)
lexer.input(webpage)

#define parser
import ply.yacc as yacc
parser = yacc.yacc(module=tokrules_1,errorlog=yacc.NullLogger())
parser_out = parser.parse(str(webpage))

#create the list of data extracted
table_data = []
tmp_list = []
tmp_list.extend(parser_out.split('\n'))
table_data.extend([i.split('|') for i in tmp_list])

#add country links to the list and create dictionary of data indexed by name of country or continent
summary_data_dict = {}
for i in table_data:
    if(i[1] in country_list):
        i[2] = url+'country'+i[2]
        summary_data_dict[i[1]] = i
    if(i[1] in continent_list or i[1] == 'World'):
        summary_data_dict[i[1]] = i


#fetch all countries data
import tokrules_2
countries_data = {}
lexer2 = lex.lex(module=tokrules_2)
parser2 = yacc.yacc(module=tokrules_2,errorlog=yacc.NullLogger())
for country in country_list:
    url = summary_data_dict.get(country)[2]
    webpage = get_webpage(url)
    lexer2.input(webpage)
    parser_out2 = parser2.parse(str(webpage))
    countries_data[country] = parser_out2
