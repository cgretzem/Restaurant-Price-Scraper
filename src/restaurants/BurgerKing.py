from Restaurant import Restaurant
import requests
import json
import aiohttp
class BurgerKing(Restaurant):
    def __init__(self, address):
        super().__init__(address)
        self.availProducts = {
            'combo_5804': 'Whopper Combo (Small)',
            'item_953': 'Whopper',
            'combo_5774': 'Hamburger King Jr. Meal',
            'combo_5797': '4 Pc Chicken Nuggets Jr. Meal',
            'item_541': 'Small Fries',
            'item_540': 'Medium Fries',
            'item_539': 'Large Fries',
            'item_43091': 'Small Coke',
            'item_43092': 'Medium Coke',
            'item_43093': 'Large Coke',
            'item_781': 'Shakes (Vanilla/Chocolate/Strawberry',
            'item_581': 'Bk Café Iced Coffee',
            'item_584': 'Bk Café Iced Coffee',
            'item_53713' : 'Small Coke',
            'item_53714' : 'Medium Coke',
            'item_53715' : 'Large Coke',
            "item_52523" : 'Small Coke',
            "item_52524" : 'Medium Coke',
            "item_52525" : 'Large Coke'
            }
        

    async def scrape_menu(self):
        if self.store_num == None:
            self.default = True
            self.menu = self.default_menu()
            return
        url = f"https://use1-prod-bk-gateway.rbictg.com/graphql?operationName=storeMenu&variables=%7B%22channel%22%3A%22whitelabel%22%2C%22region%22%3A%22US%22%2C%22storeId%22%3A%22{self.store_num}%22%2C%22serviceMode%22%3A%22pickup%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22713eb1f46bf8b3ba1a867c65d0e0fd2a879cf0e2d1d3e9788addda059e617cc0%22%7D%7D"

        payload={}
        headers = {
        'authority': 'use1-prod-bk-gateway.rbictg.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'apollographql-client-name': 'wl-web',
        'apollographql-client-version': '958b49c',
        'content-type': 'application/json',
        'origin': 'https://www.bk.com',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-forter-token': 'b58bf187b29f47e8af48498e3daf2581_1671744334756__UDF43_13ck_tt',
        'x-session-id': '4F7451F9-CC93-443C-BDC0-E1AEE02F1B6E',
        'x-ui-language': 'en',
        'x-ui-platform': 'web',
        'x-ui-region': 'US',
        'x-user-datetime': '2022-12-22T14:33:50-07:00'
        }

        response = await self.fetch(url, headers=headers, payload=payload)
        if not 'errors' in response.keys():
            for item in response['data']['storeMenu']:
                if item['id'] in self.availProducts.keys():
                    if item['isAvailable'] == False and self.availProducts[item['id']] not in self.menu.keys():
                        self.menu[self.availProducts[item['id']]] = -1
                        continue
                    elif self.availProducts[item['id']] not in self.menu.keys() or self.menu[self.availProducts[item['id']]] == -1 or self.menu[self.availProducts[item['id']]] == 0:
                        self.menu[self.availProducts[item['id']]] = item['price']['default']/100


        if not self.menu:
            self.store_index += 1
            await self.get_store(index = self.store_index)
            await self.scrape_menu()
        


    async def get_store(self, index = 0):

        url = "https://use1-prod-bk.rbictg.com/graphql"

        payload = json.dumps([
        {
            "operationName": "GetRestaurants",
            "variables": {
            "input": {
                "filter": "NEARBY",
                "coordinates": {
                "userLat": self.address.lat,
                "userLng": self.address.long,
                "searchRadius": 32000
                },
                "first": 20,
                "status": "OPEN"
            }
            },
            "query": "query GetRestaurants($input: RestaurantsInput) {\n  restaurants(input: $input) {\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    totalCount\n    nodes {\n      ...RestaurantNodeFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment RestaurantNodeFragment on RestaurantNode {\n  _id\n  storeId\n  isAvailable\n  posVendor\n  chaseMerchantId\n  curbsideHours {\n    ...OperatingHoursFragment\n    __typename\n  }\n  deliveryHours {\n    ...OperatingHoursFragment\n    __typename\n  }\n  diningRoomHours {\n    ...OperatingHoursFragment\n    __typename\n  }\n  distanceInMiles\n  drinkStationType\n  driveThruHours {\n    ...OperatingHoursFragment\n    __typename\n  }\n  driveThruLaneType\n  email\n  environment\n  franchiseGroupId\n  franchiseGroupName\n  frontCounterClosed\n  hasBreakfast\n  hasBurgersForBreakfast\n  hasCatering\n  hasCurbside\n  hasDelivery\n  hasDineIn\n  hasDriveThru\n  hasTableService\n  hasMobileOrdering\n  hasLateNightMenu\n  hasParking\n  hasPlayground\n  hasTakeOut\n  hasWifi\n  hasLoyalty\n  id\n  isDarkKitchen\n  isFavorite\n  isHalal\n  isRecent\n  latitude\n  longitude\n  mobileOrderingStatus\n  name\n  number\n  parkingType\n  phoneNumber\n  physicalAddress {\n    address1\n    address2\n    city\n    country\n    postalCode\n    stateProvince\n    stateProvinceShort\n    __typename\n  }\n  playgroundType\n  pos {\n    vendor\n    __typename\n  }\n  posRestaurantId\n  restaurantImage {\n    asset {\n      _id\n      metadata {\n        lqip\n        palette {\n          dominant {\n            background\n            foreground\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    crop {\n      top\n      bottom\n      left\n      right\n      __typename\n    }\n    hotspot {\n      height\n      width\n      x\n      y\n      __typename\n    }\n    __typename\n  }\n  restaurantPosData {\n    _id\n    __typename\n  }\n  status\n  vatNumber\n  __typename\n}\n\nfragment OperatingHoursFragment on OperatingHours {\n  friClose\n  friOpen\n  monClose\n  monOpen\n  satClose\n  satOpen\n  sunClose\n  sunOpen\n  thrClose\n  thrOpen\n  tueClose\n  tueOpen\n  wedClose\n  wedOpen\n  __typename\n}\n"
        }
        ])
        headers = {
        'authority': 'use1-prod-bk.rbictg.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'apollographql-client-name': 'wl-web',
        'apollographql-client-version': '958b49c',
        'content-type': 'application/json',
        'origin': 'https://www.bk.com',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-forter-token': 'b58bf187b29f47e8af48498e3daf2581_1671744334756__UDF43_13ck_tt',
        'x-session-id': '4F7451F9-CC93-443C-BDC0-E1AEE02F1B6E',
        'x-ui-language': 'en',
        'x-ui-platform': 'web',
        'x-ui-region': 'US',
        'x-user-datetime': '2022-12-22T14:26:33-07:00'
        }
        response = await self.post(url, headers=headers, payload=payload)
        try:
            
            self.store_num = int(response[0]['data']['restaurants']['nodes'][index]['storeId'])
            self.address.address = response[0]['data']['restaurants']['nodes'][index]['physicalAddress']['address1']
            if response[0]['data']['restaurants']['nodes'][index]['isAvailable'] == False:
                self.store_index += 1
                await self.get_store(index = self.store_index)
        except IndexError:
            self.store_num = None



