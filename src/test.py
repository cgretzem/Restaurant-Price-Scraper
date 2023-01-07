

from Address import Address
from Excel import Excel
from restaurants.BurgerKing import BurgerKing
from restaurants.CarlsJr import CarlsJr
from restaurants.TacoBell import TacoBell
import asyncio
from selenium import webdriver

from restaurants.TacoBueno import TacoBueno


def load_zips():
    ex = Excel('Jan 2023 copy.xlsx')
    addresses = ex.get_addresses()
    zips = {}
    try:
        with open('zipCodes.csv', 'r') as f:
            for line in f:
                vals = line.split(',')
                zips[int(vals[0])] = (float(vals[1]),float(vals[2]))
    except FileNotFoundError:
        codes = ex.get_all_zips()
        zips_not_found = []
        for code in codes:
            latlong = Address.geocode(code)
            if(latlong == None):
                zips_not_found.append(code)
                continue
            print(f"Zip: {code}\tlat: {latlong[0]}, long={latlong[1]}")
            zips[code] = latlong
        with open('zipCodes.csv', 'w') as f:
            for key, val in zips.items():
                f.write(f'{key},{val[0]},{val[1]}\n')
        print(zips_not_found)
    finally:
        return zips


if __name__ == '__main__':
    zips = load_zips()

    code = 85374
    lat, long = zips[code]
    ad = Address(code, "6333 Riverside Ave",latitude=lat, longitude=long)
    driver = webdriver.Chrome()
    tc = BurgerKing(ad)
    
    asyncio.run(tc.initalize())
    print(tc.menu)