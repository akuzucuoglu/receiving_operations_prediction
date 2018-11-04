#################################################
#################################################
#################################################
#################################################
#################################################
#################################################
#1. Libraries
import pandas as pd
#import matplotlib.pyplot as plt
#2. Initial Work
#my_ds=input('Enter dataset file name:')



my_ds=dataset
my_tv="TOPLAM_SURE_OLUSTURMA_RECEIVE"
#3. Core Work

#1. Descriptive for all dataset
descriptive_all=my_ds.describe(include='all')
descriptive_categoric=my_ds.describe(include='object')
descriptive_numeric=my_ds.describe()


#2. t-Test on Binary Variable
from scipy.stats import ttest_ind

t_test_result_array =  pd.DataFrame( columns=["COLUMN","T_STATISTICS","PVALUE"])
i=0
for column in my_ds:
    if my_ds[column].dtype == 'object': #Kategorik değişkense
        if my_ds[column].value_counts().size<=2:    #Unique değeri 5'ten azsa çizsin
            
            cat1 = my_ds[my_ds[column]==my_ds[column].unique()[0]]
            cat2 = my_ds[my_ds[column]==my_ds[column].unique()[1]]
            
            t_test_result = ttest_ind(cat1[my_tv], cat2[my_tv], equal_var = False)
            t_test_result_array.loc[i]=[column,t_test_result[0],t_test_result[1]]
            i=i+1
            
            
#3. Hist çizdirme
for column in my_ds:
    if my_ds[column].dtype == 'object': #Kategorik değişkense
        if my_ds[column].value_counts().size<=4:    #Unique değeri 5'ten azsa çizsin
            print(column)
            my_ds[my_tv].astype('int64').hist(bins=5,  by=my_ds[column]) #Histogram çizdir paşam

my_ds[my_tv].astype('int64')

#4. Basic Statistics gösterme
mean_of_unique_values =  pd.DataFrame( columns=["COLUMN","VALUE","MEAN","MEDIAN","COUNT"])
i = 0
for column in my_ds:
    if my_ds[column].dtype == 'object': #Kategorik değişkense
        if my_ds[column].value_counts().size<=100:    #Unique değeri 5'ten azsa çizsin
           for unique_val in my_ds[column].unique():
               mean_of_col = my_ds.groupby(column).mean()
               median_of_col = my_ds.groupby(column).median()
               count_of_col = my_ds[column].value_counts()
               mean_of_unique_values.loc[i] = [column,unique_val,mean_of_col[mean_of_col.index==unique_val][my_tv][0],median_of_col[median_of_col.index==unique_val][my_tv][0],count_of_col[count_of_col.index==unique_val][0]]
               i=i+1


#Numeric değişkenler için correlation heatmap
#import seaborn as sns
#sns.heatmap(my_ds.corr())