1. packages used datetime, urllib, ply, nltk.corpus, nltk.tokenize, WordCloud, matplotlib

2. to install nltk
    pip install nltk
    nltk.download('punkt')
    nltk.download('stopwords')

3. The program was tested on Windows 10 OS

4. To run the program enter: python menu.py

4. There are following files: menu.py, task1.py, task2.py, tokrules_1.py, tokrules_2.py, tokrules_3.py, tokrules_4.py
tokrules_5.py, tokrules_6.py, tokrules_7.py
   menu.py contains the menu logic for both tasks. task1.py contains all the function and uitities for task 1 of assignment. 
   task2.py contains all the function and utilities for task 2 of assignment. tokrules_1.py contains grammer to extract
   data from worldometers table, tokrules_2.py contains grammer to extract covid data for each individual country in worldomenters website.
   tokrules_3.py contains grammer to extract links of world news, world responses, country news from wikipedia. tokrules_4.py contains
   grammer to extract news links for England. tokrules_5 contains grammer to extract data from world news and response pages for each date.
   tokrules_6 contains grammer to extract news from country news page for each country. tokrules_7 contain grammer to format the country news. 

5. As the program was tested of Win10 OS so we use 'cls' system call. 
   If the program needs to be checked on linux we can change CLEAR constant to "clear" at the top in menu.py

6. Constant SMOOTHING_FACTOR in task1.py file is initialized to 0.0001 and can be changed if needed.

7. For finding closest countries we are using left margin (LMARGIN) and right margin (RMARGIN) constants.
The program will return the list of countries with percentage change in range [givenPchange+LMARGIN, givenPchange+RMARGIN]
where 'givenPchange' is the percentage change value of the input country. The LMARGIN and RMARGIN are set to 5 by default
and can be changed if needed. The constants LMARGIN, RMARGIN can be found in task1.py

8. Date format followed is dd-mm-yyyy

9. To record logs a file 'query_logs.txt' will be created automatically

10. The names of countries and continents are read from file 'worldometers_countrylist.txt'. The format of file
should be 
    continent_1:
    -----------------
    country_1
    country_2

    continent_2:
    --------------------
    country_1
    country_2

11. We are initially parsing all the required data(for task 1) at once so when the program is started, need to wait
for around 1 minute for menu to be visible. Once menu is visible we can fire queries.

12. For some queries need to wait for some time to get the output.