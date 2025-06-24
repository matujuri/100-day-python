# arguments default values
def foo(a, b=4, c=6): 
    print(a, b, c)

foo(1)

# dynamic arguments
def add(*args):
    print(args)
    return sum(args)

print(add(1, 2, 3, 4, 5))

# keyword arguments
def calculate(n, **kwargs):
    print(kwargs)
    # for key, value in kwargs.items():
    #     print(key, value)
    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)

calculate(2, add=3, multiply=5)

class Car:
    def __init__(self, **kwargs):
        self.make = kwargs.get("make")
        self.model = kwargs.get("model")
        self.color = kwargs.get("color")

my_car = Car(make="Nissan", model="GT-R", color="Red")
print(my_car.make)
print(my_car.model)
print(my_car.color)