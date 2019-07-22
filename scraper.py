from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import csv

count = 1 

def get_all_urls():
	# iterate over the different urls
	for page in range(1, 100):
		url = 'https://www.namauto.com/cars/?order=price&page={}&per_page=72'.format(page)

		html = urlopen(url)
		bs = BeautifulSoup(html.read(), 'lxml')

		cars = bs.findAll('div', {'class': 'cycle off'})

		if cars:
			for car in cars:
				res = get_car_data(car.a['href'])
				write_to_csv(res)
				count += 1
		else:
			break

def get_car_data(url):

	full_url = 'https://www.namauto.com{}'.format(url)
	res = urlopen(full_url)
	data = BeautifulSoup(res.read(), 'lxml')

	car = []

	car.append(full_url) # url
	car.append(data.find('div', {'class': 'price-now'}).select('span.value')[0].get_text().strip()) # price

	for title in data.find('div', {'class': 'title module'}).find_all('span'):
		print(title.attrs['class'][0])
		car[title.getText().strip()]

	for prop in data.find(True, {'class': 'overview-data-standard'}).find_all(True, {'class': 'value'}):
		car[prop.getText().strip()]

	return car

def write_to_csv(car):
	with open("namauto.csv", 'a', newline='') as f: 
		writer = csv.writer(f)
		writer.writerows([car])
		print('Added...{}'.format(count))

if __name__ == '__main__':
	get_all_urls()