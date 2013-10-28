import random
import requests
import time
from pymongo import MongoClient
import pdb

requests_count = 0

def make_users(n, file_name):
	'''
	creates a list of n random ids and writes them to a file
	only ever use this ONCE!
	'''
	ids = random.sample(range(30000000), n)
	f = file(file_name,'w')
	for user_id in ids:
		f.write("%s\n" % user_id)
	f.close()


def user_list(file_name):
	'''
	opens user file and builds a python list containing all
	user therin
	'''
	f = file(file_name)
	ids = f.read().splitlines()
	return ids

def too_many():
	''' 
	function to look at global count of requests
	waits if count is too high and updates count to zero
	if count is small enough, will increment count and coninue
	'''
	global requests_count
	if requests_count >= 5:
		print 'sleeping for 1.2 seconds because count was too high'
		time.sleep(1.2)
		requests_count = 0
	else:
		requests_count += 1

def get(user_id):
	'''
	takes an user_id and returns the relevent information for that user
	'''
	# list of api calls to make
	api_calls = ['user.getinfo','user.getrecenttracks','user.getfriends',
	'user.gettopartists']
	# initialize dictionary of results with the user id as _id for mongo
	results = {}
	results['_id'] = user_id
	# make the api calls
	for call in api_calls:
		# customize url with payload
		payload = {'user': 
		(user_id),'method':call, 
		'api_key':'872d9492f0b60d20c8f230faef15cc00', 'format':'json'}
		if call == 'user.gettopartists':
			payload['limit'] = '5'
		try:
			# get user info
			too_many()
			info = requests.get('http://ws.audioscrobbler.com/2.0/', params = payload)
		except (requests.exceptions):
			results = None
			print "******* error in request ******  ", info
			# if there was an error in the request, 
			# break out of calls and return none
			break
		# skip if user_id was invalid
		if call == 'user.getinfo' and 'error' in info.json().keys():
			# if there was an error from last.fm
			# break out of calls and return none
			results = None
			break
		elif call == 'user.gettopartists':
			# if the call was get top artists, iterate through the top artists
			# and get the first top tag
			payload['limit'] = '1'
			payload['method'] = 'artist.gettoptags'
			# remove the user from the payload as it's irrelevant
			payload.pop('user', None)
			tags = []
			try:
				# get the artist info
				info_list = info.json()['topartists']['artist']
				if isinstance(info_list, dict):
					# if the artist info only contains one artist, turn it into
					# an interable
					info_list = [info_list]
				# iterate through the artist info
				for artist_info in info_list:
					payload['artist'] = artist_info['name']
					# try to get the tag for the artist
					try:
						too_many()
						tag_info = requests.get('http://ws.audioscrobbler.com/2.0/',
							params = payload)
						tags.append(tag_info.json()['toptags']['tag'][0]['name'])
					except(requests.exceptions):
						# if the request for artist tags failed, continue to next artist
						pass
				results['top_tags'] = tags
				results['top_artists'] = info.json()
			except(KeyError):
				print 'no top artists'
				results['top_tags'] = tags
				results['top_artists'] = []
		else:
			results[call.split('.')[1]] = info.json()
	return results

def write_to_db(user_info):
	'''
	write the user's info to the database
	'''
	client = MongoClient()
	db = client.test
	collection = db.test
	collection.insert(user_info) 
	
def main():
	ids = user_list('users.txt')
	for user_id in ids:
		too_many()
		print 'looking up user ' + str(user_id)
		info = get(user_id = user_id)
		if info:
			print 'writing info to database'
			write_to_db(user_info = info)

		else:
			print 'error in user info'



if __name__ == "__main__":
	main()




			

