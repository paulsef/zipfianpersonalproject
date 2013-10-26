import random
import requests
import time

def retrieve():
	flag = False
	api_calls = ['user.getinfo','user.getrecenttracks','user.getfriends',
	'user.topartists', 'artist.toptags']
	ids = random.sample(range(30000000), 20)#200000)
	for i in ids:
		results = {i:{}}
		for call in api_calls:
			payload = {'user': str(i),'method':str(call), 
			'key':'872d9492f0b60d20c8f230faef15cc00'}
			# get user info
			info = requests.get('http://ws.audioscrobbler.com/2.0/', params = payload)
			# skip if user id was invalid
			if call == 'user.getinfo' and 'error' in info.json().keys():
				#wait
				time.stop()
				break
			if call == ''
			reuslts[i][call] = inf
		else:
			break

			

