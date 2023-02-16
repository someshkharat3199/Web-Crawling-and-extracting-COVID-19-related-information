import os 
import task1 as t1
import task2 as t2
CLEAR = 'cls'
while(1):
    print('''
    ***** TASK-1 *****
    1. Total cases
    2. Active cases
    3. Total deaths
    4. Total recovered
    5. Total tests
    6. Death/million
    7. Tests/million
    8. New case
    9. New death
    10. New recovered
    11. Change in active cases in %
    12. Change in daily death in %
    13. Change in new recovered in %
    14. Change in new cases in %
    
    ***** TASK-2 *****
    15. Show all the worldwide news between the given time range.
    16. Show all the worldwide responses between the given time range  
    17. Plot two different word clouds for all the common words and only covid related common words.
    18. Find the percentage of covid related words in common words.
    19. Find the top-20 common words and covid related words.
    20. Find date range of available news information for given country
    21. Find all the news between the time duration, for given country and plot a word cloud.
    22. Exit
          ''')
    while(1):
        try:
            choice = int(input("enter your choice: "))
            break
        except Exception:
            print("Please enter integer choice [1-15]")
        
    if(choice in range(1,11)):
        indexes = ['total cases','active cases','total deaths','total recovered','total tests',
           'death/million','tests/million','new cases','new death','new recovered']
        query = input('Enter name of country/Continent or fetch for all (World):')
        details = t1.get_summary_details(query)
        per_details= t1.get_percent_details(details)
        if(details == None):
            print("{} country/continent not present".format(query))
        elif(details[indexes[choice-1]] == -1):
            print("{} for {} : N/A".format(indexes[choice-1],query))
            t1.add_log_entry('{} {} {}\n'.format(query,indexes[choice-1],'N/A'))
        else:
            print("{} for {} : {}\npercent of total world cases: {}".format(indexes[choice-1],query,details[indexes[choice-1]],per_details[indexes[choice-1]]))
            t1.add_log_entry('{} {} {:.4f}\n'.format(query,indexes[choice-1],details[indexes[choice-1]]))
        
    elif(choice in range(11,15)):
        indexes = ['active','death','recovery','new']
        country = input("enter name of country: ")
        start_date = input("Enter starte date (dd-mm-yyyy): ")
        end_date = input("Enter end date (dd-mm-yyyy): ")
        result = t1.perform_query(country,start_date,end_date,indexes[choice-11])
        if(result == -2):
            print('Error: {} cases data not available for {}'.format(indexes[choice-11],country))
        elif(result == -3):
            print("Error: specified dates not present")
        elif(result == -4):
            print("Error: start or end value not available")
        elif(result != -1):
            if(result < 0):
                print('percentage change in daily {} cases of {}: {:.4f}% decrease'.format(indexes[choice-11],country,-result))
                t1.add_log_entry('{} daily {} cases {:.4f}\n'.format(country,indexes[choice-11],-result))
            else:
                print('percentage change in daily {} cases of {}: {:.4f}% increase'.format(indexes[choice-11],country,result))
                t1.add_log_entry('{} daily {} cases {:.4f}\n'.format(country,indexes[choice-11],result))
            print("Want list of countries with similar percent change in {} cases? (Enter Yes/No) ".format(indexes[choice-11]))
            while(1):
                followup = input()
                if(followup == 'Yes'):
                    closest = t1.closest_country(country,start_date,end_date,indexes[choice-11])
                    print("list of closest countries: ")
                    if(len(closest) > 0):
                        for k in closest:
                            if(k[1] < 0):
                                print('country: {} percent change: {:.4f}% decrease'.format(k[0],-k[1]))
                            else:
                                print('country: {} percent change: {:.4f}% increase'.format(k[0],k[1]))
                    else:
                        print("No closest country found")
                    break
                elif(followup == 'No'):
                    break
                print("Enter appropriate input (Yes/No) Please try again!")   
    
    elif(choice == 15):
        while(1):
            time_range = input("Enter time range (dd-mm-yyyy,dd-mm-yyyy): ").split(',')
            if len(time_range) != 2:
                print('Please provide correct number of arguments')
            elif not t2.is_valid_date(time_range[0]) or not t2.is_valid_date(time_range[1]):
                print('Dates are not valid')
            elif not t2.is_valid_date_range(time_range[0],time_range[1]):
                print('date range in not valid')
            else:    
                world_news = t2.get_world_news_responses(time_range[0],time_range[1],t2.get_world_newslinks())
                document = ''
                for date in world_news:
                    print('{}\n{}\n\n'.format(date,world_news[date]))
                    document = document + date + world_news[date]
                if(len(document) == 0):
                    print("No data available")
                else:
                    t2.generate_word_cloud(document,"Word cloud for World News")
                break
    elif(choice == 16):
        while(1):
            time_range = input("Enter time range (dd-mm-yyyy,dd-mm-yyyy): ").split(',')
            if len(time_range) != 2:
                print('Please provide correct number of arguments')
            elif not t2.is_valid_date(time_range[0]) or not t2.is_valid_date(time_range[1]):
                print('Dates are not valid')
            elif not t2.is_valid_date_range(time_range[0],time_range[1]):
                print('date range in not valid')
            else:    
                world_responses = t2.get_world_news_responses(time_range[0],time_range[1],t2.get_world_responselinks())
                document = ''
                for date in world_responses:
                    print('{}\n{}\n\n'.format(date,world_responses[date]))
                    document = document + date + world_responses[date]
                if(len(document) == 0):
                    print("No data available")
                else:
                    t2.generate_word_cloud(document,"Word cloud for world responses")
                break
    
    elif(choice == 17):
        while(1):
            time_range1 = input("Enter first timerange (dd-mm-yyyy,dd-mm-yyyy): ").split(',')
            time_range2 = input("Enter second timerange (dd-mm-yyyy,dd-mm-yyyy): ").split(',')
            if len(time_range1) != 2 or len(time_range2) != 2:
                print("please provide correct number of arguments")
            elif not t2.is_valid_date(time_range1[0]) or not t2.is_valid_date(time_range1[1]) or not t2.is_valid_date(time_range2[0]) or not t2.is_valid_date(time_range2[1]):
                print("Dates are not valid")
            elif not t2.is_valid_date_range(time_range1[0],time_range1[1]) or not t2.is_valid_date_range(time_range2[0],time_range2[1]):
                print('date range are not valid')
            elif t2.is_overlapping(time_range1,time_range2):
                print("time range are overlapping")
            else:
                while(1):
                    ch = input("plot world cloud for\na.news\nb.responses\n")
                    if(ch == 'a'):
                        world_news1 = t2.get_world_news_responses(time_range1[0],time_range1[1],t2.get_world_newslinks())
                        world_news2 = t2.get_world_news_responses(time_range2[0],time_range2[1],t2.get_world_newslinks())
                        doc1 = ''
                        doc2 = ''
                        for date in world_news1:
                            doc1 = doc1 + date + world_news1[date]
                        
                        for date in world_news2:
                            doc2 = doc2 + date + world_news2[date]
                            
                        if(len(doc1) == 0 and len(doc2) == 0):
                            print('No data available')
                            break
                            
                        common_words = [*t2.remove_stop_words(doc1), *t2.remove_stop_words(doc2)]
                        print('world cloud for common words')
                        t2.generate_word_cloud(' '.join(common_words),"word cloud for News common words")
                        
                        covid_common_words = t2.covid_common_words(common_words)
                        print('world cloud for covid common words',"Word cloud for news covid related common words")
                        t2.generate_word_cloud(' '.join(covid_common_words),"word cloud for News covid common words")
                        break
                    elif(ch == 'b'):
                        world_responses1 = t2.get_world_news_responses(time_range1[0],time_range1[1],t2.get_world_responselinks())
                        world_responses2 = t2.get_world_news_responses(time_range2[0],time_range2[1],t2.get_world_responselinks())
                        doc1 = ''
                        doc2 = ''
                        for date in world_responses1:
                            doc1 = doc1 + date + world_responses1[date]
                        
                        for date in world_responses2:
                            doc2 = doc2 + date + world_responses2[date]
                            
                        if(len(doc1) == 0 and len(doc2) == 0):
                            print('No data available')
                            break
                            
                        common_words = [*t2.remove_stop_words(doc1), *t2.remove_stop_words(doc2)]
                        print('world cloud for common words')
                        t2.generate_word_cloud(' '.join(common_words),"Word cloud for responses common words")
                        
                        covid_common_words = t2.covid_common_words(common_words)
                        print('world cloud for covid common words')
                        t2.generate_word_cloud(' '.join(covid_common_words),"Word cloud for responses covid common words")
                        break
                    else:
                        print("enter appropriate choice. Try again")
                break
    elif(choice == 18):
        while(1):
            time_range1 = input("Enter first timerange (dd-mm-yyyy,dd-mm-yyyy): ").split(',')
            time_range2 = input("Enter second timerange (dd-mm-yyyy,dd-mm-yyyy): ").split(',')
            if len(time_range1) != 2 or len(time_range2) != 2:
                print("please provide correct number of arguments")
            elif not t2.is_valid_date(time_range1[0]) or not t2.is_valid_date(time_range1[1]) or not t2.is_valid_date(time_range2[0]) or not t2.is_valid_date(time_range2[1]):
                print("Dates are not valid")
            elif not t2.is_valid_date_range(time_range1[0],time_range1[1]) or not t2.is_valid_date_range(time_range2[0],time_range2[1]):
                print('date range are not valid')
            elif t2.is_overlapping(time_range1,time_range2):
                print("time range are overlapping")
            else:
                while(1):
                    ch = input("find percentage of covid related words for\na.news\nb.responses\n")
                    if(ch == 'a'):
                        world_news1 = t2.get_world_news_responses(time_range1[0],time_range1[1],t2.get_world_newslinks())
                        world_news2 = t2.get_world_news_responses(time_range2[0],time_range2[1],t2.get_world_newslinks())
                        doc1 = ''
                        doc2 = ''
                        for date in world_news1:
                            doc1 = doc1 + date + world_news1[date]
                        
                        for date in world_news2:
                            doc2 = doc2 + date + world_news2[date]
                            
                        if(len(doc1) == 0 and len(doc2) == 0):
                            print('No data available')
                            break
                            
                        common_words = [*t2.remove_stop_words(doc1), *t2.remove_stop_words(doc2)]
                        covid_words_percent = t2.covid_words_per(common_words)
                        for percent in covid_words_percent:
                            print('{} = {:2f}'.format(percent,covid_words_percent[percent]))
                        break
                    elif(ch == 'b'):
                        world_responses1 = t2.get_world_news_responses(time_range1[0],time_range1[1],t2.get_world_responselinks())
                        world_responses2 = t2.get_world_news_responses(time_range2[0],time_range2[1],t2.get_world_responselinks())
                        doc1 = ''
                        doc2 = ''
                        for date in world_responses1:
                            doc1 = doc1 + date + world_responses1[date]
                        
                        for date in world_responses2:
                            doc2 = doc2 + date + world_responses2[date]
                        
                        if(len(doc1) == 0 and len(doc2) == 0):
                            print('No data available')
                            break
                            
                        common_words = [*t2.remove_stop_words(doc1), *t2.remove_stop_words(doc2)]
                        covid_words_percent = t2.covid_words_per(common_words)
                        for percent in covid_words_percent:
                            print('{} = {:2f}'.format(percent,covid_words_percent[percent]))
                        break
                    else:
                        print("enter appropriate choice. Try again")
                break
    elif(choice == 19):
        while(1):
            time_range1 = input("Enter first timerange (dd-mm-yyyy,dd-mm-yyyy): ").split(',')
            time_range2 = input("Enter second timerange (dd-mm-yyyy,dd-mm-yyyy): ").split(',')
            if len(time_range1) != 2 or len(time_range2) != 2:
                print("please provide correct number of arguments")
            elif not t2.is_valid_date(time_range1[0]) or not t2.is_valid_date(time_range1[1]) or not t2.is_valid_date(time_range2[0]) or not t2.is_valid_date(time_range2[1]):
                print("Dates are not valid")
            elif not t2.is_valid_date_range(time_range1[0],time_range1[1]) or not t2.is_valid_date_range(time_range2[0],time_range2[1]):
                print('date range are not valid')
            elif t2.is_overlapping(time_range1,time_range2):
                print("time range are overlapping")
            else:
                while(1):
                    ch = input("find top 20 common words for\na.news\nb.responses\n")
                    if(ch == 'a'):
                        world_news1 = t2.get_world_news_responses(time_range1[0],time_range1[1],t2.get_world_newslinks())
                        world_news2 = t2.get_world_news_responses(time_range2[0],time_range2[1],t2.get_world_newslinks())
                        doc1 = ''
                        doc2 = ''
                        for date in world_news1:
                            doc1 = doc1 + date + world_news1[date]
                        
                        for date in world_news2:
                            doc2 = doc2 + date + world_news2[date]
                        
                        if(len(doc1) == 0 and len(doc2) == 0):
                            print('No data available')
                            break
                            
                        common_words = [*t2.remove_stop_words(doc1), *t2.remove_stop_words(doc2)]
                        top_common = t2.find_top_common(common_words)
                        print('top 20 common words')
                        print(*top_common[0:20])
                        for words in top_common[0:20]:
                            print(*words)
                        print('\n')
                        common_covid_words = t2.find_top_covid(common_words)
                        print('top 20 common covid words')
                        for words in common_covid_words[0:20]:
                            print(*words)
                        break
                    elif(ch == 'b'):
                        world_responses1 = t2.get_world_news_responses(time_range1[0],time_range1[1],t2.get_world_responselinks())
                        world_responses2 = t2.get_world_news_responses(time_range2[0],time_range2[1],t2.get_world_responselinks())
                        doc1 = ''
                        doc2 = ''
                        for date in world_responses1:
                            doc1 = doc1 + date + world_responses1[date]
                        
                        for date in world_responses2:
                            doc2 = doc2 + date + world_responses2[date]
                            
                        if(len(doc1) == 0 and len(doc2) == 0):
                            print('No data available')
                            break
                            
                        common_words = [*t2.remove_stop_words(doc1), *t2.remove_stop_words(doc2)]
                        top_common = t2.find_top_common(common_words)
                        print('top 20 common words')
                        for words in top_common[0:20]:
                            print(*words)
                        print('\n')
                        common_covid_words = t2.find_top_covid(common_words)
                        print('top 20 common covid words')
                        for words in common_covid_words[0:20]:
                            print(*words)
                        break
                    else:
                        print("enter appropriate choice. Try again")
                break 
    elif(choice == 20):
        while(1):
            country = input("enter country name: ")
            if country in t2.country_list:
                print(t2.get_date_range(country))
                break
            else:
                print("country not available in list")
    
    elif(choice == 21):
        while(1):
            country = input("enter country name: ")
            if country in t2.country_list:
                while(1):
                    time_range = input("Enter time range (dd-mm-yyyy,dd-mm-yyyy): ").split(',')
                    if len(time_range) != 2:
                        print('Please provide correct number of arguments')
                    elif not t2.is_valid_date(time_range[0]) or not t2.is_valid_date(time_range[1]):
                        print('Dates are not valid')
                    elif not t2.is_valid_date_range(time_range[0],time_range[1]):
                        print('date range in not valid')
                    else:    
                        country_news = t2.get_country_news_data(country,time_range[0],time_range[1])
                        main_document = ''
                        for date in country_news:
                            print('{}\n{}\n\n'.format(date,country_news[date]))
                            main_document = main_document + date + country_news[date]
                        if(len(main_document) == 0):
                            print("No data available")
                            break
                        else:
                            t2.generate_word_cloud(main_document,"Word cloud for country news")
                        
                        while(1):
                            ch = input("Find top 3 closest according to Jaccard similarity (Yes/No): ")
                            if ch == "Yes":
                                while(1):
                                    ch2 = input("find jaccard similarity of:\na.common words\nb.covid words\n")
                                    if(ch2 == 'a'):
                                        scores = {}
                                        for countries in t2.country_list:
                                            if(country != countries):
                                                country_news = t2.get_country_news_data(countries,time_range[0],time_range[1])
                                                document = ''
                                                for date in country_news:
                                                    document = document + date + country_news[date]
                                                if(len(document) != 0):
                                                    scores[countries] = t2.jaccard(main_document,document)
                                        sorted_scores = sorted(scores.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
                                        for score in sorted_scores[0:3]:
                                            print('{} {:2f}'.format(score[0],score[1]))
                                        break
                                    elif(ch2 == 'b'):
                                        scores = {}
                                        for countries in t2.country_list:
                                            if(country != countries):
                                                country_news = t2.get_country_news_data(countries,time_range[0],time_range[1])
                                                document = ''
                                                for date in country_news:
                                                    document = document + date + country_news[date]
                                                if(len(document) != 0):
                                                    scores[countries] = t2.jaccard_covid(main_document,document)
                                        sorted_scores = sorted(scores.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
                                        for score in sorted_scores[0:3]:
                                            print('{} {:2f}'.format(score[0],score[1]))
                                        break
                                    else:
                                        print("please provide appropriate option")           
                                break
                            elif ch == "No":
                                break
                            else:
                                print("please enter appropriate answer")
                        break
                break
                
            else:
                print("country not availabel")
        
    elif(choice == 22):
        print("Exiting")
        break
    else:
        print("Worng choice entered, Please try again!")

    input("Press any key to continue...")
    os.system(CLEAR)



