## How to send data to generators

def chai_customer():
    print("Welcome! what chai would you like")
    order = yield
    while True:
        print(f"Preparing :{order}" )
        order= yield

stall = chai_customer()

next(stall) # starting the generator

stall.send("Masala chai")
stall.send("Lemon Chai")

# The yield causes the function to pause execution
# Thus the function does not run into an infinite loop