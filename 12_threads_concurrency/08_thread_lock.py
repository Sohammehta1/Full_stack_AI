import threading
import time

counter = 0
lock = threading.Lock()

def increment():
    global counter
    # Using lock here means I am protecting the increment and not the loop
    # Thus lock will be changed for every iteration,
    for _ in range(100_000_000):
        with lock:  
            counter += 1
        counter +=1
if __name__ == "__main__":
    start = time.time()

    p1 = threading.Thread(target=increment)
    p2 = threading.Thread(target=increment)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    end= time.time()

    print(f"Total time is {end-start:.2f}s")