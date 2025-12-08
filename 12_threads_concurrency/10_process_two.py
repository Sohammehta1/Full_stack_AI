from multiprocessing import Process
import time

def cpu_heavy():
    print(f"Crunching some numbers...")

    total = 0
    for i in range(10**7):
        total +=i
    print("Done ✅")

start  = time.time()
processess = [Process(target=cpu_heavy) for _ in range(2)]

[t.start() for t in processess]
[t.join() for t in processess]

end = time.time()
print(f"Time taken: {end-start}")