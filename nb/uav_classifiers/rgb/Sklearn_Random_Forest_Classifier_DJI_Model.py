#!/usr/bin/env python

import pandas as pd
import csv
import numpy as np
import argparse
import pdb
import pickle
from random import sample
from sklearn import cross_validation
from sklearn import metrics
from sklearn.metrics import explained_variance_score, mean_squared_error, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold
from pprint import pprint

filepath = input("Please enter the filepath: ")
input_table_name = input("Please enter the name of the input table (without extension): ")
input_table = filepath + "\\" + input_table_name + ".csv"
result_table = filepath + "\\" + input_table_name + "_Result.csv"
sort_table = filepath + "\\" + input_table_name + "_Result_Sorted.csv"
picklefile = filepath + "\\" + input_table_name + "_Result.p"

# main routine
def main():
    df = pd.read_csv(input_table, header = 0)
    jDa = df.replace([np.inf, -np.inf], np.nan).copy()
    df1a = jDa.dropna()
    
    # read and define train table, then extract the 'class' column
    input_table_temp = df1a[['class','red','green', 'blue']]
    
    # get class value, then convert value to integer
    target_temp_1 = input_table_temp[['class']].astype(int)
    target_temp_2 = target_temp_1.values
    Y_1 = target_temp_2.ravel()
    
    # select out the predictor variables    
    X_1 = input_table_temp[['red','green', 'blue',]]
    
    """# randomly select 80% of the data for modelling and 20% of the data for corss validation, random_state = 42 for reproducible result
    X_1, X_2, Y_1, Y_2 = cross_validation.train_test_split(train, target, train_size = 0.99) # X_1 = train_features, X_2 = test_features, Y_1 = train_class_value, Y_2 = test_class_value
    print("Number of training data points selected: ", X_1.shape)
    print("Number of testing data ponts selected: ", X_2.shape, "\n")
    print("Running Random Forest Classifier... \n")"""
    
    # run random forest classifier
    # 1. instantiate model with 1024 decision trees
    rf = RandomForestClassifier(n_estimators=512, max_features='log2', bootstrap=True, oob_score=True, n_jobs=-1)
    
    # 2. train the model on training data, remember for above lines: X_1 = train_features, Y_1 = train_class_value 
    rfc = rf.fit(X_1, Y_1)
    #results = rfc.predict(X_2)    
    
    # calculate feature importance
    feature_importances = list(rf.feature_importances_)
    fi = enumerate(rf.feature_importances_)
    cols = X_1.columns 
    fiResult = [(value,cols[i]) for (i,value) in fi]
    fiResult = np.array(fiResult)
    score = np.float64(fiResult[:,0])
    band = fiResult[:,1]
    a = fiResult[np.argsort(fiResult[:, 1])]
    
    # output feature importance to a csv table
    df2 = pd.DataFrame(dict(band = band,n = score))
    df2.apply(pd.to_numeric, errors="error")
    ind = np.arange(len(df2))
    dfsort = df2.sort_values(by = 'n', ascending=[False], na_position='first')
    dfsort.to_csv(sort_table)
    print("Feature Importance Table: ")
    print(dfsort, "\n")
    
    
    # print the accuracy of random forest classifier
    #r2 = rf.score(X_2, Y_2, sample_weight = None)
    #print("Accuracy = {:0.4f}%.".format(r2), "\n")
    
    # print the parametre of the classifier
    print("Parametres currently in use: \n")
    pprint(rf.get_params())
    print("\n")
    
    # output random forest classifier result to a csv table
    #df_p = pd.DataFrame(results)
    #df_o = pd.DataFrame(Y_2)
    #df_r = pd.concat([df_p, df_o], axis=1)
    #df_r.to_csv(result_table)
    #print(df_r)
    
    #output random forest classifier result to a Pickle file 
    with open(picklefile, 'wb') as f:
        pickle.dump(rfc, f)
    print("The Pickle file has been outputed to: ", str(picklefile))   

    
if __name__=="__main__":
    main()        
    