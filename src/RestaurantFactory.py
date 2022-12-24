

from restaurants.BurgerKing import BurgerKing
from restaurants.CarlsJr import CarlsJr
from restaurants.JackInTheBox import JackInTheBox
from restaurants.Wendys import Wendys 
from restaurants.Chipotle import Chipotle


class RestaurantFactory():
    def create(name, zipcode, driver):
        if name == "Chipotle":
            return Chipotle(zipcode)
        if name == 'Burger King':
            return BurgerKing(zipcode)
        if name == 'Wendys':
            return Wendys(zipcode)
        if name == 'Jack In the Box':
            return JackInTheBox(zipcode)
        if name == 'Carls Jr':
            return CarlsJr(zipcode, driver)
        if name == 'Taco Bell':
            pass
        if name == 'Taco Bueno':
            pass