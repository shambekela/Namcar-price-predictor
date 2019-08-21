from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import urllib

counter = 1 # keep track of progress
all_cars = []

def get_all_urls():
    # iterate over the different urls
    for page in range(1, 100):
        url = 'https://www.namauto.com/cars/?order=price&page={}&per_page=24'.format(page)

        html = urlopen(url)
        bs = BeautifulSoup(html.read(), 'lxml')

        cars = bs.findAll('div', {'class': 'cycle off'})

        if cars:
            for car in cars:
                res = get_car_data(car.a['href'])
                global all_cars
                all_cars.append(res)
                global counter
                print('Counter at {}'.format(str(counter)))
                counter += 1
        else:
            break

        write_to_dataframe(all_cars)
        all_cars = []

def get_car_data(url):

    full_url = 'https://www.namauto.com{}'.format(url)
    res = urlopen(full_url)
    data = BeautifulSoup(res.read(), 'lxml')

    car = []

    car.append(full_url) # url
    
    for span in data.find('div', {'class': 'price-now'}).find_all('span', {'class': 'value'}):
        car.append(span.getText())
    
    for title in data.find('div', {'class': 'title module'}).find_all('span'):
        car.append(title.getText()) #make model variant

    for prop in data.find(True, {'class': 'overview-data-standard'}).find_all(True, {'class': 'value'}):
        car.append(prop.getText().strip())
        #car.append(prop.attrs['class'][1])
    return car


def write_to_dataframe(car):
    df = pd.DataFrame(data = car, columns = ['url',
        'price',
        'make',
        'model',
        'variant',
        'reg',
        'previous-owners',
        'mpg',
        'colour',
        'interior-colour',
        'exterior-colour',
        'doors',
        'fuel-type',
        'bodystyle',
        'mileage',
        'engine-size',
        'transmission'])
    
    quoted = urllib.parse.quote_plus(r"DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-R64COUI;DATABASE=Shambekela;Trusted_Connection=yes")
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))

    df.to_sql('namauto', schema='dbo', con = engine, if_exists='append')

    result = engine.execute('select count(*) from dbo.namauto')
    result.fetchall()

if __name__ == '__main__':
    get_all_urls()
