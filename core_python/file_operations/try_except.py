def process_order(item: int, quantity: int):
    try:
        price = {"masala": 10}[item]
        if isinstance(quantity,int):
            cost = price*quantity
            print(f'Total cost is :{cost}')
        else:
            # raise TypeError(f"Quantity must be an int not a : {type(quantity)}")
            raise TypeError(type(quantity))
    except KeyError as k:
        print(f"Sorry, we dont make {k} chai here.")
    except TypeError as e:
        print(f"Quantity must be an integer not a {e}")

process_order("ginger",2)
process_order("masala","two")

process_order("masala",2)