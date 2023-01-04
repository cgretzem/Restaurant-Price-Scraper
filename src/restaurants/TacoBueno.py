from Restaurant import Restaurant
import json

class TacoBueno(Restaurant):
    def __init__(self, address):
        super().__init__(address)
        self.availProducts = {
            'Beef Crispy Taco': 'Original Crispy Taco',
            "Big Freak'n Taco": "Big Freak'n Taco",
            "Bean Burrito": 'Bean Burrito',
            "Combination Burrito": 'Combo Burrito',
            "Beef Burrito": 'Beef Burrito',
            "Chicken Quesadilla": 'Chicken Quesadilla',
            'Cheese Quesadilla': 'Cheese Quesadilla',
            "Beef Mucho Nachos": 'Mucho Nachos',
            'Combo 2': 'Combo #2 Three Crispy Beef Tacos Combo',
            'Coca Cola' : 'Coke'
            }

    def default_menu(self):
        menu = {}
        for item in self.availProducts.values():
            if item != 'Coke':
                menu[item] = -1
        menu["Small Coke"] = -1
        menu["Medium Coke"] = -1
        menu["Large Coke"] = -1
        return menu

    async def scrape_menu(self):
        if self.store_num == -1:
            return
        url = "https://buenoonthego.com/mp/ndXTAL/get_available_menus"

        payload = json.dumps({
        "customer_id": 1068982,
        "restaurant_id": f"{self.store_num}"
        })
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'NovaDine.session=a561ac5bfae09685743f49b323d0fc26d4d928b0c55c06f5e71541febcd522d6fc5ade46; ROUTE_ID=.app-11-prod-01; __ac=Z3Vlc3Q3OTc4OTdAbm92YWRpbmUuY29tOlYzWjRjMXoz',
        'Origin': 'https://buenoonthego.com',
        'Referer': 'https://buenoonthego.com/mp/nd/sites/xilan-double-prime/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
        }

        response = await self.post(url, headers=headers, payload=payload)

        for category in response['menus'][0]['categories']:
            if "subcategories" in category.keys():
                category = category['subcategories'][0]
            for item in category['items']:
                if item['name'] in self.availProducts.keys():
                    if item['name'] == "Coca Cola":
                        price_range = [item['base_price_range'][0], item['base_price_range'][1]]
                        if item['base_price_range'][0] == 99:
                            price_range = [199, item['base_price_range'][1]]
                        self.menu["Small Coke"] = price_range[0]/100
                        self.menu["Medium Coke"] = (price_range[0] + ((price_range[1]-price_range[0])/2) + 10)/100
                        self.menu["Large Coke"] = price_range[1]/100
                    else:
                        self.menu[self.availProducts[item['name']]] = item['display_price']/100
        

    async def get_store(self, index=0):
        url = "https://buenoonthego.com/mp/ndXTAL/searchPickupRestaurants_JSON"

        payload=f'serviceTypeId=2&zipcode=\%22{self.address.zipcode}\%22&distanceInMiles=50&serviceHours=true'
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'NovaDine.session=a561ac5bfae09685743f49b323d0fc26d4d928b0c55c06f5e71541febcd522d6fc5ade46; ROUTE_ID=.app-11-prod-01; __ac=Z3Vlc3Q3OTc4OTdAbm92YWRpbmUuY29tOlYzWjRjMXoz',
        'Origin': 'https://buenoonthego.com',
        'Referer': 'https://buenoonthego.com/mp/nd/sites/xilan-double-prime/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
        }

        response = await self.post(url, headers=headers, payload=payload)

        try:
            self.id = response[self.store_num]['resturantid']
            self.address.address = response[self.store_num][0]['address1']
        except IndexError:
            self.store_num = -1