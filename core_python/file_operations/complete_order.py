_COUNT: int = 0

class InvalidChaiError(Exception):pass

def bill(flavor, cups):
    global _COUNT
    menu = {"masala": 20,
             "ginger": 25,
            }
    try:
        _COUNT +=1
        print('----------------------\nOrder number: %i'%_COUNT)
        if flavor  not in menu:
            raise InvalidChaiError(f"{flavor} flavor chai is not available")
        if not isinstance(cups,int):
            raise TypeError(f"Cups must be an int, not a {type(cups)}")
        total = menu[flavor] *cups
        print(f"Your bill is {total} rs")
    except Exception as e:
        print("ごめんなさい 🙇: %s"%e)
    finally:
        print('''
Thank you for visiting!
----------------------''')

bill('mint',2)
bill("masala",3)