
from restaurants.BurgerKing import BurgerKing
from restaurants.Chipotle import Chipotle
from Address import Address
from Excel import Excel
from RestaurantFactory import RestaurantFactory
from restaurants.JackInTheBox import JackInTheBox
from restaurants.Wendys import Wendys
def main():
    ex = Excel('Jan 2023 copy.xlsx')
    for sheet_name in ex.get_sheet_names():
        if sheet_name == "McDonald":
            continue
        ex.set_active_sheet(sheet_name)
        items = {}.setdefault()
        for zipcode in ex.read_zips():
            #SKIP IF NO GEOCODING
            lat, long = Address.geocode(zipcode)
            addr = Address(zipcode, lat, long)
            restaurant = RestaurantFactory.create(sheet_name, Address)
            print('----------------')
            print(f'Restaurant: {restaurant.store_num}')
            print(f'Menu: {restaurant.menu}')
            print("-----------------\n")
            for item, price in restaurant.menu:
                items.setdefault(item, []).append(price)

        for item, lst in items:
            ex.put_prices(item, lst)

if __name__ == "__main__":
    #lat, long = Address.geocode(92673)
    addr = Address(zipcode = 92673, longitude =-117.613509, latitude =33.467371)
    jack = JackInTheBox(addr)
    print(jack.menu)