# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 22:29:29 2018

@author: Ahmet
"""

print("step_5_Print_Results_Start")
from __main__ import *


import time
import datetime

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print ('Model completed', st )
end_time=datetime.datetime.now()

#before pip install xlutils
import xlrd, xlwt
from xlutils.copy import copy as xl_copy

#book = xlwt.Workbook()
prebook= xlrd.open_workbook('model_runs.xls')

sheet_param=max([number_of_neighbors,number_of_trees,number_of_epochs])

sheetname=model_applied+'_'+str(sheet_param)+'_'+test_set_size+'_'+str(X_str)

book=xl_copy(prebook)
sh = book.add_sheet(sheetname)

sh.write(1,0,'Başlangıç' )
sh.write(1,1,'Bitiş' )
sh.write(1,2,'Model Bitiş Süre' )
sh.write(1,3,'Toplam Süre' )

sh.write(2,0,st_start )
sh.write(2,1,st )
diff_time = st_model_end - start_time
sh.write(2,2,str(round((diff_time.seconds/60),2))+' minutes' )
diff_time_total = end_time - start_time
sh.write(2,3,str(round((diff_time_total.seconds/60),2))+' minutes' )

sh.write(3,0,'Parametreler')
sh.write(4,0,'data_years')
sh.write(4,1, str(X_str))
sh.write(5,0,'model_applied')
sh.write(5,1, model_applied)
sh.write(6,0,'test_set_size')
sh.write(6,1, test_set_size)
sh.write(8,0,'last_year_of_data')
sh.write(8,1, last_year_of_data)
sh.write(9,0,'number_of_trees')
sh.write(9,1, number_of_trees)
sh.write(10,0,'number_of_neighbors')
sh.write(10,1, number_of_neighbors)
sh.write(11,0,'num_of_batch_size')
sh.write(11,1, num_of_batch_size)
sh.write(12,0,'number_of_epochs')
sh.write(12,1, number_of_epochs)
sh.write(15,0, 'Precision')
sh.write(15,1, str(round(prf_scores[0],3)) )
sh.write(16,0, 'Recall')
sh.write(16,1, str(round(prf_scores[1],3)))
sh.write(17,0, 'F_score')
sh.write(17,1, str(round(prf_scores[2],3)))
sh.write(18,0 ,'Accuracy')
sh.write(18,1 ,str(round(y_accuracy,3)))

sh.write(20,0 ,'Confusion Matrix')

x_axis=1
y_axis=21

for i in np.nditer(cm):   
    sh.write(y_axis,x_axis,  str(i))
    x_axis=x_axis+1
    if x_axis==6:
        #Satırı yazmayı bitirince alt satıra geçirmek için değişkenleri tazele.
        y_axis=y_axis+1
        x_axis=1

sh.write(27,0 ,'Class Precision')
x_axis=1
y_axis=27
for i in np.nditer(cm.diagonal(0)):   
    sh.write(y_axis,x_axis,  str(round(cm.diagonal(0)[x_axis-1]/cm.sum(axis=0)[x_axis-1],3)))
    x_axis=x_axis+1

sh.write(28,0 ,'Class Recall')
x_axis=1
y_axis=28
for i in np.nditer(cm.diagonal(0)):   
    sh.write(y_axis,x_axis,  str(round(cm.diagonal(0)[x_axis-1]/cm.sum(axis=1)[x_axis-1],3)))
    x_axis=x_axis+1

#print(str(round(cm.diagonal(0)[diag_index]/cm.sum(axis=0)[diag_index],3)))
#print(str(round(cm.diagonal(0)[diag_index]/cm.sum(axis=0)[diag_index],3)))

book.save('model_runs.xls')

