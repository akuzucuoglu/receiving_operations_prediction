# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 14:51:49 2018

@author: Ahmet
"""


#1. Libraries
import pandas as pd

#2. Initial Work
#my_ds=input('Enter dataset file name:')
#my_tv=input('Enter target variable name:')

my_ds=dataset
my_tv="KATEGORIK_SURE" #"TOPLAM_SURE_OLUSTURMA_RECEIVE"
#3. Core Work


# Descriptive for all dataset
descriptive_all=my_ds.describe(include='all')
descriptive_categoric=my_ds.describe(include='object')
descriptive_numeric=my_ds.describe()

# Column üzerinde gezerek 
for column in my_ds:
    if my_ds[column].dtype == 'object': #Kategorik değişkense
        if my_ds[column].value_counts().size<=4:    #Unique değeri 5'ten azsa çizsin
            my_ds[my_tv].hist(bins=100,  by=my_ds[column]) #Histogram çizdir paşam


#Unique values of variables.
desc1_country=my_ds["COUNTRY"].value_counts() #To get as array: my_ds["COUNTRY"].unique()
desc1_city=my_ds["CITY"].value_counts()
desc1_yurt_ici_disi=my_ds["YURT_ICI_DISI"].value_counts()
desc1_satinalmaci_id_new=my_ds["SATINALMACI_ID_NEW"].


#Histogram için kullanılan kodlar
my_ds[my_tv].describe()
my_ds[my_tv].hist(bins=200)
my_ds[my_tv].hist(bins=100,  by=my_ds["SATINALMACI_ID_NEW"])
#my_ds[my_tv].hist(bins=100, by=my_ds["COUNTRY"] )

my_ds.groupby('YURT_ICI_DISI').mean()
#Student t-Test on Yurt içi Dışı

from scipy.stats import ttest_ind

cat1 = my_ds[my_ds['YURT_ICI_DISI']=='Yurt içi']
cat2 = my_ds[my_ds['YURT_ICI_DISI']=='Yurt dışı']

t_test_result=ttest_ind(cat1[my_tv], cat2[my_tv], equal_var = False)


#Mean of TOPLAM_SURE_OLUSTURMA by country
country_based_mean=my_ds.groupby('SATINALMACI_ID_NEW').mean()
desc2_satinalmaci_id_new=round(country_based_mean["TOPLAM_SURE_OLUSTURMA_RECEIVE"],2)

my_ds["SATINALMACI_ID_NEW"].value_count()

#
import seaborn as sns
sns.heatmap(my_ds.corr())




