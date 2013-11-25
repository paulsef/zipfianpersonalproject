import os
import json
import pdb

def from_json(filepath):
        ''' 
        takes a json file and converts it to dictionaries
        '''
        f = open(filepath)
        dictionaries = [json.loads(line) for line in f.readlines()]
        return dictionaries

image_dict = {}
for filename in os.listdir('jsonout'):
	path = 'jsonout/' + filename
	dicts = from_json(path)
	for userdict in dicts:
		try:
			source = userdict['getinfo']['user']['image'][1]['#text']
			if len(source) == 0:
				source = 'http://cdn.last.fm/flatness/responsive/2/noimage/default_user_140_g2.png'
		except(KeyError, IndexError):
			source = 'http://cdn.last.fm/flatness/responsive/2/noimage/default_user_140_g2.png'
		image_dict[userdict['getinfo']['user']['name']] = source

json.dump(image_dict, file('image_dict.json','w'))