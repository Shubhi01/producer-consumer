from collections import deque
import concurrent.futures
from threading import Event, Semaphore
import time
"""
Single producer
Single consumer
"""

global queue
global event
global full, empty
Q_CAP = 5

"""
race condition
deadlock
"""

"""
Different rate of producing and consuming --
if rate of producing > rate of consuming, then producer will have to wait if there's no buffer,
i.e. producer can produce futher till the last message is consumed
unbounded buffer can lead to out-of-memory issues if rate of producing >> rate of consuming
Different rates of production and consumption can be simulated by making the corresponding thread sleep
"""

"""
since we have just a single producer and consumer, using a thread unsafe data structure,
deque works here
If we had multiple consumers or producers, we'll need a thread safe data strucutre like queue.Queue
"""

def consume():

    # consume till event is not set,
    # or if queue still has elements
    # second condition ensures final messages are not lost
    while not event.is_set() or len(queue):
        time.sleep(0.5)
        full.acquire()
        x = queue.popleft()
        empty.release()

        print("Consuming {}".format(x))


def produce():
    count = 1
    while not event.is_set():

        empty.acquire()
        queue.append(count)
        print("Produced {}".format(count))

        count += 1
        full.release()


if __name__ == '__main__':
    global queue
    queue = deque()
    event = Event()
    full = Semaphore(0)
    empty = Semaphore(Q_CAP)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(produce)
        executor.submit(consume)
        time.sleep(1)
        event.set()

