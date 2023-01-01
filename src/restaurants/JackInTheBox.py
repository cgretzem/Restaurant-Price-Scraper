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
            "Double Jack®":'Double Jack Cheese Burger',
            "-1" :'2 Monster Tacos',
            "2 Tacos for $0.99":'2 Tacos',
            "French Fries": "French  Fries",
            "Diet Coke®":'Fountain Drink',	
            "Chocolate Shake":'Shake (Vanilla/Chocolate/Strawberry)',
            "Hamburger Meal":'Hamburger Kids Meal',
            "Chicken Nuggets (5) Meal":'4PC Chicken Nuggets Kids Meal'
        }
        


    def default_menu(self):
        menu = {}
        for product in self.availProducts.values():
            if "Fries" not in product and "Drink" not in product and "Shake" not in product:
                menu[product] = -1
        menu["Small French  Fries"] = -1
        menu["Medium French  Fries"] = -1
        menu["Large French  Fries"] = -1
        menu["Small Fountain Drink"] = -1
        menu["Medium Fountain Drink"] = -1
        menu["Large Fountain Drink"] = -1
        menu["Regular Shake (Vanilla/Chocolate/Strawberry)"] = -1
        menu["Large Shake (Vanilla/Chocolate/Strawberry)"] = -1
        return menu

    async def add_size_group(self, prod_id, prod_name, options, add_prefix = True):


        url = f"https://www.jackinthebox.com/products/{prod_id}/modifiers?clientid=jackinthebox&nomnom=product-modifiers&nomnom_restaurant_id={self.store_num}"

        payload={}
        headers = {}

        response = await self.fetch(url, headers=headers, payload=payload)
        

        for opt in options:
            
            prefix = opt + ' '
            if not add_prefix:
                prefix = ''
            if not response['optiongroups']:
                self.menu[prefix + prod_name] = -1
                continue
            if opt == 'Small' or opt == 'Regular':
                
                self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][0]['cost']
            elif opt == 'Medium':
                self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][1]['cost']
            else:
                try:
                    self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][2]['cost']
                except:
                    try:
                        self.menu[prefix + prod_name] = response['optiongroups'][0]['options'][1]['cost']
                    except:
                        self.menu[prefix + prod_name] = -1


    async def scrape_menu(self):
        if self.store_num == None:
            self.default = True
            self.menu = self.default_menu()
            return
        url = f"https://www.jackinthebox.com/restaurants/{self.store_num}/menu?nomnom=add-restaurant-to-menu"

        payload={}
        headers = {}

        response = await self.fetch(url, headers=headers, payload=payload)

        for category in response['categories']:
            for product in category['products']:
                if product['name'] in self.availProducts.keys():
                    if product['cost'] == 0:
                        if "Combo" in product['name']:
                            await self.add_size_group(product['id'], self.availProducts[product['name']], ['Small'], add_prefix=False)
                        elif "Shake" in product['name']:
                            await self.add_size_group(product['id'], self.availProducts[product['name']], ['Regular', 'Large'])
                        else:
                            await self.add_size_group(product['id'], self.availProducts[product['name']], ['Small', 'Medium','Large'])
                    else:
                        self.menu[self.availProducts[product['name']]] = product['cost']
        if not self.menu:
            self.store_index += 1
            await self.get_store(index = self.store_index)
            await self.scrape_menu()


    async def get_store(self, index = 0):
        url = f"https://www.jackinthebox.com/restaurants/near?lat={self.address.lat}&long={self.address.long}&radius=20&limit=6&nomnom=calendars&nomnom_calendars_from=20221221&nomnom_calendars_to=20221229&nomnom_exclude_extref=999"

        payload={}
        headers = {}

        response = await self.fetch(url, headers=headers, payload=payload)

        
        try:
            if not response['restaurants'][index]['isavailable']:
                self.store_index += 1
                await self.get_store(self.store_index)
            else:
                self.store_num = response['restaurants'][index]['id']
                self.address.address = response['restaurants'][index]['streetaddress']
        except IndexError:
            self.store_num = None
