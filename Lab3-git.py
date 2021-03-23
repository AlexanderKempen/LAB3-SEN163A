#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 20:33:58 2021

@author: alexanderkempen
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import concurrent.futures

#Starting the counter
start = time.perf_counter()

#Creating universal DataFrame for all articles
column_names = ["Name", "Surname", "Year", "Month", "Day","Time","Title"]
df = pd.DataFrame(columns = column_names)


#Initial website newspaper Tabularazor
tabularazor = 'https://news.tabularazor.org/'

#Indicates that page is accessible if 200 and valid
def checkStatusSite(site):
    if site.status_code == 200:
        headers = site.headers
        print('Site is available','\n')
        print('The headers of the site are:', '\n', headers, '\n')

#Creates connection with a specific site creating soup object
def createSoupConnection(http):
    inputUrl = requests.get(http)
    src = inputUrl.content
    soup = BeautifulSoup(src, 'lxml')
    return soup

#Finds clickable html elements and returns these in a list
def findHtmlLink(soupConnection):
    htmlLinks = []
    hyperlinks = soupConnection.find_all('a')
    #Convert to only text part
    #for hyperlink in hyperlinks:
    for hyperlink in hyperlinks:
        htmlLinks.append(hyperlink.attrs['href'])
    return htmlLinks
    
#ehfuehfeuh
#Create connection with the site
soupSite = createSoupConnection(tabularazor)

#Create list for all the article years
years = findHtmlLink(soupSite)

#Adds article attributes in a DataFrame
def getArticleInfo(article):
    index = len(df.index)
    soupArticle = createSoupConnection(tabularazor+article)
    author = soupArticle.find('div', 'author')
    date = soupArticle.find('div', 'date')
    times = soupArticle.find('div','time')
    title = soupArticle.find('h1')
    titles = title.get_text()
    timess = times.get_text()
    authora = author.get_text()
    data = date.get_text().split('-')
    name = authora.split()
    df.loc[index,'Name'] = name[0]
    df.loc[index, 'Surname'] = name[1]
    df.loc[index,'Year'] = data[0]
    df.loc[index,'Month'] = data[1]
    df.loc[index,'Day'] = data[2]
    df.loc[index,'Time'] = timess
    df.loc[index, 'Title'] = titles
               
#Gets all the articles from a specific month
def getArticlesOfMonth(month):
        soupArticles = createSoupConnection(tabularazor+month)
        articles = findHtmlLink(soupArticles)
        
########Om alles te runnen verwijder hieronder [:100] 

        for article in articles[:100]:
            print('i')
            getArticleInfo(article)
        #return df

#Gets all the articles from a specific year and returns these in a DataFrame
def getMonthsOfYear(year):
    soupMonth = createSoupConnection(tabularazor+year)
    months = findHtmlLink(soupMonth)
    for month in months:
        getArticlesOfMonth(month)
    return df


######Verwijder # voor welk jaar je een DataFrame wilt maken

#twelve = getMonthsOfYear(years[0])
#thirteen = getMonthsOfYear(years[1])
#fourteen = getMonthsOfYear(years[2])
#fifteen = getMonthsOfYear(years[3])
#sixteen = getMonthsOfYear(years[4])
#seventeen = getMonthsOfYear(years[5])
#eighteen = getMonthsOfYear(years[6])
#nineteen = getMonthsOfYear(years[7])

# =============================================================================
# if __name__ == '__main__':
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         results = executor.map(getMonthsOfYear,years)
#         for result in results:
#             df2 = df2.append(result)
#             #print(df2)
#   
# =============================================================================
        
finish = time.perf_counter()

print(f'Finished in {round(finish-start,2)} seconds(s)')

