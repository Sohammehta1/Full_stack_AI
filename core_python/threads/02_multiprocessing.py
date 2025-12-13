from multiprocessing import Process
from time import sleep

def brew_chai(name):
    print(f"Start of {name} chai brewing")
    sleep(3)
    print(f"End of {name} chai brewing")

if __name__ == "__main__":
    chai_makers = [
        Process(target=brew_chai, args=(f"Chai Maker #{i+1}", ))
        for i in range(3)
    ]

    # Start all processess
    for p in chai_makers:
        p.start()
    
    # Wait for them to finish
    for p in chai_makers:
        p.join()
    
    print("All chai served")