import requests
import random
import time


class WebReader(object):
    """
    WebReader grabs temperature information from a web API, assigned an ID on creation
    which remains constant.
    """
    def __init__(self, reading_id):
        # This will always be for Cambridge:
        self.root = 'http://api.openweathermap.org/data/2.5/weather'
        self.query = {'q': 'Cambridge,uk'}
        self.reading_id = reading_id

    def get_temp(self):
        # Make the request
        r = requests.get(self.root, params=self.query)
        if r.status_code is 200:
            # Interpret the response
            result = r.json()
            temp = result['main']['temp'] - 273.15
            return temp, self.reading_id
        else:
            raise ConnectionError("Couldn't get the temperature")


class DHTReader(object):
    def __init__(self):
        pass

    def get_temp(self):
        pass


class DummySerialReader(object):
    """ Dummy version of the serial reader used to monitor the mote
    Waits a random length of time before outputting a reading to simulate
    waiting for a serial input
    Also simulates receiving an ID from the serial input
    """
    def __init__(self):
        self.min_wait = 0
        self.max_wait = 5
        self.max_dummy_temp = 30.0

    def get_temp(self):
        # Wait for a bit
        time.sleep(random.randint(self.min_wait, self.max_wait))
        # Make up a reading
        dummy_temp = self.max_dummy_temp*random.random()
        # Make up an reading_id
        reading_id = "Serial reading: " + str(random.randint(0, 100))
        return dummy_temp, reading_id
