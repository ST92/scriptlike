
import itertools


def asd_foobar(x,y):
    print(x)
    print(y)
    return 13

def boo(x):
    lol = asd_foobar(x,x)
    print("Boo!", lol*2)
    return lol*2