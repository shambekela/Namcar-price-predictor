from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import pandas as pd
#import pyodbc
from sqlalchemy import create_engine
import urllib
import os

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
                print('Counter at {} : '.format(str(counter)), car.a['href'])
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
    
    title = data.find('div', {'class': 'title module'}).find_all('span')


    ## make
    car.append(title[0].getText()) 
    # combine model variant
    car.append(title[1].getText() + ' ' + title[2].getText())


    for prop in data.find(True, {'class': 'overview-data-featured'}).find_all(True, {'class': 'value'}):
        car.append(prop.getText().strip())

    car.append("None") # empty value to match data to number of columns

    return car


def write_to_dataframe(car):

    '''
    df = pd.DataFrame(data = car, columns = 
        ['url',
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
    '''

    df = pd.DataFrame(data = car, columns = [
    'link',
    'price',
    'manufacturer',
    'model',
    'reg-year',
    'mileage',
    'engine-size',
    'transmission',
    'fuel-type',
    'drive',
    'finance'])

    path = os.path.join(os.getcwd(),r'data\\namauto14012020.csv')

    if not os.path.isfile(path):
       df.to_csv(path, index=False)
    else: # else it exists so append without writing the header
       df.to_csv(path, mode="a", index=False, header=False)
    
    print('Added to csv------------------------------------------------')

if __name__ == '__main__':
    get_all_urls()
