
from restaurants.BurgerKing import BurgerKing
from restaurants.CarlsJr import CarlsJr
from restaurants.Chipotle import Chipotle
from Address import Address
from Excel import Excel
from RestaurantFactory import RestaurantFactory
from restaurants.JackInTheBox import JackInTheBox
from restaurants.Wendys import Wendys
from selenium import webdriver

def main():
    driver = webdriver.Chrome()
    ex = Excel('Jan 2023 copy.xlsx')
    zips = {}
    try:
        with open('zipCodes.csv', 'r') as f:
            for line in f:
                vals = line.split(',')
                zips[vals[0]] = vals[1]
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
        if sheet_name == "McDonald":
            continue
        ex.set_active_sheet(sheet_name)
        items = {}
        for zipcode in ex.read_zips():
            #SKIP IF NO GEOCODING
            lat, long = Address.geocode(zipcode)
            addr = Address(zipcode, lat, long)
            restaurant = RestaurantFactory.create(sheet_name, addr, driver)
            print('----------------')
            print(f'Restaurant: {restaurant.store_num}')
            print(f'Address: {restaurant.address.address}')
            print(f'Menu: {restaurant.menu}')
            print("-----------------\n")
            for item, price in restaurant.menu.items():
                items.setdefault(item, []).append(price)
            items.setdefault('Competitive Address', []).append(restaurant.address.address)

        for item, lst in items.items():
            ex.put_prices(item, lst)

if __name__ == "__main__":
    main()