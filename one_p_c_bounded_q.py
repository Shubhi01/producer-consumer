from collections import deque
import concurrent.futures
from threading import Event
import time
"""
Single producer
Single consumer
"""

global queue
global event
Q_CAP = 5


def consume():

    # consume till event is not set,
    # or if queue still has elements
    # second condition ensures final messages are not lost
    while not event.is_set() or len(queue):
        # time.sleep(1)
        if len(queue) > 0:
            x = queue.popleft()
            print("Consuming {}".format(x))

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
def produce():
    count = 1
    while not event.is_set():
        # time.sleep(1)
        if (len(queue) < Q_CAP):
            print("Producing {}".format(count))
            queue.append(count)
            count += 1


if __name__ == '__main__':
    global queue
    queue = deque()
    event = Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(produce)
        executor.submit(consume)
        time.sleep(0.1)
        event.set()

