from abc import ABC, abstractmethod
from aiohttp import ClientSession
from aiohttp import client_exceptions
from asyncio import sleep

import aiohttp
class Restaurant(ABC):
    def __init__(self, address):
        self.address = address
        self.availProducts = None
        self.menu = {}
        self.store_num = 0
        self.store_index = 0
        self.default = False
        self.session = None

    async def post(self, url, headers=None, payload=None):
        for x in range(3):
            try:
                async with self.session.post(url, headers=headers, data=payload) as response:
                    return await response.json()
            except Exception as e:
                print(e)
                print(f"ATTEMPT {x+1}")
                await sleep(10)
        print("FINAL ATTEMPT : 30s")
        await sleep(30)
        async with self.session.post(url, headers=headers, data=payload) as response:
            return await response.json()
    async def fetch(self, url, headers=None, payload=None):

        for x in range(3):
            try:
                async with self.session.get(url, headers=headers, data=payload) as response:
                    #print(await response.text())
                    return await response.json()
            except Exception as e:
                print(e)
                print(f"ATTEMPT {x+1}")
                await sleep(10)
        print("FINAL ATTEMPT : 30s")
        await sleep(30)
        async with self.session.get(url, headers=headers, data=payload) as response:
            return await response.json()
        
    @abstractmethod
    async def scrape_menu(self):
        pass

    @abstractmethod
    async def get_store(self, index=0):
        pass

    def get_product(self, name):
        return self.menu.get(name)

    async def initalize(self):
        self.session = ClientSession()
        self.menu = self.default_menu()
        await self.get_store()
        await self.scrape_menu()
        await self.session.close()

    def default_menu(self):
        menu = {}
        for product in self.availProducts.values():
            menu[product] = -1
        return menu

