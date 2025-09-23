#Class methods are nothing but pythons attempt of constructor overloading 
class ChaiOrder:
    def __init__(self, tea_type, sweetness, size):
        self._tea_type = tea_type
        self.sweetness = sweetness
        self.size = size

    @classmethod
    def from_dict(cls,order_data): # yes no self
        return cls(
            order_data["tea_type"],
            order_data["sweetness"],
            order_data["size"]
        )
    
    @classmethod
    def from_list(cls,order_data):
        return cls(
            order_data[0],
            order_data[1],
            order_data[2]
        )

    @classmethod
    def from_str(cls,order_data: str):
        order = order_data.split('-')
        return cls.from_list(order)
    
order1 = ChaiOrder.from_dict({"tea_type":"adrak", "sweetness": 'none', "size":"cutting"})
print(order1.__dict__)

order2 = ChaiOrder.from_str('masala-moderate-full')
print(order2.__str__)
print(order2.__dict__)