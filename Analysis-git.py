#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 15:20:43 2021

@author: alexanderkempen
"""

import pandas as pd
import datetime
import time

#Starting the counter
start = time.perf_counter()

# Import the scraping data from csv to a DataFrame
df = pd.read_csv('resultScraping.csv')

#Needs fixing
del df['Unnamed: 0']


# Method to check if authors have the same last name
def checkForSharedSurname(df):
    df.drop_duplicates(subset="Name", keep="first", inplace=True)
    df[['First Name','Last Name']] = df.Name.str.split(" ",expand=True,)
    del df['Name']
    df = df[["First Name", "Last Name", "Date", "Time"]]
    print(len(df.index))

    if df['Last Name'].is_unique:
        print('There are no couples with the the same last name')
        
def convertDates(df):
    for index in range(len(df.index)):
        temp = df.loc[index,'Date']
        dateArray = temp.split('-')
        df.loc[index, 'Date'] = datetime.date(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]))
  



startd = datetime.date(2012, 1, 1)

daystwentytwelve = []

i = 1
daystwentytwelve.insert(i,startd)

print(daystwentytwelve)

for i in range(365):
    daystwentytwelve.insert(i,datetime.timedelta(days=i))
     
    









finish = time.perf_counter()

print(f'Finished in {round(finish-start,2)} seconds(s)')