import requests
import json
from Restaurant import Restaurant
class JackInTheBox(Restaurant):
    def __init__(self, address):
        super().__init__(address)
        self.availProducts = {
            "Jumbo Jack®":'Jumbo Jack',
            "Double Jack® Combo":'Double Jack Combo (Small)',
            "Jumbo Jack® Combo":'Jumbo Jack Combo (Small)',
            "54439851":'Double Jack Cheese Burger',
            "-1" :'2 Monster Tacos',
            "2 Tacos for $0.99":'2 Tacos',
            "French Fries": "French  Fries",
            "Diet Coke®":'Fountain Drink',	
            "Chocolate Shake":'Shake (Vanilla/Chocolate/Strawberry)',
            "Hamburger Meal":'Hamburger Kids Meal',
            "Chicken Nuggets (5) Meal":'4PC Chicken Nuggets Kids Meal'
        }
        self.ids = {}
        self.get_store()
        self.scrape_menu()


    def add_size_group(self, prod_id, prod_name, options):


        url = f"https://www.jackinthebox.com/products/{prod_id}/modifiers?clientid=jackinthebox&nomnom=product-modifiers&nomnom_restaurant_id={self.store_num}"

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload).json()

        for opt in options:
            if opt == 'Small' or opt == 'Regular':
                self.menu[opt +" "+ prod_name] = response['optiongroups'][0]['options'][0]['cost']
            elif opt == 'Medium':
                self.menu[opt +" "+ prod_name] = response['optiongroups'][0]['options'][1]['cost']
            else:
                try:
                    self.menu[opt +" "+ prod_name] = response['optiongroups'][0]['options'][2]['cost']
                except:
                    self.menu[opt +" "+ prod_name] = response['optiongroups'][0]['options'][1]['cost']


    def scrape_menu(self):
        url = f"https://www.jackinthebox.com/restaurants/{self.store_num}/menu?nomnom=add-restaurant-to-menu"

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload).json()

        for category in response['categories']:
            for product in category['products']:
                if product['name'] in self.availProducts.keys():
                    if product['cost'] == 0:
                        if "Combo" in product['name']:
                            self.add_size_group(product['id'], self.availProducts[product['name']], ['Small'])
                        elif "Shake" in product['name']:
                            self.add_size_group(product['id'], self.availProducts[product['name']], ['Regular, Large'])
                        else:
                            self.add_size_group(product['id'], self.availProducts[product['name']], ['Small', 'Medium',' Large'])
                    else:
                        self.menu[self.availProducts[product['name']]] = product['cost']


    def get_store(self):
        url = f"https://www.jackinthebox.com/restaurants/near?lat={self.address.lat}&long={self.address.long}&radius=20&limit=6&nomnom=calendars&nomnom_calendars_from=20221221&nomnom_calendars_to=20221229&nomnom_exclude_extref=999"

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload).json()

        self.store_num = response['restaurants'][0]['id']
        self.address.address = response['restaurants'][0]['streetaddress']
