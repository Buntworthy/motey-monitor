import requests
import random
import time
import datetime


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

            # Assemble the result
            reading = {'temp': temp, 'id': self.reading_id}
            reading = self.add_reading_time(reading)
            return reading
        else:
            raise ConnectionError("Couldn't get the temperature")

    def add_reading_time(self, reading):
        # TODO make this a method of an abc
        now = datetime.datetime.now()
        reading['datetime']  = str(now)
        return reading

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

        # Assemble the result
        reading = {'temp': dummy_temp, 'id': reading_id}
        reading = self.add_reading_time(reading)
        return reading

    def add_reading_time(self, reading):
        now = datetime.datetime.now()
        reading['datetime']  = str(now)
        return reading
