import threading
import time
from queue import Queue

# External
import requests

class webReader(object):

    def __init__(self):
        self.root = 'http://api.openweathermap.org/data/2.5/weather'
        self.query = {'q': 'Cambridge,uk'}

    def getTemp(self):
        # Make the request
        print("Getting the temperature")
        r = requests.get(self.root, params=self.query)
        if r.status_code is 200:
            # Interpret the response
            result = r.json()
            temp = result['main']['temp'] - 273.15
            return temp
        else:
            raise ConnectionError("Couldn't get the temperature")

def worker(interval, reader, reading_queue):

    while True:
        time.sleep(interval)
        reading = reader.getTemp()
        reading_queue.put(reading)

def printr(writing_queue):

	while True:
		message = q.get()
		print(message)

if __name__ == "__main__":

    # Set up queue and threads
    web_temperature = webReader()
    q = Queue()
    t = threading.Thread(target=worker, args=(10, web_temperature, q))
    t.setDaemon(True)
    p = threading.Thread(target=printr, args=(q,))
    p.setDaemon(False)

    t.start()
    p.start()