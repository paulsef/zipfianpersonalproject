import pandas as pd
import numpy as np
import time
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Imputer, LabelEncoder

import pdb

def time(dataframe):
	time = ['registered','recent_date1','recent_date2','recent_date3','recent_date4','recent_date5']
	for col in time:
	    new_series = []
	    hours = []
	    for item in dataframe[col]:
	        if pd.isnull(item):
	            new_series.append(item)
	            continue
	        new_series.append(datetime.fromtimestamp(item))
	    dataframe[col] = new_series
	    if col == 'registered':
	    	hours = []
	    	for item in new_series:
	    		if pd.isnull(item):
	    			hours.append(item)
	    		hours.append(item.strftime('%H'))
	    	dataframe['hour_registered'] = hours
	return dataframe

def nas(dataframe, presence):
	for col in presence:
		for i in dataframe[col].index:
			dataframe[col][i] = 1 if not pd.isnull(dataframe[col][i]) else 0
	#imp = Imputer(missing_values = 'NaN', strategy = 'most_frequent')
	#dataframe['age'] = imp.fit_transform(dataframe['age'])[0]
	dataframe['age'] = dataframe['age'].fillna(dataframe['age'].median())
	return dataframe

def drop(dataframe, dropcolumns):
	'''
	drops unwanted columns and people who haven't listened to 
	more than five songs
	'''
	d = dataframe.drop(dropcolumns, axis = 1)
	d = d.iloc[d.iloc[:,8:].dropna().index,]
	return d

def init_encode(dataframe, test = False, encoder_dict = None):
	'''
	uses sklearn to encode all values as integers/floats
	returns a dictionary containing sklearn encoding objects
	and encoded data frame
	'''
	if not test:
		encoder_dict = {}
	encoded = pd.DataFrame(index = dataframe.index)
	for col in dataframe:
		if test:
			encoder = encoder_dict[col]
			encoded[col] = encoder.transform(dataframe[col])
		else:
			encoder = LabelEncoder()
			encoder_dict[col] = encoder.fit(dataframe[col].tolist())
	 		encoded[col] = encoder.transform(dataframe[col])
	return encoder_dict, encoded

def buildmodel(encoded_df):

def pred_encode(test_df, encoder_dict):
	encoded = pd.DataFrame(index = )
	for col in test_df.columns:






