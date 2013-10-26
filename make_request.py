import json
import requests
import sched, time
from pymongo import MongoClient
client = MongoClient()
db = client.db

def make_request():
	# retreive user1 from username database that have not gotten info
	print "Retreiving neighbors"
	neighbors = requests.get('http://ws.audioscrobbler.com/2.0/http://ws.audioscrobbler.com/2.0/?method=user.getneighbours&user=phnx485&api_key=872d9492f0b60d20c8f230faef15cc00&format=json')
	neighbors_text = neighbors.json()
	for key in neighbors_text.keys():
		
	# get list of user1's neighbors, 
	# upsert neighbors into username database
	print 'added ' + str(n) + 'number of users to usernames db'
	# get user1's info
	print 'getting user info '
	user_info = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user=phnx485&api_key=872d9492f0b60d20c8f230faef15cc00&format=json')
	user_info_text  = user_info.json()
	# get user1's top artists via api call

	# get user1's number of friends via api call

	# get user1's top tags (ie favorite genre) via api call
	
	# dump all ueser1s info into mongo db

	return None

import sched, time
s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    make_request()
    # do your stuff
    sc.enter(60, 1, do_something, (sc,))

s.enter(60, 1, do_something, (s,))
s.run()