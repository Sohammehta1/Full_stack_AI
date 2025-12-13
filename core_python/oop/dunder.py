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

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Point ({}, {})'.format(self.x,self.y)
    
    def __add__(self, otherPoint):
        return Point(self.x + otherPoint.x,self.y + otherPoint.y)
    
    def __sub__(self, otherPoint):
        return Point(self.x - otherPoint.x,self.y - otherPoint.y)

# Here instead of updating current attributes new instance is created and returned.

p1 = Point(1,3)
p2 = Point(3,5)
print(p1+p2)    
