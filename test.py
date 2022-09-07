def decorator1(func):
    def wrapper(*args, **kwargs):
        print("the decoretor is decoretor1 !")
        func(*args, **kwargs)
    return wrapper

def decorator2(func):
    def wrapper(*args, **kwargs):
        print("the decoretor is decoretor2 !")
        func(*args, **kwargs)
    return wrapper

@decorator1
@decorator2
def myfun(func_name):
    print('This is a function named :', func_name)


myfun('myfun')
