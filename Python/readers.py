import requests


class WebReader(object):
    def __init__(self):
        self.root = 'http://api.openweathermap.org/data/2.5/weather'
        self.query = {'q': 'Cambridge,uk'}

    def get_temp(self):
        # Make the request
        r = requests.get(self.root, params=self.query)
        if r.status_code is 200:
            # Interpret the response
            result = r.json()
            temp = result['main']['temp'] - 273.15
            return temp
        else:
            raise ConnectionError("Couldn't get the temperature")


class DHTReader(object):
    def __init__(self):
        pass

    def get_temp(self):
        pass
