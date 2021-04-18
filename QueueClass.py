'''
# Representation of queue that will be used with the conversion for the frames
# Locks will also be used to avoid race conditions as well as accidental deletion of frames and so on
'''

import threading

class queueClass:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(10)

    def put(self, item):
        self.empty.acquire() # This is the lock semaphore
        self.lock.acquire() # This is locking the lock
        self.queue.append(item) # This is adding our new frames
        self.lock.release() # This is releasing the lock
        self.full.release()

    def get(self):
        self.full.acquire() # This is the lock semaphore
        self.lock.acquire() # This is locking the lock
        item_popped = self.queue.pop(0) # This pops at the first position
        self.lock.release() # This releases the lock
        self.empty.release() # This releases the semaphore
        return item_popped # Returns the item

    def markEnd(self):
        self.put('end') # This is for when we finish the frames we are adding
