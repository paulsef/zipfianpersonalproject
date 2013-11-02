from pymongo import MongoClient
import numpy as np
import json
import pdb



def connect():
	'''
	connects to the test database
	and returns the documents 
	'''
	client = MongoClient()
	db = client.test
	collection = db.test
	documents = collection.find()
	return documents

def to_json():
	documents = connect()
	doc_count = documents.count()
	path = 'jsonout/' 
	for i in range(doc_count):
		if i%5000 == 0:
			f_name = str(i) + '.json'
		f = open(path + f_name, 'a')
		json.dump(documents[i],f)
		f.write('\n')
		f.close()

def from_json(filepath):
	''' 
	takes a json file and converts it to 
	'''
	f = open(filepath)
	dictionaries = [json.loads(line) for line in f.readlines()]
	return dictionaries

def flatten_userinfo(entry):
	'''
	takes an entry and flattens the user information
	returns a a flattened dictionary
	'''

	info_dict = entry['getinfo']['user']
	raw_info = [info_dict[i] for i in info_dict.keys()]
	for key in info_dict:
		if key == 'image':
			mask = [False if i == '' else True for i in [im['#text'] for im in info_dict['image']]]
			info_dict[key] = np.any(mask)
		if key == 'registered':
			info_dict[key] = info_dict[key]['unixtime']
	entry['getinfo'] = info_dict
	return entry


def flatten_recenttracks(entry):
	artists = []
	tracks = []
	dates = []
	try:
		track_list = entry['getrecenttracks']['recenttracks']['track']
		if not isinstance(track_list, list):
			track_list = [track_list]
		for t in track_list:
			artists.append(t['artist']['#text'])
			tracks.append(t['name'])
			dates.append(t['date']['uts'])
		num_nones = 5 - len(track_list)
	except(KeyError):
		num_nones = 5
	if num_nones > 0:
		for i in range(num_nones):
			artists.append(None)
			tracks.append(None)
			dates.append(None)
	entry['getrecenttracks'] = {'artists':artists, 'tracks':tracks, 'dates':dates}
	return entry

def flatten_topartist(entry):
	artists = []
	counts = []
	try:
		artist_list = entry['top_artists']['topartists']['artist']
		if not isinstance(artist_list, list):
			artist_list = [artist_list]
		for a in artist_list:
			artists.append(a['name'])
			counts.append(a['playcount'])
		num_nones = 5 - len(artist_list)
	except(TypeError):
		num_nones = 5
	if num_nones > 0:
		for i in range(num_nones):
			artists.append(None)
			counts.append(None)
	entry['top_artists'] = {'artists':artists, 'counts':counts}
	return entry

def flatten_friends(entry):
	try:
		friend_list = entry['getfriends']['friends']['user']
		if isinstance(friend_list, list):
			num_friends = len(friend_list)
		else:
			num_friends = 1
	except(KeyError):
		num_friends = 0
	entry['getfriends'] = num_friends
	return entry

def flatten_events(entry):
	try:
		event_list = entry['getevents']['events']['event']
		if isinstance(event_list, list):
			num_events = len(event_list)
		else:
			num_events = 1
	except(KeyError):
		num_events = 0
	entry['getevents'] = num_events
	return entry

def flatten_toptags(entry):
	tags = entry['top_tags']
	num_nones = 5 - len(tags)
	for i in range(num_nones):
		tags.append(None)
	entry['getTopTags'] = tags
	return entry


def main():
	docs = from_json('jsonout/0.json')
	for doc in docs:
		flatten_toptags(doc)
		flatten_events(doc)
		flatten_friends(doc)
		flatten_topartist(doc)
		flatten_userinfo(doc)
		flatten_recenttracks(doc)
	return docs









if __name__ == '__main__' :
	to_json()



