import requests
import json
from Restaurant import Restaurant


class Chipotle(Restaurant):
    def __init__(self, address):
        super().__init__(address)
        self.availProducts = {
                'Chicken Burrito': 'Chicken Burrito',
                'Steak Burrito':'Steak Burrito',
                'Guacamole':'Guacamole',
                'Chicken Quesadilla':'Chicken Quesadilla',
                'Steak Quesadilla':'Steak Quesadilla'
        }
        self.get_store()
        
        self.scrape_menu()


    def scrape_menu(self):
        if self.store_num == None:
            self.default = True
            self.menu = self.default_menu()
            return
        url = f"https://services.chipotle.com/menuinnovation/v1/restaurants/{self.store_num}/onlinemenu?channelId=web&includeUnavailableItems=true"

        payload={}
        headers = {
        'Ocp-Apim-Subscription-Key': 'b4d9f36380184a3788857063bce25d6a',
        'Cookie': 'f5avrbbbbbbbbbbbbbbbb=AGELJLLMFJNGBOMNKHAOKOMFFACFEOMJCBEFHMLFNNEKPPNFHCIKCNCMJOPLIDALCFAAALIGAFJDEJDGDDFCFBHKBKGAJMAACKKCKNHDDKKCKHBEDNAHMAHGMMLFAMBN; TS01cfe0ce=013836ca937c6052e4c1c3b237dc07144d7fe301c557e1bf816ffd24bf7d9bf2fc846433f0c2a575084fa1aabb9170d2598f093f62ddfa3fc6fd82bba1fd2f398dd32118c7'
        }

        response = requests.request("GET", url, headers=headers, data=payload).json()
        for item in response['entrees']:
            #print(item['itemName'])
            if item['itemName'] in self.availProducts.keys():
                self.menu[item['itemName']] = item['unitPrice']

        if not self.menu:
            self.store_index += 1
            self.get_store(index = self.store_index)
            self.scrape_menu()

    def get_store(self, index = 0):
        url = "https://services.chipotle.com/restaurant/v3/restaurant"

        payload = json.dumps({
        "latitude": self.address.lat,
        "longitude": self.address.long,
        "radius": 80467,
        "restaurantStatuses": [
            "OPEN",
            "LAB"
        ],
        "conceptIds": [
            "CMG"
        ],
        "orderBy": "distance",
        "orderByDescending": False,
        "pageSize": 10,
        "pageIndex": 0,
        "embeds": {
            "addressTypes": [
            "MAIN"
            ],
            "realHours": True,
            "directions": True,
            "catering": True,
            "onlineOrdering": True,
            "timezone": True,
            "marketing": True,
            "chipotlane": True,
            "sustainability": True,
            "experience": True
        }
        })
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Chipotle-CorrelationId': 'OrderWeb-8b7a4605-b13c-4c5c-9e29-4445117b5d03',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'b4d9f36380184a3788857063bce25d6a',
        'Origin': 'https://www.chipotle.com',
        'Referer': 'https://www.chipotle.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Cookie': 'f5avrbbbbbbbbbbbbbbbb=FDGEMIMDIBGMFAHOAKIKKDADDOCOJDNGOGLFCJPDMODBMFMPNFEDCPFGPDACLHLAAHMIAIAINGDDGMNEPEDNBEBEBDJAGACEDLLGIEINHMPEBMCKMNNOEAEABOINGEGL; TS01cfe0ce=013836ca93994ff26339c4eaa3df22c43dc082b1c3573ef84147794b4177c61c95e635c1075d73d4d82d19952d1d7a87b68b1f0fbc4cd168d5b79f2d063bbaf8c9357ee6e6'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        try:
            self.store_num = response['data'][index]['restaurantNumber']
            self.address.address = response['data'][index]['addresses'][0]
        except IndexError:
            self.store_num = None
