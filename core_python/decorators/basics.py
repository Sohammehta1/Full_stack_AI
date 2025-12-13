# Used to decorate blocks
# Just like function pointers in c/c++
# useful if  I want to do something common/similar before and after
#  multiple functions

from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper():
        print("Before function runs")
        func()
        print("After function runs")
    return wrapper

@my_decorator
def greet():
    print("Hello from decorators class from chai code")

greet()
print(greet.__name__)