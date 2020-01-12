from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import os

counter = 1 # keep track of progress
all_cars = [] 

def get_all_urls():
	for page in range(1, 150):
		url = 'https://www.namcars.net/index.php?module=cars&filters=1&type=used_cars,demo,new_cars&page={}&lang=en'.format(page)

		html = urlopen(url)
		bs = BeautifulSoup(html.read(), 'lxml')

		cars = bs.find('div', {'class': 'itemsContainer'}).find_all('a', {'class': 'link'})

		if cars:
			for carlink in cars:
				curr_car = get_car_data(carlink.get('href')) # get the car for the specific link and return in array format
				global all_cars
				all_cars.append(curr_car)
				global counter
				print('Counter at {} : '.format(str(counter)), carlink.get('href'))
				counter += 1
		else:
			break

		write_to_dataframe(all_cars)
		all_cars = []

def get_car_data(url):
	base = 'https://www.namcars.net{}'.format(url)

	car = urlopen(base)
	res = BeautifulSoup(car.read(), 'lxml')

	dict_attr = {}
	car_attr = []
	car_attr_keys = ['reg-year', 'mileage', 'engine-size', 'fuel-type', 'transmission', 'drive', 'finance']

	item_price = res.find('div', {'class': 'detail_left'}).find('span', itemprop="price").getText().strip() # item price

	car_attr.append(base)
	car_attr.append(item_price)

	for header in res.find('div', {'class': 'title-box'}).find_all('span'):
		if header.has_attr('itemprop'):
			prop = str(header.get('itemprop'))
			val = header.getText().strip()
			car_attr.append(val) # add the manufacturer, model to attr dictionary

	for spec in res.find('div', 'car-specs').find_all('div', {'class': 'row'})[:len(car_attr_keys)]:
		car_attr.append(spec.getText().strip())

	return car_attr

def write_to_dataframe(car):
	df = pd.DataFrame(data=car, columns=['link', 'price', 'manufacturer', 'model' , 'reg-year', 'mileage', 'engine-size', 'fuel-type', 'transmission', 'drive', 'finance'])

	path = os.path.join(os.getcwd(),r'data\\namcars12012020.csv')

	if not os.path.isfile(path):
	   df.to_csv(path, index=False)
	else: # else it exists so append without writing the header
	   df.to_csv(path, mode="a", index=False, header=False)

	print('Added to csv------------------------------------------------')

if __name__ == '__main__':
	get_all_urls()