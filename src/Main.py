
from Chipotle import Chipotle
from Address import Address
from Excel import Excel
if __name__ == "__main__":
    ex = Excel()
    print(ex.read_chipotle_zips())
    # lat, long = Address.geocode(92506)
    # add = Address(92506, lat, long)
    # res = Chipotle(add)
    # print(res.store_num)
    # print(res.menu)