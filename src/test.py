

from Address import Address
from restaurants.TacoBell import TacoBell
import asyncio
from selenium import webdriver

from restaurants.TacoBueno import TacoBueno

if __name__ == '__main__':
    ad = Address(92506, "6333 Riverside Ave",latitude=33.882614, longitude=-117.528205)
    #driver = webdriver.Chrome()
    tc = TacoBueno(ad)
    
    asyncio.run(tc.initalize())
    print(tc.menu)