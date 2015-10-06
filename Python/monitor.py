# Standard
import threading
import time
from queue import Queue

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
            reading, id = self.reader.get_temp()
            self.queue.put((reading,id))


def printr(writing_queue):
    while True:
        message = writing_queue.get()
        print(message)


if __name__ == "__main__":

    # Set up queue and workers
    q = Queue()
    workers = list()
    workers.append(Worker(2, WebReader("Web reading"), q))
    workers.append(Worker(0.1, DummySerialReader(), q))

    # Set up thread for output
    p = threading.Thread(target=printr, args=(q,))
    p.setDaemon(False)

    # Start threads
    for worker in workers:
        worker.start()
    p.start()
