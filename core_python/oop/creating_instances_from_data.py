# cityNames = ['Pune','Mumbai', 'Nashik']
# populations = [10000, 30000, 8000]
# states = ['MH','MH','MH']

# city_tuples = zip(cityNames,populations,states)

# class City:
#     def __init__(self,n,p,s):
#         self.name = n
#         self.population = p
#         self.state = s

#     def __str__(self): #used when string is expected to be returned from an object
#         return '{}, {} (pop: {})'.format(self.name,self.state, self.population)   

# cities = [City(*t) for t in city_tuples]

# for city in cities: print(city) 

class Cereal:
    def __init__(self,name: str, brand: str, fiber: int):
        self.name  = name
        self.brand = brand
        self.fiber = fiber
    
    def __str__(self):
        return "{} cereal is produced by {} and has {} grams of fiber in every serving!".format(
            self.name,self.brand,self.fiber)
        
c1 = Cereal("Corn Flakes","Kellogg's",2)
print(c1)

c2 = Cereal("Honey Nut Cheerios","General Mills",3)
print(c2)