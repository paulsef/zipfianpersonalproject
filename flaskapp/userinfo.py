from bs4 import BeautifulSoup
import requests
import pdb

def get_image(user_id):
	r = requests.get('http://www.last.fm/user/' + str(user_id))
	soup = BeautifulSoup(r.text)
	image_tag = soup.find(class_ = 'userImage')
	return image_tag

def slice_playcount(dataframe, split_value, greater_than = True):
	'''
	paramters is a dictionary of paramaters, may contain null values
	slice by 'playcount','top_count,'avg_diff_hours','age',
	'hour_registered','subscriber'
	'''
	if greater_than:
		dataframe = dataframe[dataframe['playcount'] > split_value]
	else:
		dataframe = dataframe[dataframe['playcount'] <= split_value]
	return dataframe

def slice_top_count(dataframe, split_value, greater_than = True):
	if greater_than:
		dataframe = dataframe[dataframe['top_count1'] > split_value]
	else:
		dataframe = dataframe[dataframe['top_count1'] <= split_value]
	return dataframe

def slice_avg_diff_hours(dataframe, split_value, greater_than = True):
	if greater_than:
		dataframe = dataframe[dataframe['avg_diff_hours'] > split_value]
	else:
		dataframe = dataframe[dataframe['avg_diff_hours'] <= split_value]
	return dataframe

def slice_age(dataframe, split_value, greater_than = True):
	if greater_than:
		dataframe = dataframe[dataframe['age'] > split_value]
	else:
		dataframe = dataframe[dataframe['age'] <= split_value]
	return dataframe

def slice_hour_reg(dataframe, hour_registered):
	return dataframe[dataframe['hour_registered'] == hour_registered]

def slice_genre(dataframe, genre):
	dataframe = dataframe[dataframe[genre] > .2]
	return dataframe

def error_handling(dataframe, playcount, top_count, avg_diff_hours, age, hour_registered, genre):
	errors = []
	try:
		playcount[0]
		playcount = int(playcount)
	except(ValueError, IndexError):
		playcount = 0
		errors.append(str(playcount) + 'was not a number was not used in the slice')
	try:
		top_count[0]
		top_count = int(top_count)
	except(ValueError, IndexError):
		top_count = 0
		errors.append(str(top_count)+'was not a number was not used in the slice')
	try:
		avg_diff_hours[0]
		avg_diff_hours = int(avg_diff_hours)
	except(ValueError, IndexError):
		top_count = 0
		errors.append(str(avg_diff_hours) + 'was not a number was not used in the slice')
	try:
		age[0]
		age = int(age)
	except(ValueError, IndexError):
		age = 0
		errors.append(str(age) + 'was not a number was not used in the slice')
	try:
		hour_registered[0]
		hour_registered = int(hour_registered)
	except(ValueError, IndexError):
		hour_registered = None
		errors.append(str(hour_registered) + 'was not a number was not used in the slice')
	try:
		genre[0]
		dataframe[genre]
	except(KeyError, IndexError):
		genre = None
		errors.append(str(genre) + 'was not a z valid genre')
	return playcount, top_count, avg_diff_hours, age, hour_registered, genre, errors

def slice_all(dataframe, playcount, top_count,avg_diff_hours, age, hour_registered, genre):
	playcount, top_count, avg_diff_hours, age, hour_registered, genre, errors = error_handling(
												dataframe, playcount, top_count, 
												avg_diff_hours, age,
												hour_registered, genre)
	dataframe = slice_playcount(dataframe, playcount, greater_than = True)
	dataframe = slice_top_count(dataframe, top_count, greater_than = True)
	dataframe = slice_avg_diff_hours(dataframe, avg_diff_hours, greater_than = True)
	dataframe = slice_age(dataframe, age, greater_than = True)
	if hour_registered:
		dataframe = slice_hour_reg(dataframe, hour_registered, greater_than = True)
	if genre:
		dataframe =  slice_genre(dataframe, genre)
	return dataframe, errors


