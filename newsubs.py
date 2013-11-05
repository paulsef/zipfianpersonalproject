from bs4 import BeautifulSoup
import requests
import re
import pdb

def new_subscibers():
	r = requests.get('http://www.last.fm/subscribe')
	soup = BeautifulSoup(r.text)
	less_soup = soup.find_all(href = re.compile('/user'))
	usernames = []
	for obj in less_soup:
		usernames.append(obj.getText())
	return usernames

def add_new_subscribers(new_users):
	f = file('tomodusers.txt')
	ids = f.readlines()
	f.close()
	f = file('tomodusers.txt', 'w')
	new_ids = new_users + ids
	for i in new_ids:
		i = str(i.strip())
		f.write(i)
		f.write('\n')
	f.close()

def main():
	new_users = new_subscibers()
	add_new_subscribers(new_users)

if __name__ == '__main__':
	main()


