from pymongo import MongoClient
import numpy as np
import pandas as pd
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
	takes a json file and converts it to dictionaries
	'''
	f = open(filepath)
	dictionaries = [json.loads(line) for line in f.readlines()]
	return dictionaries

def flatten_userinfo(entry, master):
	'''
	takes an entry and flattens the user information
	returns a a flattened dictionary
	'''
	info_dict = entry['getinfo']['user']
	if info_dict['age'] == '':
		info_dict['age'] = None
	else:
		info_dict['age'] = int(info_dict['age'])
	if info_dict['country'] = '':
		info_dict['country'] = None
	info_dict['subscriber'] = int(info_dict['subscriber'])
	#info_dict['age'] = int(info_dict['age']) if not info_dict == '' else None
	for key in info_dict:
		if key == 'image':
			mask = [False if i == '' else True for i in [im['#text'] for im in info_dict['image']]]
			info_dict[key] = np.any(mask)
		if key == 'registered':
			info_dict[key] = info_dict[key]['#text']
	master.update(info_dict)
	return master


def flatten_recenttracks(entry, master):
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
			dates.append(t['date']['#text'])
		num_nones = 10 - len(track_list)
	except(KeyError):
		num_nones = 10
	if num_nones > 0:
		for i in range(num_nones):
			artists.append(None)
			tracks.append(None)
			dates.append(None)
	#entry['getrecenttracks'] = {'artists':artists, 'tracks':tracks, 'dates':dates}
	artist_keys = ['recent_artist1','recent_artist2','recent_artist3','recent_artist4',
			'recent_artist5']
	track_keys = ['recent_track1', 'recent_track2','recent_track3', 'recent_track4',
			'recent_track5']
	date_keys = ['recent_date1','recent_date2','recent_date3', 'recent_date4',
			'recent_date5']
	master.update(dict(zip(artist_keys, artists)))
	master.update(dict(zip(track_keys, tracks)))
	master.update(dict(zip(date_keys, dates)))
	#return entry
	return master

def flatten_topartist(entry, master):
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
	artist_keys = ['top_artist1', 'top_artist2', 'top_artist3', 'top_artist4',
			'top_artist5']
	count_keys = ['top_count1', 'top_count2','top_count3', 'top_count4',
			'top_count5']
	master.update(dict(zip(artist_keys, artists)))
	master.update(dict(zip(count_keys, counts)))
	#entry['top_artists'] = {'artists':artists, 'counts':counts}
	#return entry
	return master

def flatten_friends(entry, master):
	try:
		friend_list = entry['getfriends']['friends']['user']
		if isinstance(friend_list, list):
			num_friends = len(friend_list)
		else:
			num_friends = 1
	except(KeyError):
		num_friends = 0
	#entry['getfriends'] = num_friends
	#return entry
	master['friend_count'] = num_friends
	return master


def flatten_events(entry, master):
	try:
		event_list = entry['getevents']['events']['event']
		if isinstance(event_list, list):
			num_events = len(event_list)
		else:
			num_events = 1
	except(KeyError):
		num_events = 0
	#entry['getevents'] = num_events
	#return entry
	master['event_count'] = num_events
	return master


def flatten_toptags(entry, master):
	tags = entry['top_tags']
	num_nones = 5 - len(tags)
	for i in range(num_nones):
		tags.append(None)
	tag_keys = ['tag1', 'tag2','tag3','tag4','tag5']
	master.update(dict(zip(tag_keys, tags)))
	#entry['getTopTags'] = tags
	#return entry
	return master

def create_df(master):
	row_ids = master.keys()
	rows = [master[key] for key in master]

	df = pd.DataFrame(rows, index = row_ids)
	return df



def main():
	docs = from_json('jsonout/0.json')
	super_master = {}
	for doc in docs:
		master = {}
		uid = doc['getinfo']['user']['id']
		flatten_toptags(doc, master)
		flatten_events(doc, master)
		flatten_friends(doc, master)
		flatten_topartist(doc, master)
		flatten_userinfo(doc, master)
		flatten_recenttracks(doc, master)
		super_master[uid] = master
	pd.DataFrame()
	for key in super_master:
		super_master[key]
	return super_master









if __name__ == '__main__' :
	#to_json()
	pass




