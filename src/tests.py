from Address import Address
from Excel import Excel

from selenium import webdriver
from RestaurantFactory import RestaurantFactory
import asyncio
import time


async def task_func(zips, zipcode, sheet_name, driver, address):
        lat, long = (zips[zipcode][0], zips[zipcode][1])
        addr = Address(zipcode,address, lat, long)
        restaurant = RestaurantFactory.create(sheet_name, addr, driver)
        await restaurant.initalize()
        print('----------------')
        print(f'Restaurant: {restaurant.store_num}')
        print(f'ZipCode: {restaurant.address.zipcode}')
        print(f'Address: {restaurant.address.address}')
        print(f'Menu: {restaurant.menu}')
        print("-----------------\n")

        return (restaurant.address.address, restaurant.menu)

async def run_test(name):
    driver = webdriver.Chrome()
    ex = Excel('output1.xlsx')
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

    sheet_name = name

    ex.set_active_sheet(sheet_name)
    items = {}
    all_zips = ex.read_zips()

    tasks = [task_func(zips, zipcode, sheet_name, driver, addresses[index]) for index,zipcode in enumerate(all_zips)]
    results = await asyncio.gather(*tasks)
    for item_obj in results:
        for item, lst in item_obj[1].items():
            items.setdefault(item, []).append(lst)
        items.setdefault('Competitive Address', []).append(item_obj[0])

    driver.close()
    print("WRITING TO EXCEL")
    for item, lst in items.items():
        ex.put_prices(item, lst)



async def run_all_restaurants():
    driver = webdriver.Chrome()
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
    for sheet_name in ex.get_sheet_names():
        if sheet_name.lower() == "mcdonalds":
            continue
        ex.set_active_sheet(sheet_name)
        items = {}
        all_zips = ex.read_zips()
        tasks = [task_func(zips, zipcode, sheet_name, driver, addresses[index]) for index,zipcode in enumerate(all_zips)]
        start = time.perf_counter()
        results = await asyncio.gather(*tasks)
        total = time.perf_counter() - start
        print(f"Total time taken : {total/60}")
        for item_obj in results:
            for item, lst in item_obj[1].items():
                items.setdefault(item, []).append(lst)
            items.setdefault('Competitive Address', []).append(item_obj[0])

        print("WRITING TO EXCEL")
        for item, lst in items.items():
            ex.put_prices(item, lst)
        items.clear()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_test('Burger King'))
    #loop.run_until_complete(run_all_restaurants())