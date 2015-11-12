from readers import *

# External
import Libraries.Adafruit_DHT as DHT


class DHTReader(Reader):
    def __init__(self, reading_id):
        # set up the sensor
        self.sensor = DHT.DHT22
        self.pin = 4
        self.reading_id = reading_id

    def get_temp(self):
        # TODO deal with misreads
        rh, temp = DHT.read_retry(self.sensor, self.pin)
        return temp