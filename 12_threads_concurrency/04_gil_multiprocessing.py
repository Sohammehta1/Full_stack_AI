from multiprocessing import Process
import time

COUNT = 0

def chai_brewing():
    print("Started the count process...")
    for _ in range(100_000_000):
        COUNT +=1
    print("Ended the count process...")

if __name__ == "__main__":
    start = time.time()

    p1 = Process(target=chai_brewing)
    p2 = Process(target=chai_brewing)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    end= time.time()

    print(f"Total time with multiprocessing is {end-start:.2f}s")
