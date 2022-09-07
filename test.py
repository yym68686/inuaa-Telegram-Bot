# import decorator1, decorator2 from test1
import test1

@test1.decorator1
@test1.decorator2
def myfun(func_name):
    print('This is a function named :', func_name)


myfun('myfun')
