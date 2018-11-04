# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
ML code for RS Teslimalma Prediction
"""
#import IPython
#app= IPython.Application.instance()
#app.kernel.do_shutdown(True)
#%reset

#import lib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime
import os


##Initialization
number_of_trees = 0
number_of_neighbors = 0
num_of_batch_size = 0
number_of_epochs = 0

last_year_of_data = input("Last year of your data :") 
data_years = input("Which years to include (last X years) Please enter X: ")
test_set_size = input("Preferred test train set ('last Xm') X--> 3,6,9,12 :")
model_applied = input("Preferred model (RFC / RFR / KNN / ANN ) : ")
computer_is_able_to_draw_tree= 'N' #input("Graphviz installed? (Y/N) :") 

ts_start = time.time()
st_start = datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S')
start_time=datetime.datetime.now()


#import step_1_Data_Importing.py
#import step_2_Data_Preprocessing.py
#import step_3_Data_Train_Test_Split.py
#import step_4_Apply_Models.py
#import step_5_Print_Results.py

#Adım 1
#step_1_Data_Importing.py

#Adım 2
#step_2_Data_Preprocessing.py

#Adım 3
#step_3_Data_Train_Test_Split.py

#Adım 4
#step_4_Apply_Models.py

#Adım 5
#step_5_Print_Results.py

