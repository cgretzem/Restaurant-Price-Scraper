import requests
import json
from Restaurant import Restaurant
class JackInTheBox(Restaurant):
    def __init__(self, address):
        super().__init__(address)
        self.availProducts = {
            "54439856":'Jumbo Jack',
            "54439766":'Double Jack Combo (Small)',
            "54439770":'Jumbo Jack Combo (Small)',
            "54439851":'Double Jack Cheese Burger',
            :'2 Monster Tacos',
            :'2 Tacos',
            :'Small French Fries',
            :'Medium  French Fries',
            :'Large  French Fries',
            :'Small Fountain Drink',	
            :'Medium Fountain Drink',
            :'Large Fountain Drink',
            :'Regular Shake (Vanilla/Chocolate/Strawberry)',
            :'Large Shake (Vanilla/Chocolate/Strawberry)',
            :'Hamburger Kids Meal',
            :'4PC Chicken Nuggets',
            :'Kids Meal'
        }
        
        self.scrape_menu()


    def get_menu_item(self prod_id):


        url = f"https://www.jackinthebox.com/products/{prod_id}/modifiers?clientid=jackinthebox&nomnom=product-modifiers&nomnom_restaurant_id={self.store_num}"

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload).json()

        print(response.text)


    def scrape_menu(self):
        url = f"https://www.jackinthebox.com/restaurants/{self.store_num}/menu?nomnom=add-restaurant-to-menu"

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload).json()

        for category in response['categories']:
            for product in category['products']:
                if product['name'] in self.availProducts:
                    if product['cost'] == 0:

                    self.menu[product['name']] = product['cost']


    def get_store(self):
        url = f"https://www.jackinthebox.com/restaurants/near?{self.address.lat}&long={self.address.long}&radius=20&limit=6&nomnom=calendars&nomnom_calendars_from=20221221&nomnom_calendars_to=20221229&nomnom_exclude_extref=999"

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload).json()

        self.store_num = response['restaurants'][0]['id']
        self.address.address = response['restaurants'][0]['streetaddress']
