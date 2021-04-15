#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: group 11
"""
'0. Import modules and packages'
#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import concurrent.futures

'1. Set up timer, column names and URL root'
#%%
#Starting the counter
start = time.perf_counter()

#Creating two universal DataFrame for all articles to be stored in
column_names = ["Name","Date","Time"]
df = pd.DataFrame(columns = column_names)
df2 =  pd.DataFrame(columns = column_names)


#Initial website newspaper Tabularazor
tabularazor = 'https://news.tabularazor.org/'

'2. Create soup objects for URL input'
#%%
#Creates connection with a specific input url creating soup object
def createSoupConnection(http):
    inputUrl = requests.get(http)
    src = inputUrl.content
    soup = BeautifulSoup(src, 'lxml')
    return soup

#Finds all a class html elements and returns these in a list
def findHtmlLink(soupConnection):
    htmlLinks = []
    hyperlinks = soupConnection.find_all('a')
    #Convert to only text part
    for hyperlink in hyperlinks:
        htmlLinks.append(hyperlink.attrs['href'])
    return htmlLinks
    
#Create the connection with the newspaper site
soupSite = createSoupConnection(tabularazor)

#Create a list for all the years that have a repository
years = findHtmlLink(soupSite)

'3. Get URL of year, month and article to scrape article details'
#%%
'3.1 Scrape author, date and time from an article'
#%%
#Adds article attributes in a DataFrame
def getArticleInfo(article):
    index = len(df.index)
    soupArticle = createSoupConnection(tabularazor+article)
    authors = soupArticle.find('div', 'author')
    dates = soupArticle.find('div', 'date')
    times = soupArticle.find('div','time')
    
    author = authors.get_text()
    date = dates.get_text()
    time = times.get_text()
    
    df.loc[index,'Name'] = author
    df.loc[index,'Date'] = date
    df.loc[index,'Time'] = time

'3.1. Get all URLs of a specific month'
#%%
#Gets all the articles from a specific month
def getArticlesOfMonth(month):
        soupArticles = createSoupConnection(tabularazor+month)
        articles = findHtmlLink(soupArticles)
        for article in articles:
            getArticleInfo(article)
        return df

'3.1 Get all URLs of specific year'
#%%
#Gets all the articles from a specific year and returns these in a DataFrame
def getMonthsOfYear(year):
    soupMonth = createSoupConnection(tabularazor+year)
    months = findHtmlLink(soupMonth)
    for month in months:
        getArticlesOfMonth(month)
    return df

'4. Establish multiprocessing to enhance total scraping time by processing years in parallel'
#%%
#Ruturns DataFrame for all the years using multiprocessing
def runMultiProcessing(df2):
    if __name__ == '__main__':
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(getMonthsOfYear,years)
            for result in results:
                df2 = df2.append(result)
            df2.to_csv('resultScraping.csv')
            return df2

### Executing line ###
resultScraping = runMultiProcessing(df2)

'5. Calculate total webscraping time'
#%%
finish = time.perf_counter()

print(f'Finished in {round(finish-start,2)} seconds(s)')