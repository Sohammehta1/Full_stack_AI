#The order of inheritence defines which parent class method gets 
# called first.

class A:
    label = "a"

class B(A):
    label = "b"

class C(A):
    label = "c"

class D(B,C):
    pass

print(D.label)