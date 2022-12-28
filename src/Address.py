import requests
class Address:
    def __init__(self, zipcode, del_address, latitude=0, longitude=0, address=None):
        self.del_address = del_address
        self.address = address
        self.zipcode = zipcode
        self.lat = latitude
        self.long = longitude

    def geocode(zip):
        response = requests.get(f'http://api.positionstack.com/v1/forward?access_key=5040ef9a3b2cb138ba8ac3aa89197ec5&query={zip}&country=US').json()
        if response['data'] == []:
            return None
        return (response['data'][0]['latitude'], response['data'][0]['longitude'])