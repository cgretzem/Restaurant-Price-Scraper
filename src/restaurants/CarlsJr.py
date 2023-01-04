import bs4
import json
from selenium import webdriver
import asyncio

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
    
    async def get_page(self, url):
        self.driver.get(url)
        return self.driver.page_source
    

    def default_menu(self):
        menu = {}
        for product in self.availProducts.values():
            if "Fries" not in product and "Drink" not in product:
                menu[product] = -1
        menu["Small Natural Cut Fries"] = -1
        menu["Medium Natural Cut Fries"] = -1
        menu["Large Natural Cut Fries"] = -1
        menu["Small Soft Drink"] = -1
        menu["Medium Soft Drink"] = -1
        menu["Large Soft Drink"] = -1
        return menu

    async def add_size_group(self, prod_id, prod_name, options, type='None'):
        url = f"https://nomnom-prod-api.carlsjr.com/products/{prod_id}/modifiers"

        source = await self.get_page(url)
        soup = bs4.BeautifulSoup(source, features="lxml")
        #print(soup.find('pre').text)
        response = json.loads(soup.find('pre').text)

        for opt in options:
            prefix = opt + " "
            if type =='combo':
                prefix = ''
            if type=='drink':
                index = 0
                if opt == "Small":
                    index = 0
                if opt == "Medium":
                    index = 1
                if opt == "Large":
                    index = 2
                self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][index]['modifiers'][0]['options'][0]['cost']
                if response['optiongroups'][0]['options'][index]['modifiers'][0]['options'][0]['cost'] != 0:
                    continue
            if opt == 'Small' or opt == 'Regular':
                self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][0]['cost']
                if response['optiongroups'][0]['options'][0]['cost'] == 0 and type=='combo':
                    
                    if len(response['optiongroups']) == 3:
                        res0 = response['optiongroups'][0]['options'][0]
                        res1 = response['optiongroups'][1]['options'][0]
                        res2 = response['optiongroups'][2]['options'][0]
                    else:
                        
                        res0 = response['optiongroups'][0]['options'][0]['modifiers'][0]['options'][0]
                        res1 = response['optiongroups'][0]['options'][0]['modifiers'][1]['options'][0]
                        res2 = response['optiongroups'][0]['options'][0]['modifiers'][2]['options'][0]
                    while True:
                        if 'cost' in res0.keys():
                            if res0['cost'] == 0:
                                res0 = res0['modifiers'][0]['options'][0]
                                res1 = res1['modifiers'][0]['options'][0]
                                res2 = res2['modifiers'][0]['options'][0]
                            else:
                                self.menu[prefix + prod_name] = res0['cost'] + res1['cost'] + res2['cost']
                                break
                        else:
                            res0 = res0['modifiers'][0]['options'][0]
                            res1 = res1['modifiers'][0]['options'][0]
                            res2 = res2['modifiers'][0]['options'][0]
                    #self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][0]['modifiers'][0]['options'][0]['modifiers'][0]['cost'] + response['optiongroups'][1]['options'][0]['modifiers'][0]['options'][0]['modifiers'][0]['cost'] + response['optiongroups'][2]['options'][0]['modifiers'][0]['options'][0]['modifiers'][0]['cost']
            elif opt == 'Medium':
                self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][1]['cost']
            else:
                try:
                    self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][2]['cost']
                except:
                    self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][1]['cost']


        #self.scrape_menu()
    async def scrape_menu(self):
        if self.store_num == None:
            self.default = True
            self.menu = self.default_menu()
            return
        url = f'https://nomnom-prod-api.carlsjr.com/restaurants/{self.store_num}/menu?nomnom=add-restaurant-to-menu'
        
        source = await self.get_page(url)
        soup = bs4.BeautifulSoup(source, features="lxml")
        #print(soup.find('pre').text)
        response = json.loads(soup.find('pre').text)

        if 'error' in response.keys():
            self.store_index += 1
            await self.get_store(self.store_index)
            await self.scrape_menu()
            return
        
        for category in response['categories']:
            for product in category['products']:
                if product['name'] in self.availProducts.keys():
                    if product['cost'] == 0:
                        if "Combo" in product['name'] or "Meal" in product['name']:
                            await self.add_size_group(product['id'], self.availProducts[product['name']], ['Small'], type='combo')
                        elif "Shake" in product['name']:
                            await self.add_size_group(product['id'], self.availProducts[product['name']], ['Regular, Large'], type='combo')
                        elif "Drink" in product['name']:
                            await self.add_size_group(product['id'], self.availProducts[product['name']], ['Small', 'Medium','Large'], type='drink')
                        else:
                            await self.add_size_group(product['id'], self.availProducts[product['name']], ['Small', 'Medium',' Large'])
                    else:
                        self.menu[self.availProducts[product['name']]] = product['cost']
        if not self.menu:
            self.store_index += 1
            self.get_store(index = self.store_index)
            self.scrape_menu()


    async def get_store(self,index = 0):
        url = f'https://nomnom-prod-api.carlsjr.com/restaurants/near?lat={self.address.lat}&long={self.address.long}&radius=50&limit=25&nomnom=calendars&nomnom_calendars_from=20221222&nomnom_calendars_to=20221230&nomnom_exclude_extref=999'
        
        source = await self.get_page(url)
        soup = bs4.BeautifulSoup(source, features="lxml")
        #print(soup.find('pre').text)
        response = json.loads(soup.find('pre').text)
        #driver.close()
        try:
            self.address.address = response['restaurants'][index]['streetaddress']
            self.store_num = response['restaurants'][index]['id']
        except IndexError:
            self.store_num = None
