from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_all_urls():

	for page in range(1, 100):
		url = 'https://www.namcars.net/index.php?module=cars&filters=1&type=used_cars,demo,new_cars&page={}&lang=en'.format(page)

		html = urlopen(url)
		bs = BeautifulSoup(html.read(), 'lxml')

		for carlink in bs.find('div', {'class': 'itemsContainer'}).find_all('a', {'class': 'link'}):
			href = carlink.get('href')
			get_link_data(href)
			break

def get_link_data(url):
	base = 'https://www.namcars.net{}'.format(url)

	car = urlopen(base)
	res = BeautifulSoup(car.read(), 'lxml')

	print(res.find('div', {'class': 'detail_left'}).find('span', itemprop="price").getText().strip()) # item price
	for header in res.find('div', {'class': 'title-box'}).find_all('span'):
		if header.has_attr('itemprop'):
			prop = str(header.get('itemprop'))
			val = header.getText().strip()
			print(prop + ": " + val)

	for spec in res.find('div', 'car-specs').find_all('div', {'class': 'row'}):
		print(spec.getText().strip())	

if __name__ == '__main__':
	get_all_urls()