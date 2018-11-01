# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 01:06:45 2018

@author: Ahmet
"""

# Model_1. Random Forest Classifier
if model_applied=='RFC'  :
    
    number_of_trees = int(input("How many decision trees do you want to use in your model: "))
       
    from sklearn.ensemble import RandomForestClassifier
    classifier = RandomForestClassifier(n_estimators = number_of_trees, random_state = 5, criterion="entropy")
    classifier.fit(numeric_dataset_train, y_train)
    
    y_pred = classifier.predict(numeric_dataset_test)
    
    #Feature Importance
    feature_importance = classifier.feature_importances_
    feature_importance_sorted = np.sort(feature_importance)
    
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
    y_accuracy=sum(cm.diagonal())/len(y_test.index)
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print (' ')
    print (' ')
    print ('Accuracy is', y_accuracy, st )
    print (cm)
    
    st_model_end =datetime.datetime.now()
    
    #Graphviz installed or not?
    if computer_is_able_to_draw_tree =='Y':
            
        #RFC'deki ilk ağacı çizdirir. Diğer ağaçları görmek için 0 parametresini değiştirebiliriz.
        estimator = classifier.estimators_[0]
            
        from sklearn.tree import export_graphviz
        # Export as dot file
        export_graphviz(estimator, out_file='tree_of_rfc.dot')#, 
                        #feature_names = numeric_dataset.columns,
                        #class_names = "KATEGORIK_SURE",
                        #rounded = True, proportion = False, 
                        #precision = 2, filled = True)
                        
        #PATH belirlemek için bu kodu kullanabiliriz. Admin yetkisi alınmalı.
        #import os    
        #os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'             
        
        #DOT dosyası PNG'ye çevrilir.
        import pydot    
        (graph,) = pydot.graph_from_dot_file('tree_of_rfc.dot')
        graph.write_png('tree_of_rfc.png')     
        
    
    from sklearn.metrics import precision_recall_fscore_support
    prf_scores=precision_recall_fscore_support(y_test, y_pred, average='macro')
        
# Model_2. Random Forest Regression
elif model_applied=='RFR' :  
    
    number_of_trees = int(input("How many decision trees do you want to use in your model: "))
    
    from sklearn.ensemble import RandomForestRegressor
    regressor = RandomForestRegressor(n_estimators = number_of_trees, random_state = 5, criterion="mse")
    regressor.fit(numeric_dataset_train, y_train)
    y_pred = regressor.predict(numeric_dataset_test)
    #Errors
    from sklearn.metrics import mean_squared_error
    from math import sqrt
    rms = sqrt(mean_squared_error(y_pred, y_test))
    mae = np.average( abs(y_pred - y_test))/np.average(y_test)
 
    
    
    my_array = [i for i in np.arange(0,y_pred.size,1)]
    y_pred_categorical = pd.DataFrame(index=my_array, columns=["TOPLAM_SURE_OLUSTURMA_RECEIVE"])
    y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"] = y_pred
    
    y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]=pd.to_numeric(y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"])
      
    y_pred_categorical["KATEGORIK_SURE"] = ""
    y_pred_categorical.loc[y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[1],"KATEGORIK_SURE" ]= 1
    y_pred_categorical.loc[(y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[2]) & (y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[1]),"KATEGORIK_SURE"] = 2
    y_pred_categorical.loc[(y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[3]) & (y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[2]),"KATEGORIK_SURE"] = 3
    y_pred_categorical.loc[(y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[4]) & (y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[3]),"KATEGORIK_SURE"] = 4
    y_pred_categorical.loc[(y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[4]),"KATEGORIK_SURE"] = 5
    
    y_pred_categorical["KATEGORIK_SURE"]=pd.to_numeric(y_pred_categorical["KATEGORIK_SURE"])
    
    
    y_test_categorical = pd.DataFrame(index=(y_test.index), columns=["TOPLAM_SURE_OLUSTURMA_RECEIVE"])
    y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"] = y_test
    
    y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]=pd.to_numeric(y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"])
    
    y_test_categorical["KATEGORIK_SURE"] = ""
    y_test_categorical.loc[y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[1],"KATEGORIK_SURE" ]= 1
    y_test_categorical.loc[(y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[2]) & (y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[1]),"KATEGORIK_SURE"] = 2
    y_test_categorical.loc[(y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[3]) & (y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[2]),"KATEGORIK_SURE"] = 3
    y_test_categorical.loc[(y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[4]) & (y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[3]),"KATEGORIK_SURE"] = 4
    y_test_categorical.loc[(y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[4]),"KATEGORIK_SURE"] = 5
    
    #Hatalı gibi geldi --- y_test_categorical.drop(y_test_categorical[y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"].isnull()].index, inplace=True)
    y_test_categorical["KATEGORIK_SURE"]=pd.to_numeric(y_test_categorical["KATEGORIK_SURE"])
    
        
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test_categorical["KATEGORIK_SURE"] ,y_pred_categorical["KATEGORIK_SURE"])
    y_accuracy=sum(cm.diagonal())/len(y_test_categorical.index)

    from sklearn.metrics import precision_recall_fscore_support
    prf_scores=precision_recall_fscore_support(y_test_categorical["KATEGORIK_SURE"], y_pred_categorical["KATEGORIK_SURE"], average='macro')


    #Feature Importance
    feature_importance = regressor.feature_importances_
    feature_importance_sorted = np.sort(feature_importance)
    
    st_model_end =datetime.datetime.now()
     
#Model_3. K Nearest Neighbors
elif model_applied=='KNN' :
    
    number_of_neighbors = int(input("How many neighbors do you want to use in your model: "))
    

    # Fitting K-NN to the Training set
    from sklearn.neighbors import KNeighborsClassifier
    classifier = KNeighborsClassifier(n_neighbors = number_of_neighbors, metric = 'minkowski', p = 2)
    classifier.fit(numeric_dataset_train, y_train)
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print (' ')
    print (' ')
    print ('KNN Fit phase completed', st )
    
    # Predicting the Test set results
    y_pred = classifier.predict(numeric_dataset_test)
    
    # Making the Confusion Matrix
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
    y_accuracy=sum(cm.diagonal())/len(y_test.index)
    print (' ')
    print (' ')
    print ('Accuracy is', y_accuracy )
    print (cm)
    
    st_model_end =datetime.datetime.now()
    
#Model_4. Artificial Neural Network 
elif model_applied=='ANN' :
    
    num_of_batch_size = int(input("What is your batch size: "))
    number_of_epochs  = int(input("How many epochs do you want to use in your model: "))
      
    import keras
    from keras.models import Sequential
    from keras.layers import Dense
    
    # Initialising the ANN
    ann_model = Sequential()
    
    #get dataframe number of columns    
    count_col=len(numeric_dataset_test.columns)
    count_output=round((count_col+1)/2)
    
    # Adding the input layer and the first hidden layer
    ann_model.add(Dense(output_dim =count_output , init = 'uniform', activation = 'relu', input_dim = count_col))

    # Adding the second hidden layer
    ann_model.add(Dense(output_dim = count_output, init = 'uniform', activation = 'relu'))
    
    ann_model.add(Dense(output_dim = count_output, init = 'uniform', activation = 'relu'))
    
    
    
    # Adding the second hidden layer
    #ann_model.add(Dense(output_dim = 73, init = 'uniform', activation = 'relu'))
    
    # Adding the output layer
    ann_model.add(Dense(output_dim = 1, init = 'uniform'))
    
    # Compiling the ANN
    ann_model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['mae'])
    
    # Fitting the ANN to the Training set
    ann_model.fit(numeric_dataset_train, y_train, batch_size = num_of_batch_size, nb_epoch = number_of_epochs)
    
    y_pred = ann_model.predict(numeric_dataset_test)
    

    
    y_pred_categorical = pd.DataFrame(index=(y_test.index), columns=["TOPLAM_SURE_OLUSTURMA_RECEIVE"])
    y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"] = y_pred
    y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]=pd.to_numeric(y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"])
    
    
    y_pred_categorical["KATEGORIK_SURE"] = ""
    y_pred_categorical.loc[y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[1],"KATEGORIK_SURE" ]= 1
    y_pred_categorical.loc[(y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[2]) & (y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[1]),"KATEGORIK_SURE"] = 2
    y_pred_categorical.loc[(y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[3]) & (y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[2]),"KATEGORIK_SURE"] = 3
    y_pred_categorical.loc[(y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[4]) & (y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[3]),"KATEGORIK_SURE"] = 4
    y_pred_categorical.loc[(y_pred_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[4]),"KATEGORIK_SURE"] = 5
    
    y_pred_categorical["KATEGORIK_SURE"]=pd.to_numeric(y_pred_categorical["KATEGORIK_SURE"])
    
    y_test_categorical = pd.DataFrame(index=(y_test.index), columns=["TOPLAM_SURE_OLUSTURMA_RECEIVE"])
    y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"] = y_test
    
    y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]=pd.to_numeric(y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"])
    
    y_test_categorical["KATEGORIK_SURE"] = ""
    y_test_categorical.loc[y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[1],"KATEGORIK_SURE" ]= 1
    y_test_categorical.loc[(y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[2]) & (y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[1]),"KATEGORIK_SURE"] = 2
    y_test_categorical.loc[(y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[3]) & (y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[2]),"KATEGORIK_SURE"] = 3
    y_test_categorical.loc[(y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=bins[4]) & (y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[3]),"KATEGORIK_SURE"] = 4
    y_test_categorical.loc[(y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>bins[4]),"KATEGORIK_SURE"] = 5
    
    y_test_categorical.drop(y_test_categorical[y_test_categorical["TOPLAM_SURE_OLUSTURMA_RECEIVE"].isnull()].index, inplace=True)
    y_test_categorical["KATEGORIK_SURE"]=pd.to_numeric(y_test_categorical["KATEGORIK_SURE"])
    
    
    #Feature Importance
    feature_importance_cat = classifier.feature_importances_
    feature_importance_sorted_cat = np.sort(feature_importance_cat)
    
    
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test_categorical["KATEGORIK_SURE"] ,y_pred_categorical["KATEGORIK_SURE"])
    y_accuracy=sum(cm.diagonal())/len(y_test_categorical.index)
    
    from sklearn.metrics import precision_recall_fscore_support
    prf_scores=precision_recall_fscore_support(y_test_categorical["KATEGORIK_SURE"], y_pred_categorical["KATEGORIK_SURE"], average='macro')

    
    print (' ')
    print (' ')
    print ('Accuracy is', y_accuracy )
    print (cm)

    st_model_end =datetime.datetime.now()     

else :
    print ('No available model. Please select appropriate model.' )