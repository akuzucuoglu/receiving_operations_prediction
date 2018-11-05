# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 23:07:51 2018

@author: Ahmet
"""

from __main__ import *
print("step_1_Data_Importing_Start")

import pandas as pd

#Boş data set oluşturmak için yapıldı.
dataset = pd.read_csv('2010_tedarik.csv',encoding='ISO-8859-1', thousands=',')
dataset.drop(dataset[dataset["SEVKIYAT_OLUSTURMA_YIL"]>0].index, inplace=True)

#son yıl parametre olarak alınır.
#Son X yıldaki veriden analiz yapılır.
X= int(last_year_of_data)
X_str=str(X)    
data_years = int(data_years)

if data_years > 9:
    print ('Max 9 year data exist, code will run with 9 years :) ')
    data_years=9    
elif data_years< 1:
    print ('Min 1 year is required, code will run with 1 year !!) ')
    data_years=1        
    
while data_years>0 : 
       
    dataset=dataset.append(pd.read_csv(X_str+'_tedarik.csv',encoding='ISO-8859-1', thousands=','), ignore_index=True)
    data_years=data_years-1
    X=X-1
    X_str=str(X) 