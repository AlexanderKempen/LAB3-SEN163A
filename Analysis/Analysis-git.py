#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 15:20:43 2021

@author: alexanderkempen
"""

import pandas as pd
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
        
# Returns a list of all the authors working at Tabularazor Inc.     
def extractAuthors(df):
    authors = list(df['Name'].unique())
    return authors

# Creates the publishing table for all authors and years
def createWorkingTable(df, weekType):
    # Creates a list of the authors
    authors = extractAuthors(df)
    # Index as dates, 'D' for all calendar dates. 'B' could be used for all business days.
    index = pd.date_range(start = '2012/1/1', end = '2019/12/31', freq=weekType)
    # Authors as columns
    columns = [authors]
    # Create the DataFrame
    df = pd.DataFrame(index=index, columns=columns)
    df = df.fillna(0)
    return df
 
# Fills the publishing table with the number of published article per weekday for each author
def fillWorkingTable(df_scrape, df_filled, weekType):
    if weekType == 'D':                             #Check if weektype is set for only business days
            for i in range(len(df_scrape.index)):
                date = df_scrape.loc[i,'Date']
                name = df_scrape.loc[i,'Name']
                df_filled.loc[[date],[name]] += 1
            df_filled.to_csv("Publising schedule weeks.csv")
            return df_filled
    else:
        for i in range(len(df_scrape.index)):
            date = df_scrape.loc[i,'Date']
            name = df_scrape.loc[i,'Name']
            if date in df_filled.index:
                df_filled.loc[[date],[name]] += 1
    df_filled.to_csv("Publising schedule business days.csv")
    return df_filled

    
# =============================================================================
# weekType = "D"
# # Creates the empty publishing table
# workingTable = createWorkingTable(df, weekType)
# 
# # Creates the publishing table with the number of published article per day for each author for the history of Tabularazor Inc.
# filledWorkingTable = fillWorkingTable(df, workingTable, weekType)
# 
# =============================================================================

# Creates DataFrame per week and days worked per author
dfX = pd.read_csv('WeeksWorked.csv', parse_dates=[0], index_col=[0], skipinitialspace=True,)
workWeek = dfX.resample('W', kind='period').sum()

# Correlation matrix of the matching holiday weeks per author.
corr = dfX.corr()

orderedCorrelation = dfX.corr().unstack().sort_values(ascending=False).drop_duplicates().tail(-1)

# End the timer
finish = time.perf_counter()

# Print the timer
print(f'Finished in {round(finish-start,2)} seconds(s)')