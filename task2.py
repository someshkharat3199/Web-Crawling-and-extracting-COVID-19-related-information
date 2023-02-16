#reads the url and saves the html file
def remove_stop_words(doc):
    stop_words = set(stopwords.words('english'))
    
    word_tokens = word_tokenize(doc)
    filtered_doc = []
    for w in word_tokens: 
        is_valid = re.search(".*[a-zA-Z]+.*",w);
        if is_valid != None and not w.lower() in stop_words and w != "'s":
            filtered_doc.append(w.lower())
    return filtered_doc    

def find_top_common(common_words):
    count = {}
    for word in common_words:
        count[word] = count.get(word,0) + 1
    sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    return sorted_count 

def covid_common_words(common_words):
    covid_common = []
    for word in common_words:
        if word in covid_words:
            covid_common.append(word)
    return covid_common

def covid_words_per(common_words):
    covid_common_counts = dict(find_top_covid(common_words))
    total_words = len(common_words)
    covid_per = {}
    for word in covid_common_counts:
        covid_per[word] = (covid_common_counts[word] / total_words) * 100
    return covid_per

def find_top_covid(common_words):
    count = {}
    for word in common_words:
        if word in covid_words:
            count[word] = count.get(word,0) + 1
    sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    return sorted_count

def generate_word_cloud(doc,caption):
    stopwords = STOPWORDS
    wc = WordCloud(
        background_color = 'white',
        stopwords = stopwords,
        height = 600,
        width = 400
    )
    
    wc.generate(doc)
    plt.title(caption)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    
def jaccard(doc1, doc2): 
    words_doc1 = set(remove_stop_words(doc1)) 
    words_doc2 = set(remove_stop_words(doc2))
    intersection = words_doc1.intersection(words_doc2)
    union = words_doc1.union(words_doc2)
    return float(len(intersection)) / len(union)

def jaccard_covid(doc1, doc2): 
    words_doc1 = set([i for i in remove_stop_words(doc1) if i in covid_words]) 
    words_doc2 = set([i for i in remove_stop_words(doc2) if i in covid_words])
    intersection = words_doc1.intersection(words_doc2)
    union = words_doc1.union(words_doc2)
    return float(len(intersection)) / len(union)

def get_webpage(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode('UTF-8')
    return webpage

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


def clean_content(data):
    x = re.sub(r'<.*?>','', data)
    return re.sub(r'&#91;[0-9]+?&#93;|&#91;[&#160;a-zA-z\s]+?&#93;','',x) 

def get_world_links(start_date,end_date,link_data_set):
    if((not is_valid_date(start_date)) or (not is_valid_date(end_date))):
        return -1
    if(not is_valid_date_range(start_date,end_date)):
        return -2
    start_list = start_date.split('-')
    end_list = end_date.split('-')
    list_urls = []
    if start_list[2] == end_list[2]:
        if start_list[2] in link_data_set:
            if(start_list[2] == '2019'):
                link = link_data_set['2019']
                list_urls.append(link)
            else:
                for month in range(int(start_list[1])-1,int(end_list[1])):
                    if(month < len(link_data_set[start_list[2]])):
                            link = link_data_set[start_list[2]][month]
                            list_urls.append(link)
                
    else:
        month  = int(start_list[1])-1
        for year in range(int(start_list[2]),int(end_list[2])+1):
            if str(year) in link_data_set:
                if(str(year) == '2019'):
                    list_urls.append(link_data_set['2019'])
                    month = 0
                else:
                    while(month < 12 and month < len(link_data_set[str(year)])):
                        if(end_list[2] == str(year) and month >= int(end_list[1])):
                            break
                        year_links = link_data_set[str(year)]
                        list_urls.append(year_links[month])
                        month = month + 1
            month = 0
    
    return list_urls

def get_world_news_responses(start_date, end_date, link_data_set):
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    world_links = get_world_links(start_date, end_date, link_data_set)
    world_dict = {}
    if(world_links not in [-1,-2,-3]):
        start_list = start_date.split('-')
        end_list  = end_date.split('-')
        start_day = start_list[0]
        end_day = end_list[0]
        start_month = months[int(start_list[1])-1]
        end_month = months[int(end_list[1])-1]
        start_year = start_list[2]
        end_year = end_list[2]
        
        for link in world_links:
            year = re.search('[0-9]{4}',link).group()
            parser_out = parse_webpage5(link)
            for day_month in parser_out:
                match_obj = re.search('[0-9]{1,2}',day_month)
                if(match_obj != None):
                    day = int(match_obj.group())
                    if(year == start_year and re.search(start_month,day_month)):
                        if(day < int(start_day)):
                            continue
                    if(year == end_year and re.search(end_month,day_month)):
                        if(day > int(end_day)):
                            continue
                elif (year == start_year and months.index(day_month) < months.index(start_month)) or (year == end_year and months.index(day_month) > months.index(end_month)):
                    continue
                full_date = day_month + ' ' + year
                world_dict[full_date] = clean_content(parser_out[day_month])        
    else:
        return world_links
    return world_dict

def is_overlapping(date_range1, date_range2):
    start_date1 = date_range1[0].split('-')
    end_date1 = date_range1[1].split('-')
    start_date2 = date_range2[0].split('-')
    end_date2 = date_range2[1].split('-')
    start_obj1 = date(int(start_date1[2]),int(start_date1[1]),int(start_date1[0]))
    end_obj1 = date(int(end_date1[2]),int(end_date1[1]),int(end_date1[0]))
    start_obj2 = date(int(start_date2[2]),int(start_date2[1]),int(start_date2[0]))
    end_obj2 = date(int(end_date2[2]),int(end_date2[1]),int(end_date2[0]))

    return start_obj1 <= end_obj2 and start_obj2 <= end_obj1
    

#save data to file f_name
def save_to_file(data,f_name):
    fd = open(f_name,'w',encoding='utf-8')
    fd.write(data)
    fd.close
    
def get_world_newslinks():
    world_news = {}
    x = re.search("\"[^\"]+?\"", parser_out['world_news']['2019'])
    world_news['2019'] = main_url + x.group().strip('\"')
    for year in parser_out['world_news']:
        if(year != '2019'):
            world_news[year] = []
            for month in parser_out['world_news'][year]:
                not_exists = re.search("page does not exist",parser_out['world_news'][year][month])
                if(not_exists == None):
                    x = re.search("\"[^\"]+?\"", parser_out['world_news'][year][month])
                    world_news[year].insert(0,main_url + x.group().strip('\"'))
    return world_news

def get_world_responselinks():
    world_response = {}
    for year in parser_out['responses']:
        world_response[year] = []
        for month in parser_out['responses'][year]:
            not_exists = re.search("page does not exist",parser_out['responses'][year][month])
            if not_exists == None:
                x = re.search("\"[^\"]+?\"", parser_out['responses'][year][month])
                world_response[year].insert(0,main_url + x.group().strip('\"'))
    return world_response
            
def get_country_newslinks():
    country_news = {}
    for country in parser_out['country_news']:
        if(country in country_list):
            country_news[country] = {}
            if(len(parser_out['country_news'][country]) == 2):
                for other_links in parser_out['country_news'][country]['other']:
                    x = re.search(country, other_links)
                    if x:
                        not_exists = re.search("page does not exist",parser_out['country_news'][country]['other'][other_links])
                        if(not_exists == None):
                            dates = re.search("\([^\)]+?\)", other_links)
                            link = re.search("\"[^\"]+?\"",parser_out['country_news'][country]['other'][other_links])
                            country_news[country][dates.group().lstrip('(').rstrip(')')] = main_url + link.group().strip('\"')       
                if(len(country_news[country]) == 0):
                    not_exists = re.search("page does not exist",parser_out['country_news'][country]['main_link'])
                    if(not_exists == None):
                        link = re.search("\"[^\"]+?\"",parser_out['country_news'][country]['main_link'])
                        country_news[country] = main_url + link.group().strip('\"')
            else:
                not_exists = re.search("page does not exist",parser_out['country_news'][country])
                if not_exists == None:
                    link = re.search("\"[^\"]+?\"",parser_out['country_news'][country])
                    country_news[country] = main_url + link.group().strip('\"')
                    
    country_news['Ireland'] = {}
    for other_links in parser_out['country_news']['Ireland Republic of']['other']:
        not_exists = re.search("page does not exist",parser_out['country_news']['Ireland Republic of']['other'][other_links])
        if not_exists == None:
            dates = re.search("\([^\)]+?\)", other_links)
            link = re.search("\"[^\"]+?\"",parser_out['country_news']['Ireland Republic of']['other'][other_links])
            country_news['Ireland'][dates.group().lstrip('(').rstrip(')')] = main_url + link.group().strip('\"')
    return country_news

def clean_data(data):
    cleaned_data = {}
    for i in data:
        if type(data[i]) is dict:
            for j in data[i]:
                if cleaned_data.get(i) != None:
                    if data[i][j] != None:
                        clean_value = clean_content(data[i][j])
                        if clean_value != None and clean_value != '\n':
                            cleaned_data[i].update({j : clean_value})
                else:
                    if data[i][j] != None:
                        clean_value = clean_content(data[i][j])
                        if clean_value != None and clean_value != '\n':
                            cleaned_data[i] = {j : clean_value}
        else:
            clean_value = clean_content(data[i])
            if clean_value != None and clean_value != '\n':
                cleaned_data[i] = clean_value
    return cleaned_data

def canada_format_data(data, year):
    formatted_data = {}
    for i in data:
        x = re.search("[0-9]{4}", i) 
        y = re.search("January|February|March|April|May|June|July|August|September|October|November|December",i)  
        if x:
            year = x.group()  
        
        if formatted_data.get(year) == None:
            formatted_data[year] = {}
            
                
        if y:
            if formatted_data.get(year) != None:
                if formatted_data[year].get(y.group()) == None:
                    formatted_data[year][y.group()] = {}
            else:
                formatted_data[y.group()] = {}
                

        if type(data[i]) is not dict:
            lexer5 = lex.lex(module=tokrules_7)
            lexer5.input(str(data[i]))
            parser5 = yacc.yacc(module=tokrules_7,errorlog=yacc.NullLogger())
            parser_out = parser5.parse(data[i])
            data[i] = parser_out
            
        for j in data[i]:
            lexer5 = lex.lex(module=tokrules_7)
            lexer5.input(str(data[i][j]))
            parser5 = yacc.yacc(module=tokrules_7,errorlog=yacc.NullLogger())
            parser_out = parser5.parse(data[i][j])
            data[i][j] = parser_out
            for k in data[i][j]:
                if k != 'nodata':
                    x = re.search("[0-9]{1,2}", k)      
                    y = re.search("January|February|March|April|May|June|July|August|September|October|November|December",k)   
                    if(formatted_data[year].get(y.group()) == None and x == None):
                        formatted_data[year][y.group()] = {}
                        formatted_data[year][y.group()]['1'] = data[i][j]
                    else:
                        if(formatted_data[year].get(y.group()) == None):
                            formatted_data[year][y.group()] = {}
                        if x:
                            if(formatted_data[year][y.group()].get(x.group()) != None):
                                prev_data = formatted_data[year][y.group()][x.group()]
                                formatted_data[year][y.group()][x.group()] = prev_data + data[i][j][k]
                            else:    
                                formatted_data[year][y.group()][x.group()] = data[i][j][k]
                        else:
                            formatted_data[year][y.group()]['1'] = data[i][j][k]
                else:
                    formatted_data[year][y.group()]['1'] = data[i][j][k]
    return formatted_data

def format_data(data, year):
    formatted_data = {}
    for i in data:
        x = re.search("[0-9]{4}", i) 
        y = re.search("January|February|March|April|May|June|July|August|September|October|November|December",i)  
        if x:
            year = x.group()  
        
        if formatted_data.get(year) == None:
            formatted_data[year] = {}
            
                
        if y:
            if formatted_data.get(year) != None:
                if formatted_data[year].get(y.group()) == None:
                    formatted_data[year][y.group()] = {}
            else:
                formatted_data[y.group()] = {}
        
        
        if type(data[i]) is dict:
            new_data = ''
            for k in data[i]:
                date_format = re.search('(January|February|March|April|May|June|July|August|September|October|November|December)\s[0-9]{1,2}–[0-9]{1,2}',k)
                if date_format:
                    new_data = new_data + data[i][k]
            if new_data != '':
                data[i] = new_data
                

        if type(data[i]) is not dict:
            lexer5 = lex.lex(module=tokrules_7)
            lexer5.input(str(data[i]))
            parser5 = yacc.yacc(module=tokrules_7,errorlog=yacc.NullLogger())
            parser_out = parser5.parse(data[i])
            data[i] = parser_out
            
        for j in data[i]:
            if j != 'nodata':
                x = re.search("[0-9]{1,2}", j)      
                y = re.search("January|February|March|April|May|June|July|August|September|October|November|December",j)   
                if(formatted_data[year].get(y.group()) == None and x == None):
                    formatted_data[year][y.group()] = {}
                    formatted_data[year][y.group()]['1'] = data[i][j]
                else:
                    if(formatted_data[year].get(y.group()) == None):
                        formatted_data[year][y.group()] = {}
                    if x:    
                        if(formatted_data[year][y.group()].get(x.group()) != None):
                            prev_data = formatted_data[year][y.group()][x.group()]
                            formatted_data[year][y.group()][x.group()] = prev_data + data[i][j]
                        else:    
                            formatted_data[year][y.group()][x.group()] = data[i][j]
                    else:
                        formatted_data[year][y.group()]['1'] = data[i][j]
            else:
                formatted_data[year][y.group()]['1'] = data[i][j]
    return formatted_data

def get_date_range(country):
    country_links = country_news[country]
    if type(country_links) is not str:
        first_link = list(country_links.values())[0]
        last_link = list(country_links.values())[-1]
        start_year = re.search('[0-9]{4}',first_link).group()
        end_year = re.search('[0-9]{4}',last_link).group()
        parse_out1 = parse_webpage6(first_link)
        parse_out2 = parse_webpage6(last_link)
        formatted1 = format_data(parse_out1,start_year)
        formatted2 = format_data(parse_out2,end_year)
        start_month = list(formatted1[start_year].keys())[0]
        end_month = list(formatted2[end_year].keys())[-1]
        return start_month + ',' + start_year + '-' + end_month + ',' + end_year
    else:
        if country == 'Canada':
            year = '2019'
        else:
            year = '2020'
        parse_out = parse_webpage6(country_links)
        formatted = format_data(parse_out,year)
        start_year = list(formatted.keys())[0]
        end_year = list(formatted.keys())[-1]
        start_month = list(formatted[start_year].keys())[0]
        end_month = list(formatted[end_year].keys())[-1]
        return start_month + ',' + start_year + '-' + end_month + ',' + end_year

def get_country_news_data(country, start_date, end_date):
    country_data = {}
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    if(not is_valid_date(start_date) or not is_valid_date(end_date)):
        return -1
    if(not is_valid_date_range(start_date, end_date)):
        return -2
    start_list = start_date.split('-')
    end_list  = end_date.split('-')
    start_day = start_list[0]
    end_day = end_list[0]
    start_month = months[int(start_list[1])-1]
    end_month = months[int(end_list[1])-1]
    start_year = start_list[2]
    end_year = end_list[2]
    formatted_data = {}
    country_links = country_news[country]
    if type(country_links) is str:
        parser_out = parse_webpage6(country_links)
        cleaned_data = clean_data(parser_out)
        if country == 'Canada':
            year = '2019'
            formatted_data.update(canada_format_data(cleaned_data,year))
        else:
            year = '2020' 
            formatted_data.update(format_data(cleaned_data, year))
            
        for year in formatted_data:
            if int(year) >= int(start_year) and int(year) <= int(end_year):
                for month in formatted_data[year]:
                    if (year == start_year and months.index(month) < months.index(start_month)) or (year == end_year and months.index(month) > months.index(end_month)):
                            continue
                    for day in formatted_data[year][month]:
                        if(year == start_year and start_month == month):                    
                            if(int(day) < int(start_day)):
                                continue
                        if(year == end_year and end_month == month):
                            if(int(day) > int(end_day)):
                                continue   
                        full_date = day + ' ' + month + ' ' + year
                        country_data[full_date] = formatted_data[year][month][day]
            
    else:
        for link in country_links:
            year = re.search('[0-9]{4}',link).group()
            if int(year) >= int(start_year) and int(year) <= int(end_year):
                parser_out = parse_webpage6(country_links[link])
                cleaned_data = clean_data(parser_out)
                if formatted_data.get(year) == None:
                    formatted_data.update(format_data(cleaned_data, year))
                else:
                    prev_data = formatted_data[year]
                    formatted_data[year] = {**format_data(cleaned_data,year)[year],**prev_data}
        for year in reversed(list(formatted_data.keys())):
            for month in formatted_data[year]:
                if (year == start_year and months.index(month) < months.index(start_month)) or (year == end_year and months.index(month) > months.index(end_month)):
                        continue
                for day in formatted_data[year][month]:
                    if(year == start_year and start_month == month):                    
                        if(int(day) < int(start_day)):
                            continue
                    if(year == end_year and end_month == month):
                        if(int(day) > int(end_day)):
                            continue   
                    full_date = day + ' ' + month + ' ' + year
                    country_data[full_date] = formatted_data[year][month][day]
    return country_data
             

def parse_webpage3(link):
    webpage = get_webpage(link)
    lexer = lex.lex(module=tokrules_3)
    lexer.input(str(webpage))
    parser = yacc.yacc(module=tokrules_3,errorlog=yacc.NullLogger())
    parser_out = parser.parse(webpage)
    return parser_out

def parse_webpage4(link):
    webpage = get_webpage(link)
    lexer = lex.lex(module=tokrules_4)
    lexer.input(str(webpage))
    parser = yacc.yacc(module=tokrules_4,errorlog=yacc.NullLogger())
    parser_out = parser.parse(webpage)
    return parser_out

def parse_webpage5(link):
    webpage = get_webpage(link)
    lexer = lex.lex(module=tokrules_5)
    lexer.input(str(webpage))
    parser = yacc.yacc(module=tokrules_5,errorlog=yacc.NullLogger())
    parser_out = parser.parse(webpage)
    return parser_out

def parse_webpage6(link):
    webpage = get_webpage(link)
    lexer = lex.lex(module=tokrules_6)
    lexer.input(str(webpage))
    parser = yacc.yacc(module=tokrules_6,errorlog=yacc.NullLogger())
    parser_out = parser.parse(webpage)
    return parser_out

def parse_webpage7(link):
    webpage = get_webpage(link)
    lexer = lex.lex(module=tokrules_7)
    lexer.input(str(webpage))
    parser = yacc.yacc(module=tokrules_7,errorlog=yacc.NullLogger())
    parser_out = parser.parse(webpage)
    return parser_out


import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import tokrules_3, tokrules_4, tokrules_5, tokrules_6, tokrules_7
import ply.yacc as yacc
import ply.lex as lex   
from datetime import date
from urllib.request import Request, urlopen  

COVID_WORD_DICT = 'covid_word_dictionary.txt'
COVID_COUNTRY_LIST = 'covid_country_list.txt'

#fetch web page from below url
url = 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic'
main_url = 'https://en.wikipedia.org'


parser_out = parse_webpage3(url)

covid_words = []
fd = open(COVID_WORD_DICT,'r')
for i in fd:
    for j in i.split(' '):
        covid_words.append(j.strip('\n'))

country_list = []
fd3 = open(COVID_COUNTRY_LIST,'r')
for i in fd3:
    country_list.append(i.rstrip('\n'))

country_news = get_country_newslinks()


UK_anchor_tag = re.search("\"[^\"]+?\"",parser_out['country_news']['United Kingdom']['main_link'])
UK_url = main_url + UK_anchor_tag.group().strip('\"')

parser_out2 = parse_webpage4(UK_url)

country_news['England'] = {}
for other_links in parser_out2:
    dates = re.search("\([^\)]+?\)", other_links)
    link = re.search("\"[^\"]+?\"",parser_out2[other_links])
    country_news['England'][dates.group().lstrip('(').rstrip(')')] = main_url + link.group().strip('\"')
