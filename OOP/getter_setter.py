#PROPERTY DECORATORS

class TeaLeaf:
    def __init__(self,age):
        self._age:int = age

    @property
    def Age(self):
        return self._age
    
    @Age.setter 
    def Age(self,age:int):
        self._age = age
    #This setter needs to be set on the get propery
    # It is like setter function overrides the getter function 
    # when argument is provided

    @Age.setter
    def Age(self,values: list):
        print("Hi, you called alternate setter function")
        self._age = values[0]
        print(f"Type of leaf is {values[1]}")

    

leaf = TeaLeaf(4)
print(f"Age of leaf is : {leaf.Age}")
leaf.Age = [4,5]
