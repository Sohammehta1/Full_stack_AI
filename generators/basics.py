# GENERATORS: used for optimizing memory
# generators also allow you to use special functions directly  

values = [1,2,3,4,5]

list_comp = [val for val in values] # processes entire list at the same time in memory.

generator = (val for val in values) # processses elements as a stream, not all at once.
# print(f"sum of list elements: {sum(generator)}")
# print(generator)

#YIELD: lazy evaluation

# If we run a loop using a function returning with yield then 
# Then the function actually pauses execution at each iteration
# Like in the given example, the function pauses 2 times and yields the value one at a time.
# This also allows the function to return multiple values without using much memory.

def serve_chai():
    yield "cup 1: masala chai"
    yield "cup 2: adrak chai"
    yield "cup 3: elaichi chai"

stall =  serve_chai()

for cup in stall:
    print(cup)
print()
#### Iterating without using loops -> next

stall2 = serve_chai()

print(next(stall2))
print(next(stall2))
print(next(stall2)) 

