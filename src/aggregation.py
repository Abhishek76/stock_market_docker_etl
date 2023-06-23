#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from datetime import datetime
import numpy as np
from scipy import stats
from time import time  , sleep, strftime , gmtime
from testing import *

print('Waiting for the data server...')
sleep(10)
print('ETL Starting...')

df = pd.read_csv("./output/out.csv")
print(df.size)

df['Dates'] = pd.to_datetime(df['date']).dt.date
df['Time'] = pd.to_datetime(df['date']).dt.time
df['Month'] = pd.to_datetime(df['date']).dt.month
df['Dayofweek'] = pd.to_datetime(df['date']).dt.dayofweek
df['Year'] = pd.to_datetime(df['date']).dt.year


df_time = df.groupby(['Time','country']).aggregate({'demand':  "mean", "supply":  "mean","demand_supply_gap": "mean","price": "mean",}).reset_index()
df_month = df.groupby(['Month','country']).aggregate({'demand':  "mean", "supply":  "mean","demand_supply_gap": "mean","price": "mean",}).reset_index()
df_Dayofweek = df.groupby(['Dayofweek','country']).aggregate({'demand':  "mean", "supply":  "mean","demand_supply_gap": "mean","price": "mean",}).reset_index()
df_year_mean = df.groupby(['Year','country']).aggregate({'demand':  "mean", "supply":  "mean","demand_supply_gap": "mean","price": "mean",}).reset_index()
df_year_sum = df.groupby(['Year','country']).aggregate({'demand':  "sum", "supply":  "sum","demand_supply_gap": "mean","price": "sum",}).reset_index()
                                                                                

def test_output (df,index,outputdf): 
    test_fail = 0

    if test_null_values_in_data(df) == 0 : print ('no null')
    else :
        print('null is there')
        test_fail +=1 

    if test_duplicated_index(df,index) == 0 : print ('no duplicates')
    else :
        print('duplicate is there')
        test_fail +=1 

    if test_fail == 0 : df.to_csv('./output/{0}.csv'.format(outputdf))
    else : print('there is error in the data no output generated') 

test_output (df= df_time,index = ['Time','country'],outputdf = "df_time")
test_output (df= df_month,index = ['Month','country'],outputdf = "df_month")
test_output (df= df_Dayofweek,index = ['Dayofweek','country'],outputdf = "df_Dayofweek")
test_output (df= df_year_mean,index = ['Year','country'],outputdf = "df_year_mean")
test_output (df= df_year_sum,index = ['Year','country'],outputdf = "df_year_sum")

#print(df)



