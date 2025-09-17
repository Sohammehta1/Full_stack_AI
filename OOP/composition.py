class BaseChai:
    def __init__(self,type):
        self.type = type
    
    def prepare(self):
        print(f"Preparing {self.type} chai")

class MasalaChai(BaseChai):
    def __init__(self, type):
        super().__init__(type)
    
    def addSpices(self):
        print("Adding cardamom, ginger, cloves.")

class SpecialChai:
    baseChai = BaseChai # composition

    def __init__(self, type):
        self.tapari = BaseChai(type)
    
    def prepare(self):
        self.tapari.prepare()

sc = SpecialChai("Masala")
sc.prepare()

# What exactly is the difference between inheritence and composition

#1.
# we call the functions of the parent class in composition seperately.
# In inheritence we can either keep the parent function or override it.

#2. We can choose when to instantiate the parent class.
#3. We can change the parent class at any time by just replacing 
#the class with other classes


