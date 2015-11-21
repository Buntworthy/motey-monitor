import requests
import random
import time
import datetime
import serial
import json

# Internal
from constants import *


class Reader(object):
    def __init__(self):
        self.reading_id = "000"

    def add_reading_time(self, reading):
        now = datetime.datetime.now()
        reading['datetime'] = str(now)
        return reading

    def read(self):
        temp = self.get_temp()
        reading = {'temp': temp, 'id': self.reading_id}
        reading = self.add_reading_time(reading)
        return reading


class WebReader(Reader):
    """
    WebReader grabs temperature information from a web API, assigned an ID on creation
    which remains constant.
    """

    def __init__(self, reading_id):
        # This will always be for Cambridge:
        self.root = 'http://api.openweathermap.org/data/2.5/weather'
        self.query = {'q': 'Cambridge,uk',
                      'APPID': OPENWEATHER_KEY}
        self.reading_id = reading_id

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


class SerialReader(Reader):
    """ Class to read from the serial port to receive data from
    the moteino gateway
    """

    def __init__(self):
        self.ser = serial.Serial(
            #port='/dev/ttyUSB0',
            port='COM3',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None
        )

    def read(self):
        """
        Override the superclass method as the serial string
        returns both the id and the temperature
        :return:
        """

        # Read from the serial port
        line = self.ser.readline()
        line = line.decode('utf-8')

        # Unpack the data from the serial line
        # Expect a line in json format, e.g.:
        # {"id": "ABC", "temp": 25.4}
        reading = json.loads(line)
        reading = self.add_reading_time(reading)
        return reading


class DummySerialReader(Reader):
    """ Dummy version of the serial reader used to monitor the mote
    Waits a random length of time before outputting a reading to simulate
    waiting for a serial input
    Also simulates receiving an ID from the serial input
    """

    def __init__(self):
        self.min_wait = 0
        self.max_wait = 300
        self.max_dummy_temp = 30.0

    def get_temp(self):
        # Wait for a bit
        time.sleep(random.randint(self.min_wait, self.max_wait))
        # Make up a reading
        dummy_temp = self.max_dummy_temp * random.random()
        # Make up an reading_id
        reading_id = "Serial reading: " + str(random.randint(0, 100))

        self.reading_id = reading_id
        return dummy_temp
