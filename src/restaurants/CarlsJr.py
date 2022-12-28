import bs4
import json
from selenium import webdriver

from Restaurant import Restaurant
class CarlsJr(Restaurant):
    def __init__(self, address, driver):
        super().__init__(address)
        self.driver = driver
        self.availProducts = {
                "Famous Star® with Cheese":'Famous Star',
                "Famous Star® with Cheese Combo":'Famous Star Combo (Small)',
                "The Big Carl®":'Big Carl',
                "The Big Carl® Combo":'Big Carl Combo (Small)',
                "Natural-Cut French Fries":'Natural Cut Fries',
                "Soft Drink": 'Soft Drink',
                "Hand-Scooped Ice-Cream Shakes™":'Hand Scooped Shake',
                "Hamburger Kid's Meal":'Hamburger Kids Meal',
                "2-piece Chicken Tender Kid's Meal":'2 PC Chicken Tender Kids Meal'
        }
        self.get_store()
        self.scrape_menu()
        
    
    def add_size_group(self, prod_id, prod_name, options, type='None'):
        url = f"https://nomnom-prod-api.carlsjr.com/products/{prod_id}/modifiers"

        self.driver.get(url)
        soup = bs4.BeautifulSoup(self.driver.page_source, features="lxml")
        #print(soup.find('pre').text)
        response = json.loads(soup.find('pre').text)

        for opt in options:
            prefix = opt + " "
            if type =='combo':
                prefix = ''
            if type=='drink':
                self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][0]['modifiers'][0]['options'][0]['cost']
                return
            if opt == 'Small' or opt == 'Regular':
                self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][0]['cost']
            elif opt == 'Medium':
                self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][1]['cost']
            else:
                try:
                    self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][2]['cost']
                except:
                    self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][1]['cost']


        #self.scrape_menu()
    def scrape_menu(self):
        if self.store_num == None:
            self.default = True
            self.menu = self.default_menu()
            return
        url = f'https://nomnom-prod-api.carlsjr.com/restaurants/{self.store_num}/menu?nomnom=add-restaurant-to-menu'
        
        self.driver.get(url)
        soup = bs4.BeautifulSoup(self.driver.page_source, features="lxml")
        #print(soup.find('pre').text)
        response = json.loads(soup.find('pre').text)
        
        for category in response['categories']:
            for product in category['products']:
                if product['name'] in self.availProducts.keys():
                    if product['cost'] == 0:
                        if "Combo" in product['name'] or "Meal" in product['name']:
                            self.add_size_group(product['id'], self.availProducts[product['name']], ['Small'], type='combo')
                        elif "Shake" in product['name']:
                            self.add_size_group(product['id'], self.availProducts[product['name']], ['Regular, Large'], type='combo')
                        elif "Drink" in product['name']:
                            self.add_size_group(product['id'], self.availProducts[product['name']], ['Small', 'Medium',' Large'], type='drink')
                        else:
                            self.add_size_group(product['id'], self.availProducts[product['name']], ['Small', 'Medium',' Large'])
                    else:
                        self.menu[self.availProducts[product['name']]] = product['cost']
        if not self.menu:
            self.store_index += 1
            self.get_store(index = self.store_index)
            self.scrape_menu()


    def get_store(self,index = 0):
        url = f'https://nomnom-prod-api.carlsjr.com/restaurants/near?lat={self.address.lat}&long={self.address.long}&radius=50&limit=25&nomnom=calendars&nomnom_calendars_from=20221222&nomnom_calendars_to=20221230&nomnom_exclude_extref=999'
        
        self.driver.get(url)
        soup = bs4.BeautifulSoup(self.driver.page_source, features="lxml")
        #print(soup.find('pre').text)
        response = json.loads(soup.find('pre').text)
        #driver.close()
        try:
            self.address = response['restaurants'][index]['streetaddress']
            self.store_num = response['restaurants'][index]['id']
        except IndexError:
            self.store_num = None
