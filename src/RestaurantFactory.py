

from restaurants.BurgerKing import BurgerKing
from restaurants.Wendys import Wendys 
from restaurants.Chipotle import Chipotle


class RestaurantFactory():
    def create(name, zipcode):
        if name == "Chipotle":
            return Chipotle(zipcode)
        if name == 'Burger King':
            return BurgerKing(zipcode)
        if name == 'Wendys':
            return Wendys(zipcode)
        if name == 'Jack In the Box':
            pass
        if name == 'Carls Jr':
            pass
        if name == 'Taco Bell':
            pass
        if name == 'Taco Bueno':
            pass