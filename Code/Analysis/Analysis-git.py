#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: group 11
"""
'0. Import modules and packages and start timer'
#%%

import pandas as pd
import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#Starting the counter
start = time.perf_counter()

'1. Functions for the preparation of the dataset for Analysis'
#%%

# Import the scraping data from csv to a DataFrame
df = pd.read_csv('resultScraping.csv')

#Delete the scraping Index column
del df['Unnamed: 0']

# Method to check if authors have the same last name
def checkForSharedSurname(df):
    df.drop_duplicates(subset="Name", keep="first", inplace=True)
    df[['First Name','Last Name']] = df.Name.str.split(" ",expand=True,)
    del df['Name']
    df = df[["First Name", "Last Name", "Date", "Time"]]
    
    if df['Last Name'].is_unique:
        print('There are no couples with the the same last name')
    else:
        print('There are couples with the same last name')
        
    if df['First Name'].is_unique:
        print('There are no couples with the the same first name')
    else:
        print('There are couples with the same first name')

# Returns a list of all the authors working at Tabularazor Inc.     
def extractAuthors(df):
    authors = list(df['Name'].unique())
    return authors

# Creates the publishing table for all authors and years
def createWorkingTable(df):
    # Creates a list of the authors
    authors = extractAuthors(df)
    # Index as dates, 'D' for all calendar dates. 'B' could be used for all business days.
    index = pd.date_range(start = '2012/1/1', end = '2019/12/31', freq='D')
    # Authors as columns
    columns = [authors]
    # Create the DataFrame
    df = pd.DataFrame(index=index, columns=columns)
    df = df.fillna(0)
    return df

# Fills the publishing table with the number of published article per weekday for each author
def fillWorkingTable(df_scrape, df_filled):
            for i in range(len(df_scrape.index)):
                date = df_scrape.loc[i,'Date']
                name = df_scrape.loc[i,'Name']
                df_filled.loc[[date],[name]] = 1
            df_filled.to_csv("./ResultCSV/PublishingScheduleDays.csv")
            return df_filled

# Fills the publishing table with a zero (if the author has worked that day) or with a one (if the author did not work that day)
def fillWorkingTableArticlesPerDay(df_scrape, df_filled):
            for i in range(len(df_scrape.index)):
                date = df_scrape.loc[i,'Date']
                name = df_scrape.loc[i,'Name']
                df_filled.loc[[date],[name]] += 1
            df_filled.to_csv("./ResultCSV/PublishedEachDay.csv")
            return df_filled
        
'2. Executing the preparation to retreive the dataset for Analysis'     
#%%
# Creates the empty publishing table
workingTable = createWorkingTable(df)

# Creates the publishing table with the day worked for each author for the history of Tabularazor Inc. (1 = has published that day, 0 =  has not published that day)
#filledWorkingTable = fillWorkingTable(df, workingTable)

# Creates the publishing table with amount of articles published for each author for the history of Tabularazor Inc. 
#filledWorkingTableNumbers = fillWorkingTableArticlesPerDay(df, workingTable)

# Creates DataFrame per week and days worked per author, this reads the .csv file which is produces at line 70. Could also use the DataFrame filledWorkingTable but is commented out due to computational speed.
weeksWorked = pd.read_csv('./ResultCSV/PublishingScheduleDays.csv', parse_dates=[0], index_col=[0], skipinitialspace=True,).resample('W', kind='period').sum()

# Creates DataFrame per week and amount of articles published per author, this reads the .csv file which is produces at line 79. Could also use the DataFrame filledWorkingTableNumbers but is commented out due to computational speed.
weeksWorkedAmount = pd.read_csv('./ResultCSV/PublishedEachDay.csv', parse_dates=[0], index_col=[0], skipinitialspace=True,).resample('W', kind='period').sum()

# Creates DataFrame per week and days worked per author, this reads the .csv file which is produces at line 79. Could also use the DataFrame filledWorkingTableNumbers but is commented out due to computational speed.
yearsWorked = pd.read_csv('./ResultCSV/PublishedEachDay.csv', parse_dates=[0], index_col=[0], skipinitialspace=True,).resample('Y', kind='period').sum()


# Correlation matrix of the matching holiday weeks per author.
corr = weeksWorked.corr().abs()

'3. Functions for the Analysis'
#%%

# Returns general statistics about the authors and their weekly publishing behaviour
def averageArticlePerWeek(weeksWorked):
    perWeek = weeksWorked.replace(0, np.NaN)
    return(perWeek.describe())

# Print the amount of articles published each year when given the publishing schedule per year
def totalArticlesEachYear(yearsWorked):
    yearsWorkedMean = yearsWorked.replace(0, np.NaN)
    print(yearsWorkedMean.iloc[:, 0:49].sum(axis=1))

# Generates an correlation heatmap for the author's and their working days per week 
def heatmapCorrelationAll(correlation):
    matrix = np.triu(corr) # take upper correlation matrix
    plt.subplots(figsize=(23,23))
    ax = sns.heatmap(corr,
                     mask=matrix, 
                     vmin=0, vmax=1, center=0,
                     cmap='coolwarm',
                     linewidths = 1,
                     cbar_kws={"shrink": 0.5},
                     #cmap=sns.diverging_palette(20, 220, n=200),
                     square=True
                     )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=90,
        horizontalalignment='right'
        );
    plt.savefig('./Graphs/Heatmap.png')

# Returns the correlation ordered in descending value per author couple
def checkCorrelationPerYear(df, begin, end,correlationResults, year):
    df_year = df.loc[begin:end]
    corr_year = df_year.corr().abs()
    orderedCorrelation = corr_year.unstack().sort_values(ascending=False).drop_duplicates().tail(-1)

    for i in range(len(orderedCorrelation)):
        names = orderedCorrelation.index[i]
        name = list(names)
        Value = orderedCorrelation[i]
        correlationResults.loc[i,'Name1'] = name[0]
        correlationResults.loc[i,'Name2'] = name[1]
        correlationResults.loc[i,'Correlation'] = Value
        correlationResults.loc[i,'Year'] = year
    return correlationResults

# Returns a correlation dataframe for a specific year
def correlationDF(years, correlationResults, weeksWorked):
    correlation = pd.DataFrame(columns = ['Name1', 'Name2', 'Correlation', 'Year'])
    for year in years:
        currentYear = str(year)
        result = checkCorrelationPerYear(weeksWorked, currentYear + '/1/1', currentYear + '/12/31', correlationResults, currentYear)
        correlation = correlation.append(result)
    return correlation

# Returns the correlation table of the further inspeced couples
def createCorrelationTableCouples():
    years = [2012,2013,2014,2015,2016,2017,2018,2019]
    correlationResults = pd.DataFrame(columns = ['Name1', 'Name2', 'Correlation', 'Year'])
    correlationDataFrame = correlationDF(years, correlationResults, weeksWorked)

    namesFirstpair = ['Grover Gibbons', 'Augusta Beltrami']
    namesSecondpair = ['Vonk Billips', 'Julieta Knapp']

    new = correlationDataFrame.loc[(correlationDataFrame['Name1'].isin(namesFirstpair)) & (correlationDataFrame['Name2'].isin(namesFirstpair)) | (correlationDataFrame['Name1'].isin(namesSecondpair)) & (correlationDataFrame['Name2'].isin(namesSecondpair))]
    print('The dataframe for the two most correlated couples over the years is as following:', new)
    new.to_csv('./ResultCSV/Couples over years.csv')

# Returns the similar holidays of the further inspected couple
def showSimilarHolidayCouple(weeksWorked):
    vacation_couples = weeksWorked[['Vonk Billips','Julieta Knapp','Grover Gibbons','Augusta Beltrami']]
    return vacation_couples

# Returns the amount of holidays for the 30 employees working at Tabularazor
def findHolidaysOfAuthors(df):
    df_years = df.loc['2012-1-1':'2019-12-31']

    df_years_free = df_years.isin([0]).sum(axis=0)

    df_free = pd.DataFrame(df_years_free)
    

    df_free.rename(columns={df_free.columns[0]: "Days not worked" }, inplace = True)
    df_not_worked = df_free.sort_values(by ="Days not worked")


    df_not_worked = df_not_worked.assign(Weekend = int('835'))
    df_not_worked = df_not_worked.assign(Holiday = int('51'))
    

    df_not_worked = df_not_worked[df_not_worked['Days not worked'] < 1350]

    df_not_worked.loc[:,'Number of free days'] = df_not_worked.loc[:,'Days not worked'] - df_not_worked.loc[:,'Holiday'] - df_not_worked.loc[:,'Weekend']
    df_not_worked.loc[:,'Number of free days'] = df_not_worked.loc[:,'Number of free days']/8
    
    return df_not_worked

    myFig = plt.figure();
    boxplot = df_not_worked.boxplot(column=['Number of free days'])
    myFig.savefig("./Graphs/Boxplot.png")
    
# Create plot of author publications over time
def authorPublicationPlot(df):
    plt.figure(figsize=(20,15))
    plt.title('Author Publications over Time')
    sns.scatterplot(x=df['Date'],y=df['Name'],data=df,sizes='carat',markers=False)
    plt.show()
    plt.savefig('./Graphs/AuthorPublicationPlot.png')

# Creates a plot for further inspection for maternity leave
def maternityCheck(weeksWorked):
    maternity = weeksWorked[['Marthe Hale','Corrine Gallop']]
    m_plot = maternity.plot.bar(title=('Number of days worked per week over time'))
    m_plot.set_xlabel("Date")
    m_plot.set_ylabel("Number of days worked per week")
    plt.show()
    plt.savefig('./Graphs/MaternityCheck.png')


'4. Executing the Analysis and calculate total calculation time'
#%%

#checkForSharedSurname(df)

heatmapCorrelationAll(corr)

createCorrelationTableCouples()

vactionOfCouple = showSimilarHolidayCouple(weeksWorked)

authorPublicationPlot(df)

maternityCheck(weeksWorked)

#check = findHolidaysOfAuthors(filledWorkingTable)


# End the timer
finish = time.perf_counter()

# Print the timer
print(f'Finished in {round(finish-start,2)} seconds(s)')
