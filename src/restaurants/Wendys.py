from Restaurant import Restaurant
import requests
import json

class Wendys(Restaurant):
    def __init__(self, address):
        super().__init__(address)
        self.availProducts = {
            "Dave's Single®": "Dave's Single Burger",
            "Dave's Single® LIDS Combo" : "Dave's Single Combo (Small)",
            "Dave's Single® Combo": "Dave's Single Combo (Small)",
            "Dave's Single® Mustard Combo" : "Dave's Single Combo (Small)",
            "Dave's Double®": "Dave's Double Burger",
            "Dave's Double® Mustard Combo" : "Dave's Double Combo (Small)",
            "Dave's Double® LIDS Combo" : "Dave's Double Combo (Small)",
            "Dave's Double® Combo": "Dave's Double Combo (Small)",
            "Kids' Hamburger": "Kid's Meal Hamburger",
            "Kids' Hamburger Frosty": "Kid's Meal Hamburger",
            "Kids' 4PC Nuggets": "Kid's Meal 4 Pc Nuggets ",
            "Kids' 4PC Nuggets Frosty" : "Kid's Meal 4 Pc Nuggets ",
            "Small Fries": "Small Fries",
            "Medium Fries": "Medium Fries",
            "Large Fries": "Large Fries",
            "SM FREESTYLE": "Small Fountain Drink",
            'Small Coca-Cola®' : "Small Fountain Drink",
            'Medium Coca-Cola®' : "Medium Fountain Drink",
            'Large Coca-Cola®' : "Large Fountain Drink",
            "MD FREESTYLE": "Medium Fountain Drink",
            "LG FREESTYLE": "Large Fountain Drink"
        }
        self.menu = self.default_menu()

    async def scrape_menu(self):
        if self.store_num == None:
            self.default = True
            self.menu = self.default_menu()
            return
        url = f"https://digitalservices-cdn.wendys.com/menu/getSiteMenu?lang=en&cntry=US&sourceCode=ORDER.WENDYS&version=20.0.3&siteNum={self.store_num}&freeStyleMenu=true"

        payload={}
        headers = {}

        response = await self.fetch(url, headers=headers, payload=payload)

        for item in response['menuLists']['menuItems']:
            if item['name'] in self.availProducts.keys():
                self.menu[self.availProducts[item['name']]] = item["price"]
        
        for item in response['menuLists']['salesItems']:
            if item['name'] in self.availProducts.keys():
                self.menu[self.availProducts[item['name']]] = item["price"]

        
        if not self.menu:
            self.store_index += 1
            self.get_store(index = self.store_index)
            self.scrape_menu()


    async def get_store(self, index = 0):

        url = f"https://digitalservices.prod.ext-aws.wendys.com/LocationServices/rest/nearbyLocations?&lang=en&cntry=US&sourceCode=ORDER.WENDYS&version=20.0.3&address={self.address.del_address.replace(' ', '%20').replace('.','')}&limit=25&filterSearch=true&hasMobileOrder=true&radius=20"

        payload={}
        headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://order.wendys.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Cookie': 'JSESSIONID=BE705EF682B9177DD99DB3D5EA0F796C'
        }

        response = await self.fetch(url, headers=headers, payload=payload)

        try:
            self.store_num = response['data'][index]['id']
            self.address.address = response['data'][index]['address1']
        except IndexError:
            self.store_num = None
        except KeyError:
            self.store_num = None


        
