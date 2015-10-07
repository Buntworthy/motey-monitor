# Standard
import threading
import time
from queue import Queue
import datetime

# Internal
from readers import *


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
            reading, reading_id = self.reader.get_temp()
            self.queue.put((reading,reading_id))


def printr(writing_queue):
    while True:
        message = writing_queue.get()
        print(message)


class PhpWriter(threading.Thread):

    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.url = "http://www.cutsquash.com/add-reading.php"
        self.key = "KEY_HERE"
        self.daemon = False

    def run(self):
        while True:
            # Get the reading from the queue
            (reading, reading_id) = self.queue.get()

            # Record the current time
            now = datetime.datetime.now()

            reading_entry = {"key": self.key,
                             "datetime": str(now),
                             "temp": str(reading),
                             "id": reading_id}
            response = requests.get(self.url, params=reading_entry)
            print(reading_entry)



if __name__ == "__main__":

    # Set up queue and workers
    q = Queue()
    workers = list()
    workers.append(Worker(2, WebReader("Web reading"), q))
    workers.append(Worker(0.1, DummySerialReader(), q))

    # Set up thread for output
    p = PhpWriter(q)

    # Start threads
    for worker in workers:
        worker.start()
    p.start()
