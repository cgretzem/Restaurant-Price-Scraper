from abc import ABC, abstractmethod
class Restaurant(ABC):
    def __init__(self, address):
        self.address = address
        self.availProducts = None
        self.menu = {}
        self.store_num = 0
    
    @abstractmethod
    def scrape_menu(self):
        pass

    @abstractmethod
    def get_store(self):
        pass

    def get_product(self, name):
        return self.menu.get(name)