#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 20:33:58 2021

@author: alexanderkempen
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import multiprocessing 
import time
import concurrent.futures

result = requests.get('https://news.tabularazor.org/')

#Indicates that page is accessible if 200 and valid
def checkStatusSite(site):
    if site.status_code == 200:
        headers = site.headers
        print('Site is available','\n')
        print('The headers of the site are:', '\n', headers, '\n')
   # 
src = result.content
soup = BeautifulSoup(src,'lxml')
#A tag is a hyperlink within the page, creates list of all the links
yearHyperlinks = soup.find_all('a')
#List for all the yearlinks
years = []
#Accessing all the links, adding to the list, and printing them in order
for yearHyperlink in yearHyperlinks:
    years.append(yearHyperlink.attrs['href'])


column_names = ["Name", "Surname", "Year", "Month", "Day","Time"]
df = pd.DataFrame(columns = column_names)

column_names = ["Name", "Surname", "Year", "Month", "Day","Time"]
df2 = pd.DataFrame(columns = column_names)


resultMonths = requests.get('https://news.tabularazor.org/' + years[0])
src = resultMonths.content
soups = BeautifulSoup(src,'lxml')
monthHyperlinks = soups.find_all('a')

months = []
for monthHyperlink in monthHyperlinks:
    months.append(monthHyperlink.attrs['href'])
    
def getArticlesOfMonth(month):
        index = 0
        resultArticles = requests.get('https://news.tabularazor.org/' + month)
        src = resultArticles.content
        soupss = BeautifulSoup(src,'lxml')
        articleHyperlinks = soupss.find_all('a')
        
        articles = []
        for articleHyperlink in articleHyperlinks:
            articles.append(articleHyperlink.attrs['href'])
        
            for article in articles:
                resultArticle = requests.get('https://news.tabularazor.org/' + article)
                src = resultArticle.content
                soupsss = BeautifulSoup(src,'lxml')
                author = soupsss.find('div', 'author')
                date = soupsss.find('div', 'date')
                times = soupsss.find('div','time')
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
                index = index + 1
                return df

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(getArticlesOfMonth, months)
        for result in results:
            df2 = df2.append(result)
            print(df2) 

