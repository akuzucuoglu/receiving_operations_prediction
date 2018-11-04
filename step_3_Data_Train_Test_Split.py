# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 22:29:29 2018

@author: Ahmet
"""

#Adım 3: Train Test Split  


dataset.info()


#1. PRED_SET oluşturulur!
if test_set_size=='12'  :
    dataset["PRED_SET"] =0
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL"]==last_year_of_data,"PRED_SET" ]=1
    
elif test_set_size=='9'  :
#train test ayırmak için kullanılıyor
    dataset["PRED_SET"] =0
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'04',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'05',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'06',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'07',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'08',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'09',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'10',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'11',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'12',"PRED_SET" ]=1

elif test_set_size=='6'  :
#train test ayırmak için kullanılıyor
    dataset["PRED_SET"] =0
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'07',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'08',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'09',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'10',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'11',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'12',"PRED_SET" ]=1


elif test_set_size=='3'  :
#train test ayırmak için kullanılıyor
    dataset["PRED_SET"] =0
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'10',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'11',"PRED_SET" ]=1
    dataset.loc[dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]==last_year_of_data+'12',"PRED_SET" ]=1
    

numeric_dataset["PRED_SET"]=dataset["PRED_SET"]


#2. Classification problemleri için Target Variable'da Discretization yapılır.
if model_applied in ("RFC","KNN"):  
    
    #1. Continuous Dependent Variable is Discretized!
    dataset["KATEGORIK_SURE"],bins =pd.qcut(dataset["TOPLAM_SURE_OLUSTURMA_RECEIVE"],5,retbins=True, labels=["0","1","2","3","4"])
    dataset["KATEGORIK_SURE"]=dataset["KATEGORIK_SURE"].astype('str')  
    
    #2. Numeric_dataset'e kategorik süre kolonu eklenir.
    numeric_dataset["KATEGORIK_SURE"] = dataset["KATEGORIK_SURE"]
    numeric_dataset.pop("TOPLAM_SURE_OLUSTURMA_RECEIVE") 

#3. Train Test Split İşlemi Gerçekleşir.
numeric_dataset_train = numeric_dataset[numeric_dataset["PRED_SET"] != 1]
numeric_dataset_test = numeric_dataset[numeric_dataset["PRED_SET"] == 1] 

if model_applied in ("ANN","RFR"):
    useless,bins =pd.qcut(dataset["TOPLAM_SURE_OLUSTURMA_RECEIVE"],5,retbins=True, labels=["0","1","2","3","4"])
    y_train = numeric_dataset_train.pop("TOPLAM_SURE_OLUSTURMA_RECEIVE") #Train Y
    y_test = numeric_dataset_test.pop("TOPLAM_SURE_OLUSTURMA_RECEIVE")   #Test Y
    y_dataset = numeric_dataset.pop("TOPLAM_SURE_OLUSTURMA_RECEIVE")     #Train+Test Y
    
if model_applied in ("RFC","KNN"):
    y_train = numeric_dataset_train.pop("KATEGORIK_SURE")
    y_test = numeric_dataset_test.pop("KATEGORIK_SURE")
    y_dataset = numeric_dataset.pop("KATEGORIK_SURE")
    

       
numeric_dataset_train.pop("PRED_SET")
numeric_dataset_test.pop("PRED_SET") 
