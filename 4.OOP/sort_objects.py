class Fruit:
    def __init__(self, f,q):
        self.fruit = f
        self.quantity = q

    def __str__(self):
        return '{} {}'.format(self.quantity, self.fruit)
    
    def __lt__(self,other_fruit): # Sorted uses lt only, so either define comparison 
        #in __lt__ or pass it as a lambda function in the sorted function itself.
        return self.quantity  <other_fruit.quantity

    def sortPriority(self): return self.quantity

L  = [
    Fruit("Apple", 10),
    Fruit("Cherry", 50),
    Fruit("Mango", 5)
]

for fruit in sorted(L):
    print(fruit)

grape = Fruit("grape", 20)
assert grape.quantity == 10