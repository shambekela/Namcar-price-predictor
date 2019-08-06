from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import csv

counter = 1 

def get_all_urls():
	# iterate over the different urls
	for page in range(1):
		url = 'https://www.namauto.com/cars/?order=price&page={}&per_page=72'.format(page)

		html = urlopen(url)
		bs = BeautifulSoup(html.read(), 'lxml')

		cars = bs.findAll('div', {'class': 'cycle off'})

		if cars:
			for car in cars:
				res = get_car_data(car.a['href'])
				write_to_csv(res)
				break
				global counter
				counter += 1
		else:
			break

def get_car_data(url):

	full_url = 'https://www.namauto.com{}'.format(url)
	res = urlopen(full_url)
	data = BeautifulSoup(res.read(), 'lxml')

	car = []

	car.append(full_url) # url
	car.append('url')
	car.append('price')
	
	for title in data.find('div', {'class': 'title module'}).find_all('span'):
		car.append(title.attrs['class'][0]) #make model variant

	for prop in data.find(True, {'class': 'overview-data-standard'}).find_all(True, {'class': 'value'}):
		car.append(prop.attrs['class'][1])

	return car


def write_to_csv(car):
	with open("namauto.csv", 'a', newline='') as f: 
		writer = csv.writer(f)
		writer.writerows([car])
		global counter
		print('Added...{}'.format(counter))

if __name__ == '__main__':
	get_all_urls()