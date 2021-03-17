#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 20:33:58 2021

@author: alexanderkempen
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


result = requests.get('https://news.tabularazor.org/')

#Indicates that page is accessible if 200 and valid
def checkStatusSite(site):
    if site.status_code == 200:
        headers = site.headers
        print('Site is available','\n')
        print('The headers of the site are:', '\n', headers, '\n')
    


src = result.content
soup = BeautifulSoup(src,'lxml')
#A tag is a hyperlink within the page, creates list of all the links
yearHyperlinks = soup.find_all('a')
#List for all the yearlinks
years = []
#Accessing all the links, adding to the list, and printing them in order
for yearHyperlink in yearHyperlinks:
    years.append(yearHyperlink.attrs['href'])


# =============================================================================
# 
# resultMonths = requests.get('https://news.tabularazor.org/' + years[0])
# src = resultMonths.content
# soups = BeautifulSoup(src,'lxml')
# monthHyperlinks = soups.find_all('a')
# 
# months = []
# for monthHyperlink in monthHyperlinks:
#     months.append(monthHyperlink.attrs['href'])
# 
# 
# resultArticleDay = requests.get('https://news.tabularazor.org/' + months[0])
# src = resultArticleDay.content
# soupss = BeautifulSoup(src,'lxml')
# articleHyperlinks = soupss.find_all('a')
# 
# =============================================================================

column_names = ["Name", "Surname", "Year", "Month", "Day","Time"]
df = pd.DataFrame(columns = column_names)


resultMonths = requests.get('https://news.tabularazor.org/' + years[0])
src = resultMonths.content
soups = BeautifulSoup(src,'lxml')
monthHyperlinks = soups.find_all('a')
    
months = []
for monthHyperlink in monthHyperlinks:
    months.append(monthHyperlink.attrs['href'])
    for month in months:
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
                time = soupsss.find('div','time')
                times = time.get_text()
                authora = author.get_text()
                data = date.get_text().split('-')
                name = authora.split()
                df.loc[index,'Name'] = name[0]
                df.loc[index, 'Surname'] = name[1]
                df.loc[index,'Year'] = data[0]
                df.loc[index,'Month'] = data[1]
                df.loc[index,'Day'] = data[2]
                df.loc[index,'Time'] = times
                index = index + 1
                    
    df.to_csv('AuthorRegister.csv', index=False)  

# =============================================================================
# for year in years:
#     index = 0
#     resultMonths = requests.get('https://news.tabularazor.org/' + year)
#     src = resultMonths.content
#     soups = BeautifulSoup(src,'lxml')
#     monthHyperlinks = soups.find_all('a')
#     
#     months = []
#     for monthHyperlink in monthHyperlinks:
#         months.append(monthHyperlink.attrs['href'])
# 
#             
#     for month in months:
# 
#             resultArticles = requests.get('https://news.tabularazor.org/' + month)
#             src = resultArticles.content
#             soupss = BeautifulSoup(src,'lxml')
#             articleHyperlinks = soupss.find_all('a')
#     
#             articles = []
#             for articleHyperlink in articleHyperlinks:
#                 articles.append(articleHyperlink.attrs['href'])
# 
#             for article in articles:
#                 resultArticle = requests.get('https://news.tabularazor.org/' + article)
#                 src = resultArticle.content
#                 soupsss = BeautifulSoup(src,'lxml')
#                 author = soupsss.find('div', 'author')
#                 date = soupsss.find('div', 'date')
#                 time = soupsss.find('div','time')
#                 times = time.get_text()
#                 authora = author.get_text()
#                 data = date.get_text().split('-')
#                 name = authora.split()
#                 df.loc[index,'Name'] = name[0]
#                 df.loc[index, 'Surname'] = name[1]
#                 df.loc[index,'Year'] = data[0]
#                 df.loc[index,'Month'] = data[1]
#                 df.loc[index,'Day'] = data[2]
#                 df.loc[index,'Time'] = times
#                 index = index + 1
#                 
# df.to_csv('AuthorRegister.csv', index=False)                
#             
# =============================================================================
    
# =============================================================================
# months = []
# for monthHyperlink in monthHyperlinks:
#     months.append(monthHyperlink.attrs['href'])
#             
# #amountOfMonths = len(months)
# amountOfMonths = 1
# k = 0
# for month in months:
#     if amountOfMonths !=k:
#         resultArticles = requests.get('https://news.tabularazor.org/' + months[k])
#         src = resultArticles.content
#         soupss = BeautifulSoup(src,'lxml')
#         articleHyperlinks = soupss.find_all('a')
#     else:
#         break  
# 
# amountOfArticles = len(articleHyperlinks)
# i = 0
# articles = []
# for articleHyperlink in articleHyperlinks:
#     if amountOfArticles < i:
#         articles.append(articleHyperlink.attrs['href'])
#         resultArticle = requests.get('https://news.tabularazor.org/' + articles[i])
#         src = resultArticle.content
#         soupsss = BeautifulSoup(src,'lxml')
#         author = soupsss.find('div', 'author')
#         date = soupsss.find('div', 'date')
#         authora = author.get_text()
#         data = date.get_text().split('-')
#         name = authora.split()
#         df.loc[i,'Name'] = name[0]
#         df.loc[i, 'Surname'] = name[1]
#         df.loc[i,'Year'] = data[0]
#         df.loc[i,'Day'] = data[1]
#         df.loc[i,'Month'] = data[2]
#         i = i+1
#     else:
#         break
#         
# =============================================================================

# =============================================================================
# 
# amountOfYears = 1
# #= len(years)
# j = 0
# for year in years:
#     if amountOfYears != j:
#         resultMonths = requests.get('https://news.tabularazor.org/' + years[j])
#         src = resultMonths.content
#         soups = BeautifulSoup(src,'lxml')
#         monthHyperlinks = soups.find_all('a')
#         j = j + 1
#     else:
#         break
#     
#         months = []
#         for monthHyperlink in monthHyperlinks:
#             months.append(monthHyperlink.attrs['href'])
#             
#         #amountOfMonths = len(months)
#         amountOfMonths = 1
#         k = 0
#         for month in months:
#             if amountOfMonths !=k:
#                 resultArticleDay = requests.get('https://news.tabularazor.org/' + months[k])
#                 src = resultArticleDay.content
#                 soupss = BeautifulSoup(src,'lxml')
#                 articleHyperlinks = soupss.find_all('a')
#             else:
#                 break  
#        # amountOfArticles = len(articleHyperlinks)
#             amountOfArticles = 15
#             i = 0
#             articles = []
#             for articleHyperlink in articleHyperlinks:
#                 if amountOfArticles != i:
#                     articles.append(articleHyperlink.attrs['href'])
#                     resultArticle = requests.get('https://news.tabularazor.org/' + articles[i])
#                     src = resultArticle.content
#                     soupsss = BeautifulSoup(src,'lxml')
#                     author = soupsss.find('div', 'author')
#                     date = soupsss.find('div', 'date')
#                     authora = author.get_text()
#                     data = date.get_text().split('-')
#                     name = authora.split()
#                     df.loc[i,'Name'] = name[0]
#                     df.loc[i, 'Surname'] = name[1]
#                     df.loc[i,'Year'] = data[0]
#                     df.loc[i,'Day'] = data[1]
#                     df.loc[i,'Month'] = data[2]
#                     i = i+1
#                 else:
#                     break
# =============================================================================
        
        
        
# =============================================================================
#         
# i = 0
# articles = []
# for articleHyperlink in articleHyperlinks:
#     if amountOfArticles != i:
#         articles.append(articleHyperlink.attrs['href'])
#         resultArticle = requests.get('https://news.tabularazor.org/' + articles[i])
#         src = resultArticle.content
#         soupsss = BeautifulSoup(src,'lxml')
#         author = soupsss.find('div', 'author')
#         date = soupsss.find('div', 'date')
#         authora = author.get_text()
#         data = date.get_text().split('-')
#         name = authora.split()
#         df.loc[i,'Name'] = name[0]
#         df.loc[i, 'Surname'] = name[1]
#         df.loc[i,'Year'] = data[0]
#         df.loc[i,'Day'] = data[1]
#         df.loc[i,'Month'] = data[2]
#         i = i+1
#     else:
#         break
# =============================================================================
        
    
    
# =============================================================================
#     
#         src = resultArticleDay.content
#         soupss = BeautifulSoup(src,'lxml')
#         linksss = soupss.find_all('a')
#         urlsss = []
#         for linkss in linksss:
#             urlsss.append(linkss.attrs['href'])
#             
#         resultArticle = requests.get('https://news.tabularazor.org/' + urlsss[i])
#         src = resultArticle.content
#         soupsss = BeautifulSoup(src,'lxml')
#         author = soupsss.find('div', 'author')
#         date = soupsss.find('div', 'date')
#         authora = author.get_text()
#         data = date.get_text()
#         name = authora.split()
#         df.loc[i,'Name'] = name[0]
#         df.loc[i, 'Surname'] = name[1]
#         i = i+1
#     else:
#         break
# 
# =============================================================================


# =============================================================================
# 
# resultArticleDay = requests.get('https://news.tabularazor.org/' + urlss[0])
# 
# src = resultArticleDay.content
# soupss = BeautifulSoup(src,'lxml')
# linksss = soupss.find_all('a')
# 
# urlsss = []
# for linkss in linksss:
#     urlsss.append(linkss.attrs['href'])
# for urlss in urlsss:
#     print(urlss, '\n')
#     
# resultArticle = requests.get('https://news.tabularazor.org/' + urlsss[0])
# 
# 
# src = resultArticle.content
# soupsss = BeautifulSoup(src,'lxml')
# 
# 
# author = soupsss.find('div', 'author')
# date = soupsss.find('div', 'date')
# print(date)
# print(author)
# authora = author.get_text()
# print(authora)
# =============================================================================

