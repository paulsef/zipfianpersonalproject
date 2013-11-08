import pandas as pd
import numpy as np
import time
import pickle
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Imputer, LabelEncoder

import pdb

def time(dataframe):
	'''
	converts columns to time
	'''
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
	'''
	checks certain features for presence
	imputes age based on median
	'''
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

def scrub(dataframe):
	'''
	scrubs the data set using the time, na, and drop functions
	'''
	to_drop = ['recent_date1','recent_date2','recent_date3','recent_date4','recent_date5', 'playcount', 'registered', 'id']
	presence = ['country','gender']
	d = time(dataframe)
	d = drop(d, to_drop)
	d = nas(d, presence)
	return d

def make_encoder():
	'''
	creates a general label encoder for every
	unique value of all categorical variables
	'''
	# load in the whole dataset
	df1 = pd.read_csv('ssvout/0.ssv', na_values='None')
	df1 = df1.append(pd.read_csv('ssvout/5000.ssv', na_values='None'), ignore_index = True)
	df1 = df1.append(pd.read_csv('ssvout/10000.ssv', na_values='None'), ignore_index = True)
	df1 = df1.append(pd.read_csv('ssvout/15000.ssv', na_values='None'), ignore_index = True)
	df1 = df1.append(pd.read_csv('ssvout/20000.ssv', na_values='None'), ignore_index = True)
	# scrube the data
	df1 = scrub(df1)
	# initialize the encoder and a list to store all categorical values
	encoder = LabelEncoder()
	values = []
	cols = []
	for col in df1:
		cols.append(col)
		for value in df1[col]:
			values.append(value)
	encoder.fit(values)
	pickle.dump(encoder, file('./encoder.pkl', 'w'))




def encode(dataframe):
	'''
	uses sklearn to encode all values as integers/floats
	returns a dictionary containing sklearn encoding objects
	and encoded data frame
	'''
	encoder = pickle.load(file('./encoder.pkl'))
	encoded = pd.DataFrame(index = dataframe.index)
	for col in dataframe:
		#if col == 'age':
		#	continue
		pdb.set_trace()
		print col
		values = []
		for value in dataframe[col]:
			values.append(encoder.transform([value])[0])
		endoed[col] = values
	return encoded

def buildmodel(encoded_df):
	pass








