import requests
class Address:
    def __init__(self, zipcode, latitude=0, longitude=0, address=None):
        self.address = address
        self.zipcode = zipcode
        self.lat = latitude
        self.long = longitude

    def geocode(zip):
        response = requests.get(f'http://api.positionstack.com/v1/forward?access_key=5040ef9a3b2cb138ba8ac3aa89197ec5&query={zip}&country=US').json()
        return (response['data'][0]['latitude'], response['data'][0]['longitude'])