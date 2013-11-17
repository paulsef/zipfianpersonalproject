from bs4 import BeautifulSoup
import requests

def get_image(user_id):
	r = requests.get('http://www.last.fm/user/' + str(user_id))
	soup = BeautifulSoup(r.text)
	image_tag = soup.find(class_ = 'userImage')
	return image_tag

# def slice(dataframe, parameters):
# 	'''
# 	paramters is a dictionary of paramaters, may contain null values
# 	slice by 'playcount','top_count,'avg_diff_hours','age',
# 	'hour_registered','subscriber'
# 	'''
# 	defaults = {}
# 	to_slice = ['playcount','avg_diff_hours','age',
# 				'hour_registered','subscriber', 'genre'] #,'top_count']
# 	for parameter in to_slice:
# 		if parameter == 'hour_registered':
# 			if not parameters[parameter]:
# 				continue
# 		elif parameter == 'genre':
# 			if not parameters[parameter]:
# 				continue
# 		else:
# 			if not parameter:
# 				parameters[parameter] = 0
# 			dataframe = dataframe[dataframe[parameter > parameters[parameter]]