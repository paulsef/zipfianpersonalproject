import pandas as pd
import numpy as np
import time
import pickle
import random 
import copy
import math
from random import sample
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.preprocessing import Imputer, LabelEncoder, StandardScaler, Normalizer
from sklearn.externals.six import StringIO  
from sklearn import metrics
import pydot
import pdb

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
			dataframe['hour_registered'] = np.array(hours, dtype = float)
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
	dataframe['avg_diff_hours'] = np.array(avg_difference, dtype = float)
	dataframe['use_diff_days'] = np.array(use_diff, dtype = float)
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
			dataframe['gender'][row] = 2
		elif dataframe['gender'][row] == 'm':
			dataframe['gender'][row] = 1
		else:
			dataframe['gender'][row] = 0
	dataframe['gender'] = dataframe['gender'].apply(float)
	dataframe = dataframe.ix[dataframe.iloc[:,8:].dropna().index]
	return dataframe

def drop(dataframe, dropcolumns):
	'''
	drops unwanted columns and people who haven't listened to 
	more than five songs
	'''
	d = dataframe.drop(dropcolumns, axis = 1)
	return d

def logtransform(dataframe, to_transform = []):
	'''
	takes the log transform of certain variables in the dataset
	'''
	for col in to_transform:
		try:
			if np.min(dataframe[col]) <= 0:
					dataframe[col] = dataframe[col] + (-1 * np.min(dataframe[col])) + 1
			dataframe[col] = np.log(dataframe[col])
		except(KeyError):
			continue
	#scrubbed['playcount'] = np.log(scrubbed['playcount'] + 2)
	#scrubbed['use_diff_days'] = np.log(scrubbed['use_diff_days'] + 1)
	return dataframe

def scrub(dataframe, to_drop = None, to_keep = None):
	'''
	scrubs the data set using the time, na,drop functions, and logtransform
	functions
	'''
	# if a drop list was not passed, use defaults
	#presence = ['country','gender']
	d = nas(dataframe)#, presence)
	d = time(d)
	#d = drop(d, to_drop)
	d, top_genres, user_names = reshape(d, to_drop, to_keep)
	tolog = ['playcount', 'use_diff_days', 'top_count1','top_count2', 'top_count3',
			'top_count4','top_count5']
	d = logtransform(d, to_transform = tolog)
	return d, top_genres, user_names

def reshape(dataframe, to_drop = None, to_keep = None):
	genres = []
	colset1 = ['tag1', 'tag2','tag3', 'tag4', 'tag5']
	colset2 = ['top_count1', 'top_count2','top_count3', 'top_count4','top_count5']
	zipped = zip(colset1, colset2)
	top_genres = dataframe['tag1']
	user_names = dataframe['name']
	for col1, col2 in zipped:
		genres += list(dataframe[col1])
	unique_genres = list(set(genres))
	if not to_keep:
		genre_df = pd.DataFrame(columns = unique_genres, index = dataframe.index)
		genre_df = genre_df.fillna(0)
		for col1, col2 in zipped:
			for row in dataframe.index:
				g = dataframe[col1][row]
				genre_df[g][row] += dataframe[col2][row]
		for row in genre_df.index:
			if dataframe['playcount'][row] <= 0:
				dataframe = dataframe.drop(row)
				genre_df = genre_df.drop(row)
				continue
			genre_df.ix[row] = genre_df.ix[row]/dataframe['playcount'][row]
		genre_df = genre_df.applymap(float)
		dummied1 = pd.get_dummies(dataframe['country'])
	else:
		dummied1 = pd.DataFrame(index = dataframe.index)
		genre_df = pd.DataFrame(index = dataframe.index)
	if not to_drop:
		to_drop = ['recent_date1','recent_date2','recent_date3','recent_date4',
					'recent_date5','registered', 'id','name' , 'recent_artist1', 
					'recent_artist2', 'recent_artist3', 'recent_artist4', 'recent_artist5',
					'recent_track1','recent_track2' ,'recent_track3', 'recent_track4','recent_track5',
					'top_artist1','top_artist2','top_artist3','top_artist4','top_artist5', 'country']
	dataframe = drop(dataframe, to_drop + colset1 + colset1)
	genre_df.rename(columns = {'BG':'BG.genre'}, inplace = True)
	#concatenated = pd.concat([dataframe, genre_df, dummied1], axis = 1, ignore_index = True).applymap(float)
	#return concatenated
	#appended = dataframe.append(genre_df).append(dummied1)
	x = pd.merge(dummied1, genre_df, left_index = True, right_index = True)
	z = pd.merge(x, dataframe, left_index = True, right_index = True).applymap(float)
	if to_keep:
		to_drop = list(set(list(z.columns)) - set(to_keep))
		z = drop(z, to_drop)
	return z, top_genres, user_names

def data(to_drop = None, to_keep = None, encode = False, reencode = False):
	'''
	loads in the data set
	'''
	df1 = pd.read_csv('ssvout/0.ssv', na_values='None')
	df1 = df1.append(pd.read_csv('ssvout/5000.ssv', na_values='None'), ignore_index = True)
	df1 = df1.append(pd.read_csv('ssvout/10000.ssv', na_values='None'), ignore_index = True)
	df1 = df1.append(pd.read_csv('ssvout/15000.ssv', na_values='None'), ignore_index = True)
	df1 = df1.append(pd.read_csv('ssvout/20000.ssv', na_values='None'), ignore_index = True)
	df1 = df1.append(pd.read_csv('ssvout/25000.ssv', na_values='None'), ignore_index = True)
	if len(set(list(df1.index))) > 0:
		print 'dropping found duplicates'
		df1 = df1.drop_duplicates(cols = 'id', take_last = True)
	df1.index = df1.ids
	# create a random list to index the train and test set)
	if encode:
		train = scrub(df1.ix[train_index])
		test = scrub(df1.ix[test_index])
		if reencode:
			make_encoder(train, test)
		train = dencode(train)
		test = dencode(test)
	else:
		scrubbed, top_genres, names = scrub(df1, to_drop, to_keep)
		ramsam = random.sample(list(scrubbed.index), len(scrubbed.index))
		break_point = int(len(ramsam)*.7)
		train_index = ramsam[0:break_point]
		test_index = ramsam[break_point:]
		# report the top genres and names for the test set
		top_train_genres = top_genres.ix[train_index]
		top_test_genres = top_genres.ix[test_index]
		test_names = names.ix[test_index]
		# extract the target variables
		targets = scrubbed.ix[train_index, 'subscriber']
		solutions = scrubbed.ix[test_index, 'subscriber']
		scrubbed = drop(scrubbed, ['subscriber'])
		# split the data
		train = scrubbed.ix[train_index]
		test = scrubbed.ix[test_index]
		# normalize the scrubbed data
		norm = StandardScaler()
		norm.fit(scrubbed)
		normtrain = norm.transform(train)
		normtest = norm.transform(test)
		normtrain = pd.DataFrame(normtrain, index = train_index, columns = scrubbed.columns)
		normtest = pd.DataFrame(normtest, index = test_index, columns = scrubbed.columns)
	pickle.dump(norm,file('standarizer.pkl', 'w'))
	return normtrain, targets, normtest, solutions, test, top_test_genres, test_names

def balance(n, train, target):
	subscriber_index = target[target == 1].index
	user_index = target[target == 0].index
	# randomly select users
	chosen = sample(list(user_index), len(subscriber_index)*n)
	# create a new training set with equal parts subsriber and users
	under_trained = train.ix[list(subscriber_index) + chosen]
	under_target = target.ix[list(subscriber_index) + list(chosen)]
	# sanity checky
	print 'sanity check ' + str(sum(under_trained.index != under_target.index))
	return under_trained, under_target

def growforest(training, target, num_trees, to_pickle = False):
	# encoded_target = encoded_df['subscriber']
	# encoded_training = encoded_df.drop('subscriber', axis = 1)
	m = RandomForestClassifier(n_estimators=num_trees, oob_score=True)
	mod = m.fit(training, target)
	if to_pickle:
		pickle.dump(mod, file('rfmodel.pkl'))
		return
	features = zip(mod.feature_importances_, training.columns)
	features = sorted(features, reverse=True)#, key = lambda x:features[0])
	return mod, features


def make_predictions(dataframe, solutions, model = False):
	'''
	takes a data frame or a row from a data frame and 
	predicts the outcome
	'''
	if not model:
		model = pickle.load(file('rfmodel.pkl'))
	#solutions = dataframe['subscriber']
	predictions = model.predict(dataframe)
	sv_score = np.sum(solutions == predictions)*1.0/len(predictions)
	return solutions, predictions, sv_score


def print_tree():
	to_keep = ['playcount','top_count4','top_count5','top_count2','top_count1',
			'top_count3','avg_diff_hours','age','hour_registered','subscriber']
	normtrain, targets, normtest, solutions, test, top_test_genres = data(to_keep = to_keep)
	norm = pickle.load(file('standarizer.pkl'))
	normtrain = pd.DataFrame(norm.inverse_transform(normtrain), 
							index = normtrain.index, columns = normtrain.columns)
	normtrain, targets = balance(1, normtrain, targets)
	dectree = tree.DecisionTreeClassifier(min_samples_split= 10, min_samples_leaf = 2, max_depth =5)
	dectree.fit(normtrain, targets)
	dot_data = StringIO() 
	tree.export_graphviz(dectree, out_file=dot_data, feature_names = normtrain.columns) 
	graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
	graph.write_pdf("example_tree.pdf") 

def main():
	# load the data
	normtrain, targets, normtest, solutions, test, top_test_genres, test_names = data()
	# undersample
	under_train, under_target = balance(1, normtrain, targets)
	# if something terrible happened
	if len(np.intersect1d(list(under_train.index), list(test.index))) > 0:
		pdb.set_trace()
	# make the model
	mod, features = growforest(under_train, under_target, 100)
	# make predictions
	s, predictions, score = make_predictions(test, solutions, model = mod)
	print score, mod.score(test, solutions)
	print metrics.confusion_matrix(solutions, predictions)
	probs = pd.DataFrame(mod.predict_proba(test))[1]
	norm = pickle.load(file('standarizer.pkl'))
	test = pd.DataFrame(norm.inverse_transform(test), index = test.index, columns = test.columns)
	test['probs'] = list(probs)
	test['top_genres'] = list(top_test_genres)
	test['subscriber'] = list(solutions)
	test['user_id'] = list(test.index)
	test['names'] = list(test_names)
	# test = pd.melt(test, id_vars = ['playcount', 'avg_diff_hours','top_count1', 'top_count2',
	# 	'top_count3', 'top_count4','top_count5', 'hour_registered', 'use_diff_days', 'probs',
	# 	'id'])
	test.to_csv('final_test.csv', sep = ',',index = False, na_rep = "None")
	return test, features


if __name__ == '__main__':
	main()





