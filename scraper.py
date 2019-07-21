from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import csv

def get_all_urls():
	# iterate over the different urls
	for page in range(1):
		url = 'https://www.namauto.com/cars/?order=price&page={}&per_page=12'.format(page)

		html = urlopen(url)
		bs = BeautifulSoup(html.read(), 'lxml')

		cars = bs.findAll('div', {'class': 'cycle off'})
		count = 1 

		if cars:
			for car in cars:
				res = get_car_data(car.a['href'])
				write_to_csv(res, count)
				count += 1
		else:
			break

def get_car_data(url):

	full_url = 'https://www.namauto.com{}'.format(url)
	res = urlopen(full_url)
	data = BeautifulSoup(res.read(), 'lxml')

	car = []

	car.append(full_url)
	car.append(data.find('div', {'class': 'price-now'}).select('span.value')[0].get_text().strip())

	for title in data.find('div', {'class': 'title module'}).find_all('span'):
		car.append(title.getText().strip())

	for prop in data.find(True, {'class': 'overview-data-standard'}).find_all(True, {'class': 'value'}):
		car.append(prop.getText().strip())

	return car

def write_to_csv(car, count):
	with open("namauto.csv", 'a', newline='') as f: 
		writer = csv.writer(f)
		writer.writerows([car])
		print('Added...{}'.format(count))

if __name__ == '__main__':
	get_all_urls()