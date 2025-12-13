# GIL: Global interpreter lock : used by python as mutex for protecting critical objects

import threading
import time

COUNT = 0

def brew_chai():
    print(f"{threading.current_thread().name} started brewing...")
    global COUNT
    while COUNT < 100_000_000:
        COUNT +=1
    print(f"{threading.current_thread().name} finished brewing")

t1 = threading.Thread(target=brew_chai, name= "barista1")
t2 = threading.Thread(target=brew_chai, name= "barista2")

start = time.time()
t1.start()
t2.start()

t1.join()
t2.join()

stop = time.time()

print(f"Total time taken is {stop-start:.2f}s")