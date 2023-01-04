

from Address import Address
from restaurants.TacoBell import TacoBell
import asyncio
from selenium import webdriver

if __name__ == '__main__':
    ad = Address(92506, "6333 Riverside Ave",latitude=33.882614, longitude=-117.528205)
    driver = webdriver.Chrome()
    tc = TacoBell(ad, driver)
    
    asyncio.run(tc.initalize())
    print(tc.menu)