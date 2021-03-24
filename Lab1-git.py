#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 21:37:35 2021

@author: ted
"""

# import the packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3 as sql
from datetime import datetime
# import seaborn as sns

#%%
## 1.0 Setting up and preparing the dataframe
# Create connection to database file 
con = sql.connect('./transaction_data.db')
cur = con.cursor()
begin_time = datetime.now()

# Transforming strings into integers with three decimals 
def string_conversion(i):
    if "E" in i: #columns containing a 'to the power 10 base' [E] are multiplied by 1000
        return int(float(i) * 1000)
    else: 
        integer, decimals = i.split('.') #string is split on the decimal point
        decimals = decimals[:3].ljust(3,"0") #all decimal parts are equalized to three 0's
        return int(integer+decimals) #integers are created by adding the decimals again

# Create DataFrame and handle float values and large numbers
df = pd.read_sql_query('SELECT * FROM transaction_data', con)

for col in ["amount", "oldbalanceOrig", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]:
    
    df[col] = df[col].apply(string_conversion)

#%%
## 1.1 Data set description 
df.head(10) # gives the first ten rows of the dataset
df.info() # gives overview of columns and datatypes
data_description = df.describe() # create DataFrame that gives statistical description of all variables
data_description.to_csv(r'Users\ted\Desktop\Assignment1.1\Descriptives.csv')

# Check for duplicate rows within the database
if df[df.duplicated()].empty:
    print ("There are no duplicates")
else:
    print ("The duplicate rows are")
    df[df.duplicated()]

# Check for duplicate rows
if df[df.duplicated()].empty:
    print ("There are no duplicates")
else:
    print ("The duplicate rows are")
    df[df.duplicated()]

# Check for null values 
pd.isnull('df')

#%%
## 1.2 Data consistency
# First exploratory check for amount and balance values
# Create function in which all lines of the df are checked for inconsistencies in Origin difference and amount

limiter = 50 
for i in range(0,(limiter-1)): 
     if df.loc[i,'amount'] != abs(df.loc[i,'newbalanceOrig'] - df.loc[i,'oldbalanceOrig']): 
         print ('Amount and Orig difference do not match in row ',i) 

# Further investigation of the differences in the origin accounts
df['origDiff'] = abs(df['newbalanceOrig'] - df['oldbalanceOrig']) # Add a column to df with difference in new and old Origin account

df['checkOrig'] = (df['amount'] - df['origDiff']) # Compare the difference in accounts to suggested difference (amount)

df['destDiff'] = abs(df['newbalanceDest'] - df['oldbalanceDest']) # Add a column to df with difference in new and old Destination account

df['checkDest'] = (df['amount'] - df['destDiff']) # Compare the difference in accounts to suggested difference (amount)

df['abs_Inconsistency_Orig'] = abs(df['amount'] - df['origDiff']) # Calculate absolute inconsistencies in Orig accounts
df['abs_Inconsistency_Dest'] = abs(df['amount'] - df['destDiff']) # Calculate absolute inconsistency in Dest accounts

sum_diff_check = df['abs_Inconsistency_Orig'].sum()-df['abs_Inconsistency_Dest'].sum() # Calculate total amount of 'lost' monetary value

df.value_counts('checkOrig') # How much Origin accounts differ from the amount? And how much do they differ?
df.value_counts('checkDest') # How much Desitnation accounts differ from the amount? And how much do they differ?

#%%
##1.3 Identifying Fraudulent Behavior
#Check accounts that do multiple transactions within the same timestamp
dup_df = df[df.duplicated(['nameOrig', 'timestamp'], keep=False)] #select duplicate rows
dup_df['nameOrig'].value_counts() #shows that ... accounts have sequential transactions
dup_df['nameDest'].value_counts() #shows that ... sequential transactions go to the same account

#Check account balances that do multiple transactions in general
destdup_df = df[df.duplicated(['timestamp', 'nameDest'], keep=False)]
destdup_df = destdup_df.sort_values(by=['timestamp', 'nameDest'])