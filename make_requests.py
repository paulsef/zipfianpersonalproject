import random
import requests
import time
from pymongo import MongoClient
import pdb

def retrieve(n):
	client = MongoClient()
	db = client.test
	collection = db.test
	flag = False
	api_calls = ['user.getinfo','user.getrecenttracks','user.getfriends',
	'user.gettopartists']
	ids = random.sample(range(30000000), n)
	for i in ids:
		print 'looking up user ' + str(i)
		results = {}
		results['_id'] = i
		for call in api_calls:
			payload = {'user': str(i),'method':call, 
			'api_key':'872d9492f0b60d20c8f230faef15cc00', 'format':'json'}
			if call == 'user.gettopartists':
				payload['limit'] = '5'
			# get user info
			try:
				info = requests.get('http://ws.audioscrobbler.com/2.0/', params = payload)
			except (requests.exceptions):
				print "******* error in request ******  ", info
				break
			# skip if user id was invalid
			if call == 'user.getinfo' and 'error' in info.json().keys():
				results = None
				print 'reached an error, moving to next user'
				break
			elif call == 'user.gettopartists':
				payload['limit'] = '1'
				payload['method'] = 'artist.gettoptags'
				payload.pop('user', None)
				tags = []
				try:
					if type(info.json()['topartists']['artist']) == str:
						print 'only one artist who CARES!?'
						break
					for artist_info in info.json()['topartists']['artist']:
						payload['artist'] = artist_info['name']
						tag_info = requests.get('http://ws.audioscrobbler.com/2.0/',
							params = payload)
						tags.append(tag_info.json()['toptags']['tag'][0]['name'])
					results['top_tags'] = tags
					results['top_artists'] = info.json()
					print 'waiting 1.5 seconds after getting artists tags'
					time.sleep(1.5)
				except(KeyError):
					print 'no top artists'
					results['top_tags'] = tags
					results['top_artists'] = []
			else:
				results[call.split('.')[1]] = info.json()
		if results:
			print 'adding result for user ' + str(i) + ' to database'
			collection.insert(results) 
		print 'waiting 1.5 seconds until next user'
		time.sleep(1.5)

if __name__ == "__main__":
	retrieve(20)




			

