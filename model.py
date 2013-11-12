import pandas as pd
import numpy as np
import time
import pickle
import random 
import copy
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Imputer, LabelEncoder

import pdb

def time(dataframe):
	'''
	converts columns to time
	'''
	time = ['registered','recent_date1','recent_date2','recent_date3',
			'recent_date4','recent_date5']
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
	avg_difference = []
	use_diff = []
	time = np.array(time)
	for row in dataframe.index:
		dates = dataframe.ix[row, time[time != 'registered']]
		#if np.any(pd.isnull(dates)):
		#	pdb.set_trace()
		tdelta1 = (max(dates) - min(dates))/(len(dates)-1)
		avg_difference.append((tdelta1.total_seconds())/(60*60))
		tdelta2 = dataframe.ix[row, 'recent_date1'] - dataframe.ix[row, 'registered']
		use_diff.append(tdelta2.total_seconds()/(60*60*24))
	dataframe['avg_diff_hours'] = avg_difference
	dataframe['use_diff_days'] = use_diff
	return dataframe

def nas(dataframe, presence = None, old = False):
	'''
	checks certain features for presence
	imputes age based on median
	drops (some) incomplete rows
	'''
	if old:
		for col in presence:
			for i in dataframe[col].index:
				dataframe[col][i] = 1 if not pd.isnull(dataframe[col][i]) else 0
	#imp = Imputer(missing_values = 'NaN', strategy = 'most_frequent')
	#dataframe['age'] = imp.fit_transform(dataframe['age'])[0]
	dataframe['age'] = dataframe['age'].fillna(dataframe['age'].median())
	for row in dataframe['gender'].index:
		if dataframe['gender'][row] == 'f':
			dataframe['gender'][row] == 2
		elif dataframe['gender'][row] == 'm':
			dataframe['gender'][row] == 1
		else:
			dataframe['gender'][row] == 0
	dataframe = dataframe.ix[dataframe.iloc[:,8:].dropna().index]
	return dataframe

def drop(dataframe, dropcolumns):
	'''
	drops unwanted columns and people who haven't listened to 
	more than five songs
	'''
	d = dataframe.drop(dropcolumns, axis = 1)
	return d

def scrub(dataframe, to_drop = None):
	'''
	scrubs the data set using the time, na, and drop functions
	'''
	# if a drop list was not passed, use defaults
	if not to_drop:
		to_drop = ['recent_date1','recent_date2','recent_date3','recent_date4',
					'recent_date5','registered', 'id','name' , 'recent_artist1', 
					'recent_artist2', 'recent_artist3', 'recent_artist4', 'recent_artist5']
	#presence = ['country','gender']
	d = nas(dataframe)#, presence)
	d = time(d)
	d = drop(d, to_drop)
	d = reshape(d)
	return d

def make_encoder(test, train):
	'''
	creates a general label encoder for every
	unique value of all categorical variables
	'''
	# load in the whole dataset
	# df1 = pd.read_csv('ssvout/0.ssv', na_values='None')
	# df1 = df1.append(pd.read_csv('ssvout/5000.ssv', na_values='None'), ignore_index = True)
	# df1 = df1.append(pd.read_csv('ssvout/10000.ssv', na_values='None'), ignore_index = True)
	# df1 = df1.append(pd.read_csv('ssvout/15000.ssv', na_values='None'), ignore_index = True)
	# df1 = df1.append(pd.read_csv('ssvout/20000.ssv', na_values='None'), ignore_index = True)
	# scrube the data
	# df1 = scrub(df1)
	# initialize the encoder and a list to store all categorical values
	df1 = train
	df1 = train.append(test, ignore_index = True)
	encoder = LabelEncoder()
	values = []
	cols = []
	for col in df1:
		cols.append(col)
		for value in df1[col]:
			values.append(value)
	encoder.fit(values)
	pickle.dump(encoder, file('./encoder.pkl', 'w'))

def dencode(dataframe, one_off = False, decode = False):
	'''
	uses sklearn to encode all values as integers/floats
	returns a dictionary containing sklearn encoding objects
	and encoded data frame
	'''
	encoder = pickle.load(file('./encoder.pkl'))
	if one_off:
		if decode:
			return encoder.inverse_transform([dataframe])
		else:
			return encoder.transform([dataframe])
	result = pd.DataFrame(index = dataframe.index)
	for col in dataframe:
		if decode:
			result[col] = encoder.inverse_transform(dataframe[col])
		else:
			str_values = [str(i) for i in dataframe[col]]
			result[col] = encoder.transform(str_values)
	return result

def growforest(encoded_df, num_trees, to_pickle = False):
	encoded_target = encoded_df['subscriber']
	encoded_training = encoded_df.drop('subscriber', axis = 1)
	m = RandomForestClassifier(n_estimators=num_trees, oob_score=True)
	mod = m.fit(encoded_training, encoded_target)
	if to_pickle:
		pickle.dump(mod, file('rfmodel.pkl'))
		return
	features = zip(mod.feature_importances_, encoded_df.columns)
	features = sorted(features, reverse=True)#, key = lambda x:features[0])
	return mod, features


def make_predictions(dataframe, model = False):
	'''
	takes a data frame or a row from a data frame and 
	predicts the outcome
	'''
	if not model:
		model = pickle.load(file('rfmodel.pkl'))
	solutions = dataframe['subscriber']
	predictions = model.predict(dataframe.drop('subscriber', axis = 1))
	sv_score = np.sum(solutions == predictions)*1.0/len(predictions)
	return solutions, predictions, sv_score

def data(to_drop = None, encode = True, reencode = False):
	'''
	loads in the data set
	'''
	df1 = pd.read_csv('ssvout/0.ssv', na_values='None')
	#df1 = df1.append(pd.read_csv('ssvout/5000.ssv', na_values='None'), ignore_index = True)
	#df1 = df1.append(pd.read_csv('ssvout/10000.ssv', na_values='None'), ignore_index = True)
	#df1 = df1.append(pd.read_csv('ssvout/15000.ssv', na_values='None'), ignore_index = True)
	#df1 = df1.append(pd.read_csv('ssvout/20000.ssv', na_values='None'), ignore_index = True)
	#df1 = df1.append(pd.read_csv('ssvout/25000.ssv', na_values='None'), ignore_index = True)
	#df1 = df1.drop_duplicates(cols = 'id', take_last = True)
	
	ramsam = random.sample(list(df1.index), len(df1.index))
	break_point = int(len(ramsam)*.7)
	train_index = ramsam[0:break_point]
	test_index = ramsam[break_point:]
	if encode:
		train = scrub(df1.ix[train_index])
		test = scrub(df1.ix[test_index])
		if reencode:
			make_encoder(train, test)
		train = dencode(train)
		test = dencode(test)
	else:
		train = scrub(df1.ix[train_index])
		test = scrub(df1.ix[test_index])
		#train = df1.ix[train_index]
		#test = df1.ix[test_index]


	return train, test

def reshape(dataframe):
	genres = []
	colset1 = ['tag1', 'tag2','tag3', 'tag4', 'tag5']
	colset2 = ['top_count1', 'top_count2','top_count3', 'top_count4','top_count5']
	zipped = zip(colset1, colset2)
	for col1, col2 in zipped:
	    genres += list(dataframe[col1])
	unique_genres = list(set(genres))
	genre_df = pd.DataFrame(columns = unique_genres, index = dataframe.index)
	genre_df = genre_df.fillna(0)
	for col1, col2 in zipped:
		for row in dataframe.index:
			g = dataframe[col1][row]
			genre_df[g][row] += dataframe[col2][row]
			g = 0
	dummied1 = pd.get_dummies(dataframe['country'])
	concatenated = pd.concat([dataframe, genre_df, dummied1])
	concatenated = concatenated.drop(colset1+colset2, axis = 1)
	return concatenated











