import numpy as np
import pandas as pd
import random
import os
import json
from pymongo import MongoClient
import pdb
from users.txt import 


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
	rand = random.sample(range(doc_count), doc_count)
	i = 0
	for random_index in rand:
		if i%5000 == 0:
			print i
			f_name = str(i) + '.json'
		i += 1
		f = open(path + f_name, 'a')
		json.dump(documents[random_index],f)
		f.write('\n')
		f.close()

def from_json(filepath):
	''' 
	takes a json file and converts it to dictionaries
	'''
	f = open(filepath)
	dictionaries = [json.loads(line) for line in f.readlines()]
	return dictionaries

def graph(list_of_dicts):
	f = file('graph.txt', 'a')
	#w_friends = [i for i in list_of_dicts if len(i['getfriends']['friends'].keys()) < 5]
	for doc in list_of_dicts:
		try:
			if 'user' not in doc['getfriends']['friends'].keys():
				continue
			friend_list = doc['getfriends']['friends']['user']
		except(KeyError):
			continue
		if isinstance(friend_list, dict):
			friend_list = [friend_list]
		try:
			for friend in friend_list:
				text = str(doc['getinfo']['user']['id'] + '\t' + friend['id'])
				f.write(text)
				f.write('\n')
		except(KeyError):
			continue
	f.close()


def flatten_userinfo(entry, master):
	'''
	takes an entry and flattens the user information
	returns a a flattened dictionary
	'''
	info_dict = entry['getinfo']['user']
	# convert to proper data types
	if info_dict['country'] == '':
		info_dict['country'] = None
	if info_dict['gender'] == 'n':
		info_dict['gender'] = None
	if info_dict['age'] == '':
		info_dict['age'] = None	
	else:
		info_dict['age'] = int(info_dict['age'])
	for key in ['subscriber','playcount', 'playlists']:
		info_dict[key] = int(info_dict[key])
	info_dict['subscriber'] = int(info_dict['subscriber'])
	for key in info_dict:
		# convert image info to bool
		if key == 'image':
			mask = [False if i == '' else True for i in [im['#text'] for im in info_dict['image']]]
			info_dict[key] = np.any(mask)
		# get the text version of timestamp	
		if key == 'registered':
			info_dict[key] = info_dict[key]['unixtime']
	# delte irrelevant thingssss
	for delete in ['name', 'type','url','bootstrap','realname']:	
		del info_dict[delete]
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
			dates.append(t['date']['uts'])
		num_nones = 10 - len(track_list)
	except(KeyError, TypeError):
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

def flatten_friends(entry, master = None, tomod = False):
	try:
		friend_list = entry['getfriends']['friends']['user']
		if isinstance(friend_list, dict):
			friend_list = [friend_list]
		num_friends = len(friend_list)
		friend_sub = len([friend for friend in friend_list if friend['subscriber'] == '1'])
		id_list = 
	except(KeyError):
		num_friends = 0
		friend_sub = 0
	#entry['getfriends'] = num_friends
	#return entry
	if tomod:
		if num_friends > 0:
			id_list = [friend['id'] for friend in friend_list]
			add_new_subscribers(new_users)
			return
	master['friend_count'] = num_friends
	master['friend_sub'] = friend_sub
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


def main(infile):
	'''
	takes a json file and returns a data pandas DataFrame
	'''
	docs = from_json(infile)
	super_master = []
	for doc in docs:
		master = {}
		try:
			flatten_toptags(doc, master)
			flatten_events(doc, master)
			flatten_friends(doc, master)
			flatten_topartist(doc, master)
			flatten_userinfo(doc, master)
			flatten_recenttracks(doc, master)
			super_master.append(master)
		except(KeyError):
			continue
		for key in master:
			if isinstance(master[key], unicode):
				master[key] = master[key].encode('ascii','replace')
				if ',' in master[key]:
					split = master[key].split(',')
					master[key] = ''.join(split)
	df = pd.DataFrame(super_master)
	return df


if __name__ == '__main__' :
	for filename in os.listdir('jsonout'):
		dict_list = from_json('jsonout/' + filename)
		#graph(dict_list)
		# print filename
		df = main('jsonout/' + filename)
		outfilename = filename.split('.')[0] + '.ssv'
		df.to_csv('ssvout/' + outfilename, sep = ',',index = False, na_rep = "None")#encoding = 'utf-16'	




