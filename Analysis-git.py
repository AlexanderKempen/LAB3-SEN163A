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

# Converts the 'Date' column String object to datetime objects
def convertDates(df):
    for index in range(len(df.index)):
        temp = df.loc[index,'Date']
        dateArray = temp.split('-')
        df.loc[index, 'Date'] = datetime.date(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]))
        
# Returns a list of all the authors working at Tabularazor Inc.     
def extractAuthors(df):
    df.drop_duplicates(subset="Name", keep="first", inplace=True)
    authors = df['Name'].tolist()
    return authors
    
    
# Creates a list of the authors
authors = extractAuthors(df)

# Start date for 2012 DataFrame
startd = datetime.date(2012, 1, 1)

# Index as dates, 'D' for all calendar dates. 'B' could be used for all business days.
index = pd.date_range(startd, periods=366, freq='D')

# Authors as columns
columns = [authors]
 
# Create 2012 DataFrame
dfi = pd.DataFrame(index=index, columns=columns)
dfi = dfi.fillna(0)
 
print(dfi)


# Transpose original 2012 DataFrame (switch columns with index)
dfi_transposed = dfi.T 

print(dfi_transposed)