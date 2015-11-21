# Standard
import threading
import time
from queue import Queue

# Internal
from readers import *
from readers_pi import *


class Worker(threading.Thread):
    """ A worker thread which sleeps for a set interval then reads a current
    temperature using the get_temp method of the passed reader object
    """
    def __init__(self, interval, reader, queue):
        super().__init__()
        self.daemon = True
        self.interval = interval
        self.reader = reader
        self.queue = queue

    def run(self):
        while True:
            time.sleep(self.interval)
            reading = self.reader.get_temp()
            self.queue.put(reading)


def printr(writing_queue):
    while True:
        message = writing_queue.get()
        print(message)


class PhpWriter(threading.Thread):

    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.url = "http://www.cutsquash.com/add-reading.php"
        self.key = PHP_KEY
        self.daemon = False

    def run(self):
        while True:
            # Get the reading from the queue
            reading = self.queue.get()

            # Add the secret key
            reading['key'] = self.key

            # Add to the db
            # TODO handle connection errors
            response = requests.get(self.url, params=reading)
            print(reading)



if __name__ == "__main__":

    # Set up queue and workers
    q = Queue()
    workers = list()
    workers.append(Worker(600, WebReader("web"), q))
    #workers.append(Worker(60, DHTReader("dht"), q))
    workers.append(Worker(0.1, SerialReader(), q))

    # Set up thread for output
    p = PhpWriter(q)

    # Start threads
    for worker in workers:
        worker.start()
    p.start()
